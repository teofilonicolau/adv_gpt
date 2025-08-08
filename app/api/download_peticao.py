from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from app.core.auth_combined import get_usuario_autenticado
import os

router = APIRouter()

@router.get("/api/download_peticao")
def download_peticao(arquivo: str, usuario=Depends(get_usuario_autenticado)):
    caminho = os.path.abspath(os.path.join("dados", "peticoes_geradas", arquivo))
    
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(caminho, media_type='application/octet-stream', filename=arquivo)
