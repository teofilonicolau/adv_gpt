from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.rag import responder_pergunta
from app.api import auth
from app.core.deps import get_current_user  # ⬅️ novo import

router = APIRouter()
router.include_router(auth.router)

class ConsultaRequest(BaseModel):
    pergunta: str

@router.post("/consultar")
def consultar(req: ConsultaRequest, usuario=Depends(get_current_user)):
    resposta = responder_pergunta(req.pergunta)
    return {
        "usuario": usuario.email,
        "resposta": resposta
    }
