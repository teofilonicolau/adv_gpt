# app/main.py

from fastapi import FastAPI
from app.api import router
from app.api import aprofundar_resposta
from app.api import elabora_peca

# ⬇️ Adicione esta nova importação
from app.api import download_peticao

app = FastAPI(
    title="⚖️ Previnfobot API",
    description=(
        "Robô jurídico especializado em Direito Previdenciário, "
        "com integração RAG (GPT + vetores), "
        "pronto para consultas, petições e pareceres automatizados.\n\n"
        "Desenvolvido por Teófilo Nicolau, com arquitetura modular, "
        "boas práticas e visão de escalabilidade para múltiplos ramos do Direito."
    ),
    version="1.0.0",
    contact={
        "name": "Time Previnfobot",
        "url": "https://github.com/seuusuario/previnfobot-correto",  # ajuste se quiser
        "email": "contato@seudominio.com"
    },
    openapi_tags=[
        {
            "name": "Consultas Jurídicas",
            "description": "Consulta com inteligência artificial baseada em jurisprudência e normas indexadas"
        },
        {
            "name": "Pareceres Aprofundados",
            "description": "Geração de pareceres com análise jurídica aprofundada usando RAG"
        },
        {
            "name": "Geração de Petições",
            "description": "Criação automatizada de petições com base em dados fornecidos"
        }
    ]
)

app.include_router(router.router, tags=["Consultas Jurídicas"])
app.include_router(aprofundar_resposta.router, tags=["Pareceres Aprofundados"])
app.include_router(elabora_peca.router, tags=["Geração de Petições"])

# ⬇️ Inclua esta linha no final para ativar o novo endpoint
app.include_router(download_peticao.router)
