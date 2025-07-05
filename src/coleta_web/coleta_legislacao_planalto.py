import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import hashlib
from datetime import datetime
import time

# 🔧 Configurações
PASTA_DESTINO = Path(__file__).resolve().parents[2] / "dados" / "textos_base"
LOG_CSV = Path(__file__).resolve().parents[2] / "relatorios" / "coleta_planalto.csv"
PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def limpar_texto(texto):
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n\s*\n", "\n", texto)
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    return "\n".join(linhas)

def gerar_hash(texto):
    return hashlib.md5(texto.encode("utf-8")).hexdigest()

def baixar_norma_planalto(url, nome_saida_base, max_tentativas=3):
    print(f"🌐 Acessando: {url}")
    tentativa = 1
    while tentativa <= max_tentativas:
        try:
            resposta = requests.get(url, headers=HEADERS, timeout=30)
            resposta.raise_for_status()
            soup = BeautifulSoup(resposta.text, "html.parser")
            texto = soup.get_text(separator="\n")
            texto_limpo = limpar_texto(texto)

            if len(texto_limpo.split()) < 100:
                print(f"⚠️ Texto muito curto, ignorado: {nome_saida_base}")
                return

            hash_conteudo = gerar_hash(texto_limpo)
            nome_saida = f"{nome_saida_base}.txt"
            caminho_saida = PASTA_DESTINO / nome_saida

            if caminho_saida.exists():
                with open(caminho_saida, "r", encoding="utf-8") as f:
                    hash_existente = gerar_hash(f.read())
                    if hash_existente == hash_conteudo:
                        print(f"⚠️ Já existe com mesmo conteúdo: {nome_saida}")
                        return

            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(texto_limpo)

            print(f"✅ Salvo: {nome_saida}")

            with open(LOG_CSV, "a", encoding="utf-8") as log:
                log.write(f"{nome_saida},{url},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            return

        except Exception as e:
            print(f"⚠️ Tentativa {tentativa} falhou: {e}")
            time.sleep(4)
            tentativa += 1

    print(f"❌ Não foi possível baixar após {max_tentativas} tentativas: {nome_saida_base}")

if __name__ == "__main__":
    normas = {
        "DECRETO_3048_1999": "https://www.planalto.gov.br/ccivil_03/decreto/D3048.htm",
        "EC_103_2019": "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc103.htm",
        "LEI_8213_1991": "https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm",
        "LEI_9876_1999": "https://www.planalto.gov.br/ccivil_03/leis/l9876.htm",
        "DECRETO_10410_2020": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/D10410.htm"
    }

    print("📥 Iniciando coleta das normas principais...\n")
    for nome, url in normas.items():
        baixar_norma_planalto(url, nome)
    print("\n📦 Coleta concluída.")
