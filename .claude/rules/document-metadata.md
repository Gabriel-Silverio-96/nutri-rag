---
paths:
  - "data/**/*.json"
  - "data/**/*.pdf"
---

# Metadados dos documentos

- Mantenha um `metadata.json` ao lado de cada PDF, codificado em UTF-8 e contendo um único objeto JSON.
- Registre apenas dados que possam ser confirmados no próprio documento ou em uma fonte confiável: título, autoria institucional, editora, ano, idioma, tipo, descrição, assuntos, palavras-chave e identificadores bibliográficos quando disponíveis.
- Use `pt-BR` para os documentos em português do Brasil e preserve os nomes e acentos do documento.
- Não atribua a um PDF informações que pertencem a outro documento. Se um campo não puder ser confirmado, omita-o em vez de adivinhar.
- Ao mudar um `metadata.json`, lembre que os metadados só entram no FAISS após reconstruir o índice.
