from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from pydantic import BaseModel
from datetime import datetime
import csv
import os
from app.services.rag import responder_pergunta
from app.api import auth
from app.api.upload_logo import router as upload_logo_router
from app.core.deps import get_current_user

router = APIRouter()

router.include_router(auth.router)
router.include_router(upload_logo_router, tags=["Upload de Logo"])

@router.on_event("startup")
async def startup():
    redis_instance = redis.from_url("redis://localhost:6379")
    await FastAPILimiter.init(redis_instance)

class ConsultaRequest(BaseModel):
    pergunta: str
    area: str = "previdenciario"

class FeedbackRequest(BaseModel):
    pergunta: str
    resposta: str
    feedback: str

def log_consulta(pergunta: str, resposta: str, usuario: str):
    log_file = "relatorios/consultas_rag.csv"
    os.makedirs("relatorios", exist_ok=True)
    with open(log_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pergunta, resposta, usuario, datetime.now()])

@router.post("/consultar", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def consultar(req: ConsultaRequest, usuario=Depends(get_current_user)):
    try:
        if not req.pergunta.strip():
            raise ValueError("Pergunta não pode ser vazia.")
        resposta = await responder_pergunta(req.pergunta, area=req.area)  # Função agora é assíncrona
        resposta_str = resposta.get("result", str(resposta)) if isinstance(resposta, dict) else str(resposta)
        log_consulta(req.pergunta, resposta_str, usuario.email)
        return {
            "usuario": usuario.email,
            "resposta": resposta_str
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar consulta: {str(e)}")

@router.post("/feedback")
async def salvar_feedback(req: FeedbackRequest, usuario=Depends(get_current_user)):
    try:
        feedback_file = "relatorios/feedback_rag.csv"
        os.makedirs("relatorios", exist_ok=True)
        with open(feedback_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([req.pergunta, req.resposta, req.feedback, usuario.email, datetime.now()])
        return {"mensagem": "Feedback salvo com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar feedback: {str(e)}")