from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from app.core.auth_combined import get_usuario_autenticado
import os
from pathlib import Path

router = APIRouter()
PASTA_LOGOS = Path("dados/logos_clientes")
PASTA_LOGOS.mkdir(parents=True, exist_ok=True)

@router.post("/upload_logo")
def upload_logo(
    id_escritorio: str = Form(...),
    arquivo: UploadFile = Form(...),
    usuario=Depends(get_usuario_autenticado)
):
    if not arquivo.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Formato inválido. Envie um .png ou .jpg.")

    nome_final = f"logo_{id_escritorio}.png"
    caminho_final = PASTA_LOGOS / nome_final

    with open(caminho_final, "wb") as f:
        f.write(arquivo.file.read())

    return {
        "mensagem": "Logo enviada com sucesso!",
        "caminho": str(caminho_final),
        "usuario": usuario["email"]
    }
