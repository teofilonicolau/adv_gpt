# src/gpt_utilidades/refinador_consulta_gpt.py

from src.agentes_juridicos.advogado_previdenciario import gerar_resposta_juridica

def gerar_parecer_personalizado(pergunta, base_previa=None):
    """
    Refina uma resposta existente ou gera uma análise jurídica aprofundada.

    Parameters:
    - pergunta: str → a pergunta ou consulta original
    - base_previa: str → resposta original (ex: vinda da base vetorial FAISS)

    Returns:
    - str: parecer jurídico gerado com profundidade, organização e fundamento legal
    """
    return gerar_resposta_juridica(
        pergunta=pergunta,
        contexto_adicional=base_previa,
        area="previdenciario"
    )
