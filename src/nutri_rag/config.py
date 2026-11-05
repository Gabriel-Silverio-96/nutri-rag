import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
VECTOR_STORE_DIR = ROOT_DIR / "vector_store"
SYSTEM_PROMPT = (
        "Você é um assistente que responde dúvidas sobre alimentação e nutrição "
        "com base apenas nos trechos fornecidos. Responda em português claro. "
        "Inclua citações no formato [nome do arquivo, p. N] para as afirmações "
        "apoiadas pelos trechos. Se a informação não estiver nos documentos, "
        "diga isso com clareza e não invente. Não faça diagnóstico nem prescreva "
        "tratamento ou dieta individualizada."
)

def load_settings() -> tuple[str, str]:
    load_dotenv(ROOT_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY não encontrada. Crie um arquivo .env e informe sua chave do Gemini."
        )
    return (
        api_key,
        os.getenv("GEMINI_CHAT_MODEL"),
    )


def get_embedding_model() -> str:
    load_dotenv(ROOT_DIR / ".env")
    return os.getenv(
        "SENTENCE_TRANSFORMER_MODEL",
    )


def get_reranker_model() -> str:
    load_dotenv(ROOT_DIR / ".env")
    return os.getenv(
        "CROSS_ENCODER_MODEL",
    )
