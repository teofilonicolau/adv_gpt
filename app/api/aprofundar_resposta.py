# app/api/aprofundar_resposta.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.gpt_utilidades.refinador_consulta_gpt import gerar_parecer_personalizado

router = APIRouter()

class RequisicaoAprofundar(BaseModel):
    pergunta: str
    resposta_faiss: str | None = None

@router.post("/api/aprofundar_resposta")
def aprofundar_resposta(payload: RequisicaoAprofundar):
    resposta_refinada = gerar_parecer_personalizado(
        pergunta=payload.pergunta,
        base_previa=payload.resposta_faiss
    )
    return {"resposta_aprofundada": resposta_refinada}
