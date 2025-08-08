import os
import sys
from dotenv import load_dotenv

load_dotenv()

def verificar_token(token_id):
    """Verifica token do Firebase com tratamento robusto de erros"""
    try:
        # Tenta importar firebase_admin
        import firebase_admin
        from firebase_admin import credentials, auth
        
        print("✅ Firebase Admin importado com sucesso!")
        
        # Inicializa Firebase se ainda não foi inicializado
        if not firebase_admin._apps:
            cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH", "firebase-service-account.json")
            
            # Verifica se o arquivo existe
            if not os.path.exists(cred_path):
                print(f"❌ Arquivo de credenciais não encontrado: {cred_path}")
                return None
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado com sucesso!")
        
        # Verifica o token
        decoded_token = auth.verify_id_token(token_id)
        print(f"✅ Token verificado para usuário: {decoded_token.get('email')}")
        return decoded_token
        
    except ImportError as e:
        print(f"❌ ERRO: Firebase Admin não pode ser importado: {e}")
        print(f"❌ Python path: {sys.path}")
        print(f"❌ Ambiente virtual ativo: {sys.prefix}")
        return None
    except FileNotFoundError as e:
        print(f"❌ Arquivo de credenciais não encontrado: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao verificar token Firebase: {e}")
        return None