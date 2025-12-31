import pdfplumber

def ler_pdf(caminho):
    texto_total = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto_total += pagina.extract_text() or ""
    return texto_total
