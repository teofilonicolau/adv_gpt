import os
from docx import Document
from fpdf import FPDF

def converter_pdf_sem_word(caminho_docx):
    doc = Document(caminho_docx)
    caminho_pdf = caminho_docx.replace(".docx", ".pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            pdf.multi_cell(0, 10, text)
        else:
            pdf.ln(5)

    pdf.output(caminho_pdf)
