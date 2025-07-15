# 📡 Backend — Melhorias Implementadas (13/07/2025)

## 🗂️ Upload de Logo por Escritório

- Criado o endpoint `POST /upload_logo`
- Recebe arquivos `.png`, `.jpg` e salva em `dados/logos_clientes/logo_{id_escritorio}.png`
- Validação do tipo de arquivo incluída
- Estrutura segura com uso de `Path.mkdir()` e `UploadFile`

## 📄 Geração de PDF Personalizado

- Modificado `app/api/pdf_final.py`
- Adicionado parâmetro `id_escritorio` na rota `POST /api/gerar_peticao_final_pdf`
- O caminho da logo agora busca automaticamente:
  - `dados/logos_clientes/logo_{id_escritorio}.png`
  - Fallback para `logo_padrao.png` se não existir
- Mantida compatibilidade com `gerador_pdf_formatado.py`

## 📂 Organização de diretórios

- Criada ou reforçada estrutura:
  - `dados/logos_clientes/` → logos por escritório
  - `dados/peticoes_geradas/` → arquivos gerados
