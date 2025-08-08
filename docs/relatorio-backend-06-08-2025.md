# 🧠 Relatório Backend – 06/08/2025

## 🛠️ Tecnologias Utilizadas
- **Python 3.11+**
- **FastAPI** – framework web assíncrono
- **SQLAlchemy** – ORM para manipulação de banco de dados
- **firebase-admin** – SDK oficial para verificar tokens JWT do Firebase
- **Uvicorn** – servidor ASGI para rodar a API

## 📚 Bibliotecas Instaladas
```bash
pip install fastapi sqlalchemy firebase-admin uvicorn
```

## 🔐 Funcionalidades Implementadas
- **Autenticação com Firebase JWT**
  - Verificação de token enviado pelo frontend
  - Integração com `firebase_client.py` para validar usuários
- **Endpoints RESTful**
  - `POST /auth/login` – login tradicional com email/senha
  - `POST /auth/register` – criação de conta
  - `POST /auth/reset-password-request` – envio de link de redefinição
- **Proteção de rotas**
  - Uso de `Depends` para validar token JWT
- **Estrutura Modular**
  - `app/api/` – rotas e lógica de autenticação
  - `app/models/` – modelos SQLAlchemy
  - `app/database.py` – conexão com banco
  - `app/firebase_client.py` – integração com Firebase
