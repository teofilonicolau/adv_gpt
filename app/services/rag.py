import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import redis.asyncio as redis  # Ajustado para redis.asyncio

load_dotenv()
CAMINHO_INDICE = "dados/vetores/faiss_index"  # Ajustado para o diretório correto
cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def carregar_robô_rag(area: str = "previdenciario", k: int = 4):
    caminho_indice = CAMINHO_INDICE  # Usa o diretório base, sem sufixo de área
    if not os.path.exists(caminho_indice):
        raise FileNotFoundError(f"Índice FAISS não encontrado em {caminho_indice}.")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    faiss_index = FAISS.load_local(caminho_indice, embeddings, allow_dangerous_deserialization=True)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-4",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        chain_type="stuff",
        retriever=faiss_index.as_retriever(search_type="similarity", search_kwargs={"k": k})
    )
    return qa_chain

async def responder_pergunta(pergunta: str, area: str = "previdenciario", k: int = 4) -> str:
    if not pergunta.strip():
        raise ValueError("Pergunta não pode ser vazia.")
    cache_key = f"rag:{pergunta}:{area}"
    async with cache as r:
        cached = await r.get(cache_key)
        if cached:
            return cached
    chain = carregar_robô_rag(area, k)
    resposta = chain.invoke(pergunta)
    resposta_str = resposta.get("result", str(resposta)) if isinstance(resposta, dict) else str(resposta)
    async with cache as r:
        await r.setex(cache_key, 3600, resposta_str)
    return resposta_str