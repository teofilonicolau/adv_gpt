# app/main.py
from fastapi import FastAPI
from app.api import router, aprofundar_resposta, elabora_peca, download_peticao, pdf_final, upload

from app.core.db import engine
from app.models.usuario import Base
Base.metadata.create_all(bind=engine)  # ⬅️ Cria o banco na primeira execução

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
        {"name": "Autenticação", "description": "Login e registro de usuários"}
    ]
)

app.include_router(router.router, tags=["Consultas Jurídicas"])
app.include_router(aprofundar_resposta.router, tags=["Pareceres Aprofundados"])
app.include_router(elabora_peca.router, tags=["Geração de Petições"])
app.include_router(download_peticao.router)
app.include_router(pdf_final.router, tags=["Geração de PDF final"])
app.include_router(upload.router, tags=["Upload de Documentos"])
