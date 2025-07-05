# ⚖️ PrevInfoBot – Robô Jurídico com IA e RAG
![Análise Léxica](https://img.shields.io/badge/an%C3%A1lise%20l%C3%A9xica-ativa-blueviolet?style=flat-square&logo=streamlit)


> Desenvolvido com propósito, escalabilidade e didatismo por Teófilo e assistido pelo Copilot

---

## 📌 Índice

- [🎯 Objetivo](#-objetivo)
- [🛠️ Stack Tecnológica](#️-stack-tecnológica)
- [📁 Estrutura do Projeto (atualizada)](#-estrutura-do-projeto-atualizada)
- [✅ Testes Automatizados](#-testes-automatizados)
- [🧠 Pipeline Geral](#-pipeline-geral)
- [🖱️ Como Executar](#️-como-executar)
- [📚 Documentação complementar](#-documentação-complementar)
- [🧩 Expansão futura](#-expansão-futura)

---

## 🎯 Objetivo

Criar um assistente jurídico especializado em **Direito Previdenciário**, capaz de:

- Processar documentos em lote (.pdf, .docx, imagens)
- Realizar limpeza e revisão com validação semiautomática
- Gerar respostas jurídicas com base em jurisprudência e normas
- Ser acessado por API ou interface visual (Streamlit)

---

## 🛠️ Stack Tecnológica

| Tecnologia        | Função Principal                       |
|-------------------|----------------------------------------|
| Python + FastAPI  | Backend e serviços REST                |
| LangChain + FAISS | Vetorização e RAG                      |
| GPT-4 (OpenAI)     | Geração de respostas                   |
| Streamlit         | Revisão visual e dashboards            |
| Pytest + pytest-cov| Testes automatizados                   |

---

## 📁 Estrutura do Projeto (atualizada)

```
PREVINFOBOT-CORRETO/
├── app/
│   ├── api/router.py
│   ├── core/
│   └── services/
│       ├── hash_utils.py
│       ├── limpeza.py
│       └── rag.py
│
├── dados/
│   ├── pdfs_coletados/
│   ├── textos_pendentes/
│   ├── textos_revisados/
│   ├── textos_limpos/
│   └── vetores/faiss_index/
│
├── scripts/
│   ├── extrai_e_limpa_drive.py
│   ├── limpa_textos_pendentes.py
│   ├── gera_relatorio_csv.py
│   ├── valida_textos.py
│   └── mover_textos_suspeitos.py
│
├── streamlit_apps/
│   ├── revisor_visual.py
│   ├── painel_estatisticas.py
│   └── central_pipeline.py
│
├── tests/
│   ├── test_api.py
│   ├── test_hash_utils.py
│   ├── test_limpeza.py
│   └── test_estrutura.py
│
├── converte_doc_para_docx.py
├── renomeador_doc_inteligente.py
├── executa_tudo.py
├── execute_pipeline.py
├── inicia_painel_central.bat
├── inicia_revisor.bat
├── requirements.txt
├── .env
├── .gitignore
└── docs/
    ├── testes.md
    ├── ROADMAP.md
    └── gitignore_explicado.md
```

---

## ✅ Testes Automatizados

Rodar:

```powershell
$env:PYTHONPATH="."
pytest --cov=app tests/
```

Cobertura atual:

- `router.py`: 100%
- `hash_utils.py`: 100%
- `limpeza.py`: 100%
- `rag.py`: 77%

Total: **68%**

> Mais detalhes em: [✅ Testes Automatizados](docs/testes.md)

---

## 🧠 Pipeline Geral

| Etapa                        | Status |
|-----------------------------|--------|
| Extração e OCR              | ✅     |
| Limpeza de textos brutos    | ✅     |
| Validação automática        | ✅     |
| Revisão visual em Streamlit | ✅     |
| Geração de log e relatório  | ✅     |
| Vetorização com FAISS       | ✅     |
| Integração RAG + GPT-4      | ✅     |
| API REST (FastAPI)          | ✅     |

---

## 🚀 Como Executar

### Ativar ambiente virtual (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
````

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Rodar pipeline completa

```bash
python executa_tudo.py
```

### Iniciar API local (FastAPI)

```powershell
$env:PYTHONPATH="."
uvicorn app.main:app --reload
```

Acesse a API em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Abrir interface de revisão (Streamlit)

```bash
streamlit run streamlit_apps/central_pipeline.py
```

### Ou use os atalhos `.bat`:

* `inicia_painel_central.bat` — Inicia a interface central
* `inicia_revisor.bat` — Inicia o módulo revisor

---  

## 📚 Documentação complementar

- [📌 Roadmap de evolução](docs/ROADMAP.md)
- [✅ Testes Automatizados](docs/testes.md)
- [🧾 Explicação do .gitignore](docs/gitignore_explicado.md)

---

## 🧩 Expansão futura

- [ ] Exportar respostas como `.pdf`
- [ ] Treinar modelos locais com jurisprudência
- [ ] GitHub Actions com CI/CD dos testes
- [ ] Expansão para outras áreas do Direito

---
## 📊 Análise Léxica Interativa

![image](https://github.com/user-attachments/assets/36a5061f-d44a-40d6-96e2-6f7bccc49dce)


Agora o projeto conta com um painel visual para **análise de termos mais frequentes** nos textos já limpos. Isso permite verificar se a base está cobrindo bem os temas jurídicos esperados.

### ▶️ Como rodar

```powershell
.\venv\Scripts\Activate.ps1
streamlit run streamlit_apps\analisador_lexico.py


---

🧠 *Automação com rastreabilidade e propósito. Esse é o PrevInfoBot.*



Comandado por **Teófilo**, com apoio do Copilot ⚖️
