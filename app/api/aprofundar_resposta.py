from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.gpt_utilidades.refinador_consulta_gpt import gerar_parecer_personalizado
from app.core.auth_combined import get_usuario_autenticado

router = APIRouter()

class RequisicaoAprofundar(BaseModel):
    pergunta: str
    resposta_faiss: str | None = None

@router.post("/api/aprofundar_resposta")
def aprofundar_resposta(payload: RequisicaoAprofundar, usuario=Depends(get_usuario_autenticado)):
    resposta_refinada = gerar_parecer_personalizado(
        pergunta=payload.pergunta,
        base_previa=payload.resposta_faiss
    )
    return {"resposta_aprofundada": resposta_refinada}
