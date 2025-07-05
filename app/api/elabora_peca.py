from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.documentos.elaborador_pecas import gerar_peticao

router = APIRouter()

class PeticaoRequest(BaseModel):
    nome_arquivo: str
    titulo: str
    qualificacao: str
    fatos: str
    fundamentos: str
    pedidos: List[str]
    local: str = "Icó/CE"

@router.post("/api/elabora_peca")
def elabora_peca(payload: PeticaoRequest):
    caminho, metodo_pdf = gerar_peticao(
        nome_arquivo=payload.nome_arquivo,
        titulo=payload.titulo,
        qualificacao=payload.qualificacao,
        fatos=payload.fatos,
        fundamentos=payload.fundamentos,
        pedidos=payload.pedidos,
        local=payload.local
    )

    return {
        "mensagem": "✅ Petição gerada com sucesso!",
        "arquivo_docx": caminho,
        "arquivo_pdf": caminho.replace(".docx", ".pdf"),
        "metodo_pdf": metodo_pdf  # <- agora o método usado (word, fallback ou erro) será retornado
    }
