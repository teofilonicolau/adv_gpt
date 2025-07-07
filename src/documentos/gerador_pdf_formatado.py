from docx import Document
from fpdf import FPDF
import os
import unicodedata

def limpar_unicode(texto):
    # Normaliza acentos, remove caracteres fora do latin-1
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("latin-1", "ignore").decode("latin-1")
    return texto

def gerar_pdf_formatado(
    caminho_docx,
    nome_logo=None,
    incluir_rodape=True,
    nome_escritorio="ADVOCACIA ADVOGPT",
    endereco_escritorio="Rua X, nº 123 – Icó/CE",
    telefone_escritorio="(88) 99999-0000"
):
    doc = Document(caminho_docx)
    caminho_pdf = caminho_docx.replace(".docx", "_final.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cabeçalho com logo e dados
    if nome_logo and os.path.exists(nome_logo):
        try:
            pdf.image(nome_logo, x=10, y=8, w=25)
            pdf.set_xy(40, 10)
        except RuntimeError as e:
            print(f"⚠️ Logo inválido ou corrompido: {e}")
            pdf.set_xy(10, 10)
    else:
        pdf.set_xy(10, 10)

    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 5, limpar_unicode(
        f"{nome_escritorio}\n{endereco_escritorio}\nTel: {telefone_escritorio}"
    ), align="L")

    pdf.ln(10)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Corpo da petição
    pdf.set_font("Times", "", 12)
    for para in doc.paragraphs:
        txt = para.text.strip()
        if txt:
            pdf.multi_cell(0, 8, limpar_unicode(txt))
        else:
            pdf.ln(5)

    # Rodapé opcional
    if incluir_rodape:
        pdf.set_y(-25)
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(128)
        pdf.multi_cell(0, 5, limpar_unicode("PrevInfoBot • Documento gerado automaticamente por IA jurídica"))

    pdf.output(caminho_pdf)
    return caminho_pdf
