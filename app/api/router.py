from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.rag import responder_pergunta
from app.api import auth
from app.api.upload_logo import router as upload_logo_router  # ✅ Novo import
from app.core.deps import get_current_user

router = APIRouter()
router.include_router(auth.router)
router.include_router(upload_logo_router, tags=["Upload de Logo"])  # ✅ Nova rota incluída

class ConsultaRequest(BaseModel):
    pergunta: str

@router.post("/consultar")
def consultar(req: ConsultaRequest, usuario=Depends(get_current_user)):
    resposta = responder_pergunta(req.pergunta)
    return {
        "usuario": usuario.email,
        "resposta": resposta
    }
