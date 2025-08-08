# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from app.api import (
    router,
    aprofundar_resposta,
    elabora_peca,
    download_peticao,
    pdf_final,
    upload,
    upload_logo,  # ✅ ADICIONE ESTA LINHA
    documentos
)
from app.core.db import engine
from app.models.usuario import Base
from app.models.documento import Documento

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="⚖️ Previnfobot API",
    description="Robô jurídico especializado em Direito Previdenciário...",
    version="1.0.0",
    contact={
        "name": "Time Previnfobot",
        "url": "https://github.com/teofilonicolau/adv_gpt.git",
        "email": "teofilonicolau157@gmail.com"
    },
    openapi_tags=[
        {"name": "Consultas Jurídicas", "description": "Consulta com IA jurídica"},
        {"name": "Pareceres Aprofundados", "description": "RAG + GPT"},
        {"name": "Geração de Petições", "description": "Automatização"},
        {"name": "Geração de PDF final", "description": "Download dos documentos"},
        {"name": "Upload de Documentos", "description": "Upload por escritório"},
        {"name": "Upload de Logo", "description": "Upload de logo do escritório"},  # ✅ NOVA TAG
        {"name": "Documentos", "description": "Histórico de documentos do usuário"},
        {"name": "Autenticação", "description": "Login e registro de usuários"}
    ]
)

# ✅ INICIALIZAÇÃO DO FASTAPI LIMITER
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 ROTAS
app.include_router(router.router, tags=["Consultas Jurídicas"])
app.include_router(aprofundar_resposta.router, tags=["Pareceres Aprofundados"])
app.include_router(elabora_peca.router, tags=["Geração de Petições"])
app.include_router(download_peticao.router)
app.include_router(pdf_final.router, tags=["Geração de PDF final"])
app.include_router(upload.router, tags=["Upload de Documentos"])
app.include_router(upload_logo.router, tags=["Upload de Logo"])  # ✅ ADICIONE ESTA LINHA
app.include_router(documentos.router, tags=["Documentos"])