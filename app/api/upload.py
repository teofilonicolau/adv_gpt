from fastapi import APIRouter, UploadFile, File, Form, Depends
from pathlib import Path
from app.core.auth_combined import get_usuario_autenticado
from app.models.documento import Documento
from app.core.db import get_db
from sqlalchemy.orm import Session
import shutil

router = APIRouter()

@router.post("/upload_documento")
async def upload_documento(
    arquivo: UploadFile = File(...),
    usuario=Depends(get_usuario_autenticado),
    db: Session = Depends(get_db)
):
    caminho = Path(f"dados/clientes/{usuario.get('id', usuario.get('uid'))}/documentos")
    caminho.mkdir(parents=True, exist_ok=True)

    destino = caminho / arquivo.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    doc = Documento(
        nome_original=arquivo.filename,
        tipo=arquivo.content_type,
        caminho_arquivo=str(destino),
        usuario_id=usuario.get("id")  # se for Firebase, esse campo pode ser nulo
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "mensagem": f"Arquivo '{arquivo.filename}' salvo com sucesso!",
        "usuario": usuario["email"]
    }
