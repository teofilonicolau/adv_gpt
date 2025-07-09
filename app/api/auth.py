from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth import autenticar_usuario, criar_usuario
from app.core.security import criar_token
from app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, email, senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": criar_token(user.email), "token_type": "bearer"}

@router.post("/register")
def register(nome: str, email: str, senha: str, plano: str = "gratuito", db: Session = Depends(get_db)):
    return criar_usuario(db, nome, email, senha, plano)
