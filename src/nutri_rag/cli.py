import argparse

from nutri_rag.config import DATA_DIR
from nutri_rag.rag import answer_question, build_index


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG de alimentação e nutrição")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Cria o índice FAISS e encerra sem iniciar o chat.",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Recria o índice FAISS a partir dos PDFs.",
    )
    args = parser.parse_args()

    try:
        pdf_count = len(list(DATA_DIR.rglob("*.pdf")))
        print(f"Preparando índice FAISS com {pdf_count} PDF(s)...")
        index = build_index(rebuild=args.rebuild)
        print("Índice pronto.")
        if args.index_only:
            return

        print("Faça uma pergunta sobre os documentos (ou digite 'sair').")
        while True:
            question = input("\nVocê: ").strip()
            if question.lower() in {"sair", "exit", "quit"}:
                break
            if not question:
                continue
            response, _ = answer_question(question, index)
            
            print(f"\nNutri RAG: {response}")
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
