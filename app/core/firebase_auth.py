from fastapi import Header, HTTPException
from app.api.firebase_client import verificar_token

def get_usuario_firebase(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    decoded = verificar_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return decoded
