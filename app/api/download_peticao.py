# app/api/download_peticao.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/api/download_peticao")
def download_peticao(arquivo: str):
    """
    Endpoint para download de petições geradas.

    Parâmetros:
    - arquivo (str): nome do arquivo a ser baixado.

    Retorno:
    - FileResponse: arquivo solicitado, caso exista.
    - HTTP 404: se o arquivo não for encontrado.
    """
    caminho = os.path.abspath(os.path.join("dados", "peticoes_geradas", arquivo))
    
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(caminho, media_type='application/octet-stream', filename=arquivo)
