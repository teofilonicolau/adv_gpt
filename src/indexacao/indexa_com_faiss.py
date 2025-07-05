import os
import csv
import smtplib
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# ⛽ Carregar variáveis do .env
load_dotenv()

CAMINHOS_FONTES = [
    r"C:\Users\Samsung\previnfobot-correto\dados\textos_limpos",
    r"C:\Users\Samsung\previnfobot-correto\dados\fontes_extra",
    r"C:\Users\Samsung\previnfobot-correto\dados\pdfs",
    r"C:\Users\Samsung\previnfobot-correto\dados\textos_base"  # 👈 adicionada
]

CAMINHO_INDICE = r"C:\Users\Samsung\previnfobot-correto\dados\vetores\faiss_index"
CAMINHO_LOG_CSV = r"C:\Users\Samsung\previnfobot-correto\relatorios\documentos_embutidos.csv"

def carregar_textos(caminhos):
    documentos = []
    log = []
    arquivos_lidos = set()

    for caminho in caminhos:
        if os.path.isdir(caminho):
            for nome in os.listdir(caminho):
                if nome.endswith(".txt") and nome not in arquivos_lidos:
                    try:
                        loader = TextLoader(os.path.join(caminho, nome), encoding="utf-8")
                        docs = loader.load()
                        documentos.extend(docs)
                        arquivos_lidos.add(nome)

                        tamanho_kb = round(os.path.getsize(os.path.join(caminho, nome)) / 1024, 2)
                        log.append([
                            nome,
                            caminho,
                            len(docs),
                            tamanho_kb,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ])
                    except Exception as e:
                        print(f"⚠️ Erro ao carregar {nome}: {e}")
    return documentos, log

def salvar_log_csv(dados):
    os.makedirs(os.path.dirname(CAMINHO_LOG_CSV), exist_ok=True)
    with open(CAMINHO_LOG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["arquivo", "caminho", "fragmentos", "tamanho_kb", "data_embuticao"])
        writer.writerows(dados)

def fragmentar_textos(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)

def indexar_em_lotes(docs_fragmentados, lote_tamanho=20):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    index_geral = None

    total_lotes = len(docs_fragmentados) // lote_tamanho + 1
    for i in range(0, len(docs_fragmentados), lote_tamanho):
        lote = docs_fragmentados[i:i + lote_tamanho]
        print(f"🔧 Processando lote {i // lote_tamanho + 1}/{total_lotes}")

        if not lote:
            print("⚠️ Lote vazio ignorado.")
            continue

        try:
            index_parcial = FAISS.from_documents(lote, embeddings)
            if index_parcial:
                if index_geral is None:
                    index_geral = index_parcial
                else:
                    index_geral.merge_from(index_parcial)
        except Exception as e:
            print(f"⚠️ Erro ao indexar lote: {e}")
            continue

    if index_geral:
        os.makedirs(CAMINHO_INDICE, exist_ok=True)
        index_geral.save_local(CAMINHO_INDICE)
    else:
        raise RuntimeError("❌ Nenhum índice criado. Verifique os dados ou conexão com a API.")

def enviar_email(resumo):
    remetente = os.getenv("EMAIL_ADDRESS")
    senha = os.getenv("EMAIL_PASSWORD")
    destino = os.getenv("EMAIL_ADDRESS")
    servidor = os.getenv("SMTP_SERVER")
    porta = int(os.getenv("SMTP_PORT"))

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destino
    msg["Subject"] = "✅ PrevInfoBot — Índice vetorial atualizado"

    corpo = f"""
    Olá Teófilo,

    O índice vetorial foi atualizado com sucesso.

    🗂️ Documentos embutidos: {resumo['documentos']}
    🧩 Fragmentos gerados: {resumo['fragmentos']}
    ⏱️ Tempo total: {resumo['duracao']} segundos

    🧠 Local do índice: {CAMINHO_INDICE}
    📄 Log salvo em: {CAMINHO_LOG_CSV}

    Atenciosamente,  
    PrevInfoBot
    """
    msg.attach(MIMEText(corpo, "plain"))

    try:
        with smtplib.SMTP(servidor, porta) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
            print("📧 Notificação enviada por e-mail!")
    except Exception as e:
        print(f"⚠️ Falha no envio do e-mail: {e}")

if __name__ == "__main__":
    t0 = time.time()
    print("📥 Carregando documentos...")
    docs, log_csv = carregar_textos(CAMINHOS_FONTES)

    print(f"📚 {len(docs)} documentos carregados.")
    salvar_log_csv(log_csv)

    print("✂️ Fragmentando documentos...")
    fragments = fragmentar_textos(docs)

    print(f"🔎 {len(fragments)} fragmentos gerados.")
    try:
        indexar_em_lotes(fragments)
        duracao = round(time.time() - t0, 2)

        resumo = {
            "documentos": len(docs),
            "fragmentos": len(fragments),
            "duracao": duracao
        }

        print(f"\n✅ Índice salvo com sucesso em {CAMINHO_INDICE}")
        print(f"🕒 Tempo total: {duracao} segundos")
        enviar_email(resumo)

    except Exception as e:
        print(f"❌ Erro durante a indexação: {e}")
