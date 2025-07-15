import os
from fastapi import APIRouter, Query
from src.documentos.gerador_pdf_formatado import gerar_pdf_formatado

router = APIRouter()

@router.post("/api/gerar_peticao_final_pdf")
def gerar_pdf_final(
    nome_arquivo: str = Query(..., description="Nome do arquivo .docx gerado anteriormente"),
    id_escritorio: str = Query(..., description="ID do escritório para buscar a logo personalizada"),
    nome_escritorio: str = "ADVOCACIA ADVOGPT",
    endereco_escritorio: str = "Rua X, nº 123 – Icó/CE",
    telefone_escritorio: str = "(88) 99999-0000"
):
    # Caminho do arquivo .docx gerado anteriormente
    caminho_docx = f"dados/peticoes_geradas/{nome_arquivo}"

    # Caminho da logo personalizada com fallback para logo padrão
    caminho_logo = f"dados/logos_clientes/logo_{id_escritorio}.png"
    if not os.path.exists(caminho_logo):
        caminho_logo = "dados/logos/logo_padrao.png"

    # Gera o PDF com cabeçalho personalizado
    caminho_pdf = gerar_pdf_formatado(
        caminho_docx,
        nome_logo=caminho_logo,
        incluir_rodape=True,
        nome_escritorio=nome_escritorio,
        endereco_escritorio=endereco_escritorio,
        telefone_escritorio=telefone_escritorio
    )

    return {
        "mensagem": "📄 PDF personalizado gerado com sucesso!",
        "arquivo_pdf": caminho_pdf
    }
