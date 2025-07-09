import json
import os

def carregar_dados_escritorio(id_escritorio):
    caminho_arquivo = os.path.join("dados", "clientes", "clientes.json")
    with open(caminho_arquivo, encoding="utf-8") as f:
        dados = json.load(f)
    return dados.get(id_escritorio)
