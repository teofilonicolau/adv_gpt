## 🧠 RAG Jurídico

A funcionalidade de consulta jurídica do **PrevInfoBot** utiliza Retrieval-Augmented Generation (RAG) para responder perguntas com base em normas, doutrina e jurisprudência. A lógica está centralizada em:

- **Backend**: 
  - `app/api/router.py`: Endpoint `/consultar` para consultas jurídicas e `/feedback` para avaliações.
  - `app/services/rag.py`: Carrega índices FAISS (`dados/vetores/faiss_index_{area}`) e usa `langchain` com GPT-4.
- **Frontend**:
  - `src/pages/ConsultaApp.jsx`: Página principal de consulta.
  - `src/components/ConsultaForm.jsx`: Formulário com seletor de área jurídica.
  - `src/components/RespostaBox.jsx`: Exibe respostas e permite enviar feedback.

### Funcionalidades
- **Suporte Multi-Área**: Suporta Previdenciário, Consumidor e Processual Civil.
- **Rate Limiting**: Limita a 5 requisições/minuto por usuário (usando Redis).
- **Cache**: Respostas armazenadas em Redis por 1 hora.
- **Logs**: Consultas salvas em `relatorios/consultas_rag.csv`.
- **Feedback**: Usuários podem avaliar respostas via endpoint `/feedback`, salvas em `relatorios/feedback_rag.csv`.

### Como Testar
```bash
# Testar consulta
curl -X POST http://localhost:8000/consultar -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"pergunta": "Qual a idade mínima para o LOAS?", "area": "previdenciario"}'

# Testar feedback
curl -X POST http://localhost:8000/feedback -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"pergunta": "Qual a idade mínima para o LOAS?", "resposta": "65 anos...", "feedback": "Resposta correta."}'