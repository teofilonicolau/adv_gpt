from fastapi import APIRouter, UploadFile, Form, HTTPException
import os
from pathlib import Path

router = APIRouter()
PASTA_LOGOS = Path("dados/logos_clientes")
PASTA_LOGOS.mkdir(parents=True, exist_ok=True)

@router.post("/upload_logo")
def upload_logo(id_escritorio: str = Form(...), arquivo: UploadFile = Form(...)):
    """
    Recebe a logo (.png ou .jpg) de um escritório e salva localmente com nome vinculado ao id.
    Ex: logo_123.png para o escritório com id '123'
    """
    if not arquivo.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Formato inválido. Envie um .png ou .jpg.")

    nome_final = f"logo_{id_escritorio}.png"
    caminho_final = PASTA_LOGOS / nome_final

    with open(caminho_final, "wb") as f:
        f.write(arquivo.file.read())

    return {"mensagem": "Logo enviada com sucesso!", "caminho": str(caminho_final)}
