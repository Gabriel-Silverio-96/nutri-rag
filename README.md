# Nutri RAG

Assistente inteligente de perguntas e respostas sobre **alimentação e nutrição**, desenvolvido com arquitetura **RAG (Retrieval-Augmented Generation)** para fornecer respostas contextualizadas e fundamentadas em documentos PDF, com referências às páginas consultadas.

A solução implementa um pipeline de processamento que inclui extração de texto, segmentação de documentos (_chunking_), geração de embeddings, busca semântica e _reranking_ para aprimorar a relevância dos conteúdos recuperados. As informações selecionadas são utilizadas por um modelo de linguagem (LLM) para gerar respostas contextualizadas.

Os documentos são organizados no diretório `data/`, com indexação e armazenamento vetorial local utilizando **FAISS**. A geração de embeddings e o reranking são realizados localmente com **Sentence Transformers**, permitindo maior controle sobre o processamento e a recuperação das informações.

## Requisitos

- Python 3.10 ou superior
- Chave da API do Gemini

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Edite `.env` e informe sua chave em `GEMINI_API_KEY`. Você pode gerar uma chave no [Google AI Studio](https://aistudio.google.com/apikey). O chat pode ser configurado por `GEMINI_CHAT_MODEL`, os embeddings por `SENTENCE_TRANSFORMER_MODEL` e o reranker por `CROSS_ENCODER_MODEL`.

## Indexar os documentos

Os PDFs existentes em `data/` serão descobertos automaticamente, inclusive em subpastas. Cada pasta tem um `metadata.json`; seus campos são anexados às páginas do PDF e preservados nos trechos indexados. Para responder, o FAISS recupera os 50 candidatos mais próximos e o Cross-Encoder reordena esses trechos; os 5 primeiros seguem para o Gemini. Crie o índice FAISS:

```bash
python main.py --index-only
```

Recrie o índice depois de alterar os PDFs ou seus metadados, trocar o modelo local de embeddings ou mudar as configurações de divisão:

```bash
python main.py --index-only --rebuild
```

O índice local é salvo em `vector_store/

## Fazer perguntas

```bash
python main.py
```

| Escopo | Pergunta |
| --- | --- |
| Coberta pelos documentos | Quais são as diferenças entre margarina e manteiga? |
| Coberta pelos documentos | Qual é a tabela nutricional do tomate de árvore? |
| Coberta pelos documentos | Quais são os benefícios da linhaça? |
| Fora do escopo atual | Quais são os valores nutricionais do morango branco chileno? |
| Fora do escopo atual | Quais alimentos são comuns no Chile? |
| Fora do escopo atual | Como fazer hambúrguer? |

As respostas usam os trechos recuperados e citam o nome do PDF e a página. O assistente informa quando não encontra a resposta nos documentos.
