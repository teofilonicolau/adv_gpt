from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil

router = APIRouter()

@router.post("/upload_documento")
async def upload_documento(id_escritorio: str = Form(...), arquivo: UploadFile = File(...)):
    caminho = Path(f"dados/clientes/{id_escritorio}/documentos")
    caminho.mkdir(parents=True, exist_ok=True)
    destino = caminho / arquivo.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    return {"mensagem": f"Arquivo '{arquivo.filename}' salvo com sucesso!"}
