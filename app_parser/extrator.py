import re

def extrair_pagamento(texto):
    valor = re.search(r"R\$ ?[\d\.]+,\d{2}", texto)
    cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)

    # tenta data completa
    vencimento = re.search(r"\d{2}/\d{2}/\d{4}", texto)

    # fallback: dia + contexto "Vencimento"
    if not vencimento:
        vencimento = re.search(r"Vencimento.*?(\d{2}/)", texto, re.IGNORECASE | re.DOTALL)

    return {
        "valor": valor.group() if valor else None,
        "vencimento": vencimento.group(1) if vencimento and vencimento.lastindex else (vencimento.group() if vencimento else None),
        "cnpj": cnpj.group() if cnpj else None
    }
