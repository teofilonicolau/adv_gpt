from fastapi import APIRouter, Depends, Header
from fastapi_limiter.depends import RateLimiter
from app.core.auth_combined import get_usuario_autenticado
from app.models.consulta import ConsultaRequest
from app.models.feedback import FeedbackRequest
from app.utils.logger import log_consulta
from datetime import datetime
import csv

router = APIRouter()

@router.post("/consultar", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def consultar(req: ConsultaRequest, usuario=Depends(get_usuario_autenticado)):
    resposta_str = "Resposta gerada aqui..."  # Substitua pela lógica real
    log_consulta(req.pergunta, resposta_str, usuario["email"])
    return {
        "usuario": usuario["email"],
        "resposta": resposta_str
    }

@router.post("/feedback")
async def salvar_feedback(req: FeedbackRequest, usuario=Depends(get_usuario_autenticado)):
    with open("dados/feedbacks.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([req.pergunta, req.resposta, req.feedback, usuario["email"], datetime.now()])
    return {"mensagem": "Feedback salvo com sucesso!"}
