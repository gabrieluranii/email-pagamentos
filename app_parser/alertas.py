from datetime import datetime

def calcular_alerta(data_vencimento, dias_alerta=5):
    hoje = datetime.today().date()
    vencimento = datetime.strptime(data_vencimento, "%d/%m/%Y").date()

    dias_restantes = (vencimento - hoje).days

    if dias_restantes < 0:
        status = "VENCIDO"
    elif dias_restantes <= dias_alerta:
        status = "ALERTA"
    else:
        status = "OK"

    return status, dias_restantes
