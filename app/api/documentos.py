from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.auth_combined import get_usuario_autenticado
from app.models.documento import Documento

router = APIRouter(prefix="/documentos", tags=["Documentos"])

@router.get("/historico")
def listar_documentos(usuario=Depends(get_usuario_autenticado), db: Session = Depends(get_db)):
    docs = db.query(Documento).filter(Documento.usuario_id == usuario.get("id")).order_by(Documento.criado_em.desc()).all()
    return [
        {
            "id": doc.id,
            "nome": doc.nome_original,
            "tipo": doc.tipo,
            "caminho": doc.caminho_arquivo,
            "data_envio": doc.criado_em
        }
        for doc in docs
    ]
