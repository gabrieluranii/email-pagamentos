import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app_parser.alertas import calcular_alerta
import app_parser.pdf_reader as pdf_reader
import app_parser.extrator as extrator
import csv

pasta = "uploads"
os.makedirs(pasta, exist_ok=True)

arquivo_csv = "data/pagamentos.csv"
os.makedirs("data", exist_ok=True)

cabecalho = ["arquivo", "valor", "vencimento", "cnpj", "status", "dias_restantes"]
novo_arquivo = not os.path.exists(arquivo_csv)

with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cabecalho, delimiter=';')

    if novo_arquivo:
        writer.writeheader()

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(pasta, arquivo)
            texto = pdf_reader.ler_pdf(caminho)
            dados = extrator.extrair_pagamento(texto)

            status, dias = calcular_alerta(dados["vencimento"])

            print(f"\n--- {arquivo} ---")
            print(dados)
            print(f"Status: {status} ({dias} dias)")

            writer.writerow({
                "arquivo": arquivo,
                "valor": dados["valor"],
                "vencimento": dados["vencimento"],
                "cnpj": dados["cnpj"],
                "status": status,
                "dias_restantes": dias
            })


