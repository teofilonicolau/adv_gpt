import subprocess
import os
import time

PYTHON_BIN = os.path.join("venv", "Scripts", "python.exe")

def run_tarefa(caminho_script):
    try:
        subprocess.run([PYTHON_BIN, caminho_script], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # ignora falhas silenciosamente

if __name__ == "__main__":
    run_tarefa("scripts/verificador_de_duplicatas.py")
    run_tarefa("src/indexacao/indexa_com_faiss.py")
    run_tarefa("scripts/gera_relatorio_csv.py")
