import os
import hashlib
from pathlib import Path
import shutil
import csv
from datetime import datetime

# 🔧 Configuração das pastas
PASTAS_ANALISAR = [
    "dados/textos_limpos",
    "dados/textos_base",
    "dados/fontes_extra",
    "dados/pdfs"
]
PASTA_REPETIDOS = "dados/textos_repetidos"
os.makedirs(PASTA_REPETIDOS, exist_ok=True)

# 📄 Caminho do relatório
RELATORIO_CSV = "relatorios/duplicatas_detectadas.csv"
os.makedirs("relatorios", exist_ok=True)

def gerar_hash(caminho):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()
    return hashlib.md5(conteudo.encode("utf-8")).hexdigest()

def main():
    print("🔎 Verificando duplicatas...")
    arquivos_hash = {}
    duplicatas = []

    for pasta in PASTAS_ANALISAR:
        for raiz, _, arquivos in os.walk(pasta):
            for nome in arquivos:
                if nome.endswith(".txt"):
                    caminho = os.path.join(raiz, nome)
                    try:
                        hash_arquivo = gerar_hash(caminho)
                    except Exception as e:
                        print(f"⚠️ Erro ao processar {caminho}: {e}")
                        continue

                    if hash_arquivo in arquivos_hash:
                        destino = os.path.join(PASTA_REPETIDOS, nome)
                        shutil.move(caminho, destino)
                        duplicatas.append([nome, caminho, destino, hash_arquivo, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                        print(f"🗑️  Duplicado movido: {nome}")
                    else:
                        arquivos_hash[hash_arquivo] = caminho

    # Gerar CSV
    with open(RELATORIO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["arquivo", "original", "movido_para", "hash", "data"])
        writer.writerows(duplicatas)

    print(f"\n✅ {len(duplicatas)} duplicatas detectadas e movidas.")
    print(f"📁 Relatório: {RELATORIO_CSV}")

if __name__ == "__main__":
    main()
