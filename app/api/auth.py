from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth import autenticar_usuario, criar_usuario
from app.core.security import criar_token
from app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# ✅ Novo modelo Pydantic para o body do /register
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    plano: str = "gratuito"

# ✅ Modelo para o body do /login
class UsuarioLogin(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login(req: UsuarioLogin, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, req.email, req.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": criar_token(user.email), "token_type": "bearer"}

@router.post("/register")
def register(req: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, req.nome, req.email, req.senha, req.plano)
