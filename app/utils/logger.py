import csv
import os
from datetime import datetime

def log_consulta(pergunta: str, resposta: str, usuario: str):
    log_file = "relatorios/consultas_rag.csv"
    os.makedirs("relatorios", exist_ok=True)
    with open(log_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pergunta, resposta, usuario, datetime.now()])
