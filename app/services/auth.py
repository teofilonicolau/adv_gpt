from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import hash_senha, verificar_senha, criar_token

def autenticar_usuario(db: Session, email: str, senha: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user and verificar_senha(senha, user.senha_hash):
        return user
    return None

def criar_usuario(db: Session, nome, email, senha, plano="gratuito"):
    user = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha),
        plano=plano,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
