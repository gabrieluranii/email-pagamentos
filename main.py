from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List
from pathlib import Path
import os
import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# ==============================
# IMPORTS LOCAIS
# ==============================
import app_parser.pdf_reader as pdf_reader
import app_parser.extrator as extrator
from app_parser.alertas import calcular_alerta

# ==============================
# BASE DIR (Railway safe)
# ==============================
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"
EXCEL_PATH = DATA_DIR / "pagamentos.xlsx"

UPLOAD_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ==============================
# APP
# ==============================
app = FastAPI(title="Leitor de Pagamentos PDF")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# FRONTEND
# ==============================
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ==============================
# HEALTHCHECK
# ==============================
@app.get("/health")
def health():
    return {"status": "ok"}

# ==============================
# UPLOAD E PROCESSAMENTO
# ==============================
@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    registros = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue

        caminho = UPLOAD_DIR / file.filename

        with open(caminho, "wb") as f:
            f.write(await file.read())

        texto = pdf_reader.ler_pdf(caminho)
        dados = extrator.extrair_pagamento(texto)

        status, dias = calcular_alerta(dados["vencimento"])

        registros.append({
            "Arquivo": file.filename,
            "Valor": dados["valor"],
            "Vencimento": dados["vencimento"],
            "CNPJ": dados["cnpj"],
            "Status": status,
            "Dias Restantes": dias
        })

    df = pd.DataFrame(registros)
    df.to_excel(EXCEL_PATH, index=False)

    # ==============================
    # APLICAR CORES
    # ==============================
    wb = load_workbook(EXCEL_PATH)
    ws = wb.active

    cores = {
        "OK": "C6EFCE",
        "ALERTA": "FFEB9C",
        "VENCIDO": "FFC7CE"
    }

    for row in range(2, ws.max_row + 1):
        status = ws[f"E{row}"].value
        cor = cores.get(status)

        if cor:
            fill = PatternFill(start_color=cor, end_color=cor, fill_type="solid")
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).fill = fill

    wb.save(EXCEL_PATH)

    return registros

# ==============================
# DOWNLOAD DO EXCEL
# ==============================
@app.get("/download-excel")
def download_excel():
    return FileResponse(
        path=EXCEL_PATH,
        filename="pagamentos.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
