---
paths:
  - "src/nutri_rag/config.py"
  - "pyproject.toml"
  - "requirements.txt"
  - ".env.example"
---

# Configuração e dependências

- Leia configurações externas pelo `.env` e mantenha valores de exemplo sem credenciais reais em `.env.example`.
- Nunca grave, imprima ou inclua chaves de API em código, logs, documentação ou arquivos versionados.
- Ao adicionar uma variável de ambiente, documente seu nome e finalidade no README e no `.env.example`.
- Mantenha as dependências Python declaradas em `pyproject.toml`; `requirements.txt` deve continuar apontando para a instalação do projeto.
- Não coloque credenciais do Gemini nos componentes locais de embeddings ou reranking.
