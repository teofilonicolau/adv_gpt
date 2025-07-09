# app/api/router.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import responder_pergunta
from app.api import auth  # ⬅️ Adicionado aqui

router = APIRouter()
router.include_router(auth.router)  # ⬅️ Rota de autenticação incluída

class ConsultaRequest(BaseModel):
    pergunta: str

@router.post("/consultar")
def consultar(req: ConsultaRequest):
    resposta = responder_pergunta(req.pergunta)
    return {"resposta": resposta}
