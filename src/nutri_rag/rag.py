import json
from functools import lru_cache
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder

from nutri_rag.config import (
    DATA_DIR,
    VECTOR_STORE_DIR,
    SYSTEM_PROMPT,
    get_embedding_model,
    get_reranker_model,
    load_settings,
)


def _embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=get_embedding_model(),
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        show_progress=True,
    )


@lru_cache(maxsize=1)
def _reranker() -> CrossEncoder:
    return CrossEncoder(get_reranker_model(), device="cpu")


def build_index(rebuild: bool = False) -> FAISS:
    """Cria o índice FAISS local a partir dos PDFs em data/."""
    if VECTOR_STORE_DIR.exists() and not rebuild:
        return FAISS.load_local(
            str(VECTOR_STORE_DIR),
            _embeddings(),
            allow_dangerous_deserialization=True,
        )

    pdf_paths = sorted(DATA_DIR.rglob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"Nenhum PDF encontrado em {DATA_DIR}")

    pages = []
    for pdf_path in pdf_paths:
        document_pages = PyPDFLoader(str(pdf_path)).load()
        metadata_path = pdf_path.with_name("metadata.json")
        if metadata_path.exists():
            document_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if not isinstance(document_metadata, dict):
                raise ValueError(f"Metadados devem ser um objeto JSON: {metadata_path}")
            for page in document_pages:
                page.metadata.update(document_metadata)
        pages.extend(document_pages)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    )
    chunks = splitter.split_documents(pages)
    if not chunks:
        raise ValueError("Não foi possível extrair texto dos PDFs encontrados.")

    index = FAISS.from_documents(chunks, _embeddings())
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    index.save_local(str(VECTOR_STORE_DIR))
    return index


def answer_question(
    question: str,
    index: FAISS,
    k: int = 5,
    candidate_k: int = 50,
) -> tuple[str, list[str]]:
    api_key, chat_model = load_settings()
    candidates = index.similarity_search(question, k=candidate_k)
    if not candidates:
        return "Não encontrei trechos relevantes nos documentos indexados.", []

    scores = _reranker().predict(
        [(question, document.page_content) for document in candidates],
        show_progress_bar=False,
    )
    ranked = sorted(
        zip(scores, candidates),
        key=lambda item: float(item[0]),
        reverse=True,
    )
    documents = [document for _, document in ranked[:k]]

    excerpts = []
    sources = []
    for document in documents:
        source = Path(document.metadata.get("source", "documento")).name
        page = document.metadata.get("page")
        page_label = str(page + 1) if isinstance(page, int) else "?"
        citation = f"{source}, p. {page_label}"
        excerpts.append(f"[{citation}]\n{document.page_content}")
        if citation not in sources:
            sources.append(citation)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Pergunta: {question}\n\nTrechos dos documentos:\n{context}"),
        ]
    )
    model = ChatGoogleGenerativeAI(
        model=chat_model,
        google_api_key=api_key,
    )
    response = (prompt | model).invoke(
        {"question": question, "context": "\n\n".join(excerpts)}
    )
    content = response.content
    if isinstance(content, list):
        answer = "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    elif isinstance(content, str):
        answer = content
    else:
        answer = str(content)

    return answer, sources
