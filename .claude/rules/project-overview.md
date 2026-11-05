# Nutri RAG

- O projeto é um RAG em Python para consultar os PDFs de alimentação e nutrição em `data/`.
- O fluxo é: carregar PDFs e metadados, dividir em trechos, gerar embeddings locais, indexar no FAISS, recuperar candidatos, reordenar com Cross-Encoder e responder com Gemini.
- Os embeddings e o reranking usam Sentence Transformers localmente. O Gemini é usado para geração de resposta.
- A aplicação é uma CLI iniciada por `python main.py`; `python main.py --index-only` prepara o índice.
- Responda e documente o projeto em português, salvo quando o usuário pedir outro idioma.
