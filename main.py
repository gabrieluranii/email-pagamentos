from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List
from pathlib import Path
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
# DIRETÓRIOS BASE
# ==============================
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
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
# FRONTEND (static + templates)
# ==============================
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

templates = Jinja2Templates(directory=FRONTEND_DIR)

@app.get("/", response_class=HTMLRespons_
