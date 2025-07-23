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
ADVOGPT/
├── .pytest_cache/
|    ├── V\cache
|    |   ├── lastfailed
|    |   └── nodeids
|    ├──gitignore
|    ├──CACHEDIR.TAG
|    └──README.md
├── .vscode
|    └── settings.json
├── app/
│     ├──__pycache__/
|     |   ├──_init_cpython-313.pyc
|     |   └──main.cpython-313.pyc
|     ├──api/
│     ├── __pycache__
│     ├── __init__.py
│     ├── aprofundar_resposta.py
|     ├── auth.py
|     ├── documentos.py
│     ├── download_peticao.py
│     ├── elabora_peca.py
|     ├── pdf_final.py
|     ├── router.py
|     ├── upload_logo.py
│     └── upload.py
├── core/
|   ├──___pycache__
|   ├── __init__.py
|   ├── db.py
|   ├── deps.py
|   ├── logging_monitor.py
│   └── security.py
├── models/
|   ├── __pycache__
|   ├── documento.py
|   └── usuario.py
├── __init__.py
├── services/
|   ├── __pycache__
|   ├── __init__.py
|   ├── auth.py
|   ├── hash_ultils.py
|   ├── limpeza.py
|   └── rag.py
├── main.py
├── dados/
|   ├── clientes/
│   ├── fontes_convertiveis/
│   │   ├── doc_001_crianca_com_deficiencia_intelectual_1...
│   │   ├── doc_002_contrato_benefícios_previdenciários....
│   │   ├── doc_003_procuracao_para_analfabeto.doc
│   │   └── doc_004_procuracao_ad_judicia_et_extra_com_...
│   ├── fontes_extra/
|   ├── logos/
|   |   └── logo_padrao.png
│   ├── pdfs/
│   │   └── Direito-Processual-Previdenciário (1.1).pdf
│   ├── pdfs_coletados/
│   ├── peticoes_geradas/
│   │   └── peticao_loas_teofilo.docx
│   ├── textos/
│   │   └──.txt
│   ├── textos_base/
│   │   ├── DECRETO_3048_1999.txt
│   │   ├── DECRETO_10410_2020.txt
│   │   ├── EC_103_2019.txt
│   │   ├── LEI_8213_1991.txt
│   │   └── LEI_9876_1999.txt
│   ├── textos_descartados/
│   ├── textos_limpos/
│   ├── textos_pendentes/
│   │   ├── exemplo_sujo.txt
│   │   └── regras_transicao_ec103_2019.txt
│   ├── textos_repetidos/
│   ├── textos_revisados/
│   │   ├── exemplo_sujo.txt
│   │   └── regras_transicao_ec103_2019.txt
│   ├── vetores/faiss_index/
│   │   ├── index.faiss 
|   |   └── index.pkl                           
|   └── docs/
│   |   ├── gitgnore_explicado.md
|   |   ├── RELATORIO_DIARIO.md 
|   |   ├── relatorio-backend-13-07-2025.md
|   |   ├── relatorio-backend-14-07-2025.md  
|   |   ├── ROADMAP.md   
|   |   └── testes.md    
│   |    
├── drivers/
|   └──chromodriver.exe
├── logs/
│   ├── erros_conversao.txt
│   └── renomeados.txt                                                   
├── relatorios/
│   ├── coleta_planalto.csv                                                  
│   ├── documentos_embutidos.csv
│   ├── duplicatas_detectadas.csv
│   ├── extracoes_com_erro.csv
│   ├── log_revisoes.csv
│   ├── resumo_arquivos.csv
│   └── termos_frequentes.csv
├── scripts/ 
│   ├── analisa_termos_indexados.py
│   ├── extrai_e_limpa_drive.py
│   ├── gera_relatorio_csv.py
│   ├── limpa_textos_pendentes.py
│   ├── mover_textos_suspeitos.py
│   ├── valida_textos.py
│   └── verificador_de_duplicatas.py
├── src/
|   ├── agentes_juridicos/
│   |   ├── _pycache_
|   |   └── advogado_previdenciario.py  
|   ├── coleta_web/   
|   |   ├── coleta_agendada.py      
│   |   ├── coleta_legislacao_planalto.py   
|   |   ├── coleta_normas_filtradas.py  
│   |   ├── coleta_normas_inss.py      
│   |   └── coleta_normas_selenium.py   
│   |     
|   ├── documentos/    
|   |   ├── _pycache_  
|   |   ├── docx2pdf_fallback.py  
|   |   ├── elaborador_pecas.py     
|   |   └── gerador_pdf_formatado.py
|   ├── extracao/     
|   |   └── extrai_texto.py 
|   ├── fragmentacao/ 
|   ├── gpt_ultilidades/
|   |     ├──_pycache_ 
|   |     └── refinador_consulta.py
|   ├──indexacao/
|   |  └── indexa_com_faiss.py
|   ├──limpeza/
|   |  └── limpa_textos.py
|   ├──rag_pipeline/
|   |  └── pergunta_ao_robo.py(codigo todo comentado)
|   ├── ultilidades/
|   |   └── carrega_configuracoes.py
│   ├── streamlit_apps/          
|   |   ├── analisador_lexico.py 
|   |   ├── central_pipeline.py
|   |   ├── painel_estatisticas.py
|   |   └── revisor_visual.py
|   | 
│   ├── tests/ 
|   |  ├── __pycache__
│   |  ├── test_api.py
│   |  ├── test_estrutura.py
│   |  ├── test_hash_utils.py
│   |  ├── test_limpeza.py
│   |  └── testa_docx.py
│   |
|   ├── venv/
|   |   ├── etc\jupiter\nbconfig\notebook.d
|   |   ├── pydesc.json
|   |   ├── include\site\python3.13\greenlet
|   |   |   └── greenlet.h
|   |   ├── lib
|   |   ├── Scripts
|   |   └── share
|   |       └── pyvenv.cfg
|   |
|   ├── .coverage
|   ├── .env
|   ├── .env.example
|   ├── .gitignore
|   ├── abre_docs_vscode.bat
|   ├──app.db
|   ├── coleta_planalto.bat
|   ├── converte_doc_para_docx.py
|   ├── coverage.xml
|   ├── executa_pipeline.py
|   ├── executa_tudo_agendado.py
|   ├── executa_tudo.py
|   ├── inicia_painel_central.bat
|   ├── inicia_pipeline_agendado.bat
|   ├── inicia_pipeline.bat
|   ├── inicia_revisor.bat
|   ├── README.md
|   ├── renomeador_doc_inteligente.py
|   ├── requirements.txt
|   ├── revisar_novo_texto.bat
|   └── testar_api.http
```


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
```


---

🧠 *Automação com rastreabilidade e propósito. Esse é o PrevInfoBot.*

---
### RAG Jurídico
A funcionalidade de consulta jurídica usa Retrieval-Augmented Generation (RAG):
- **Índice FAISS**: Carrega documentos de `dados/vetores/faiss_index`.
- **Embeddings**: `OpenAIEmbeddings` para vetorização.
- **LLM**: `ChatOpenAI` (GPT-4, temperatura 0.3) para respostas precisas.
- **Cadeia**: `RetrievalQA` com `chain_type="stuff"`, buscando 4 documentos mais relevantes.
A lógica está em `app/services/rag.py` e é exposta via endpoint `/consultar`.
----
Comandado por **Teófilo**, com apoio do Copilot ⚖️
