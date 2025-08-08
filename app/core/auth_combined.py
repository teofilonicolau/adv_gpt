from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.usuario import Usuario
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "super-secreto-prevbot")
ALGORITHM = "HS256"

def verificar_token_firebase(token: str):
    """Verifica token do Firebase com tratamento de erro"""
    try:
        from app.api.firebase_client import verificar_token
        return verificar_token(token)
    except Exception as e:
        print(f"Erro ao verificar token Firebase: {e}")
        return None

def get_usuario_autenticado(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    token = authorization.replace("Bearer ", "")

    # Tenta validar com Firebase primeiro
    firebase_user = verificar_token_firebase(token)
    if firebase_user:
        return {
            "email": firebase_user.get("email"),
            "uid": firebase_user.get("uid"),
            "provider": "firebase"
        }

    # Tenta validar com JWT local
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return {
            "email": user.email,
            "id": user.id,
            "provider": "local"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")