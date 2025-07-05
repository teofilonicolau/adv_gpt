import subprocess
import time
import os
import sys

# 🐍 Caminho para o Python da venv
PYTHON_BIN = os.path.join("venv", "Scripts", "python.exe")

def executar_etapa(comando, titulo):
    if not os.path.exists(PYTHON_BIN):
        print(f"❌ Ambiente virtual não encontrado em: {PYTHON_BIN}")
        sys.exit(1)

    comando[0] = PYTHON_BIN  # força uso do python da venv

    print(f"\n🎯 {titulo}")
    print("➤ Rodando:", " ".join(comando))
    inicio = time.time()

    try:
        resultado = subprocess.run(comando, check=True)
        duracao = round(time.time() - inicio, 2)
        print(f"✅ Concluído em {duracao} segundos")
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha ao executar {titulo}: {e}")
    except Exception as erro:
        print(f"⚠️ Erro inesperado: {erro}")

if __name__ == "__main__":
    print("🚀 Iniciando pipeline do PrevInfoBot...\n")

    # 🧼 Etapa 1: Verificação de duplicatas
    executar_etapa(["python", "scripts/verificador_de_duplicatas.py"], "Verificador de Duplicatas")

    # 🧠 Etapa 2: Indexação vetorial
    executar_etapa(["python", "src/indexacao/indexa_com_faiss.py"], "Indexação dos Documentos")

    # 📊 Etapa 3: Geração de relatório CSV
    executar_etapa(["python", "scripts/gera_relatorio_csv.py"], "Relatório de Métricas dos Arquivos")

    print("\n✅ Pipeline finalizada com sucesso!")
