from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.auth import autenticar_usuario, criar_usuario
from app.core.security import criar_token, hash_senha
from app.core.db import get_db
from app.models.usuario import Usuario
from jose import jwt, JWTError
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import re

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Autenticação"])

SECRET_KEY_RESET = os.getenv("SECRET_KEY_RESET", "fallback-chave-super-secreta")

SMTP_USER = os.getenv("EMAIL_ADDRESS")
SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def validar_senha(senha: str) -> bool:
    return re.match(
        r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$",
        senha
    )

def enviar_email_reset(email: str, token: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise HTTPException(status_code=500, detail="Configurações de e-mail ausentes.")

    msg = MIMEText(
        f"Para redefinir sua senha, clique aqui: http://localhost:5173/reset-password?token={token}"
    )
    msg["Subject"] = "Redefinição de Senha - PrevInfoBot"
    msg["From"] = SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Falha ao enviar e-mail: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao enviar e-mail")

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    plano: str = "gratuito"

class ResetPasswordRequest(BaseModel):
    email: str

class ResetPassword(BaseModel):
    token: str
    nova_senha: str

@router.post("/login")
def login(req: UsuarioLogin, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, req.email, req.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": criar_token(user.email), "token_type": "bearer"}

@router.post("/register")
def register(req: UsuarioCreate, db: Session = Depends(get_db)):
    if not validar_senha(req.senha):
        raise HTTPException(
            status_code=422,
            detail="A senha deve ter no mínimo 8 caracteres, incluir 1 número, 1 letra maiúscula e 1 caractere especial (@$!%*?&#)."
        )

    # 🛡️ Verificação de duplicidade
    if db.query(Usuario).filter(Usuario.email == req.email).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    return criar_usuario(db, req.nome, req.email, req.senha, req.plano)

@router.post("/reset-password-request")
def reset_password_request(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    reset_token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY_RESET,
        algorithm="HS256"
    )

    enviar_email_reset(user.email, reset_token)
    return {"mensagem": "E-mail de redefinição enviado com sucesso!"}

@router.post("/reset-password")
async def reset_password(req: ResetPassword, db: Session = Depends(get_db)):
    if not validar_senha(req.nova_senha):
        raise HTTPException(
            status_code=422,
            detail="A nova senha deve ter no mínimo 8 caracteres, incluir 1 número, 1 letra maiúscula e 1 caractere especial (@$!%*?&#)."
        )

    try:
        payload = jwt.decode(req.token, SECRET_KEY_RESET, algorithms=["HS256"])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.senha_hash = hash_senha(req.nova_senha)
    db.commit()
    return {"msg": "Senha redefinida com sucesso"}
