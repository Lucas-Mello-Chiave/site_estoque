import csv
import os
import requests
from datetime import datetime
from config import LOG_CSV

def get_location_from_ip(ip):
    """Consulta a API externa e retorna cidade/estado a partir do IP."""
    try:
        if ip == "127.0.0.1":  # acesso local
            return "localhost"
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url, timeout=5)
        data = response.json()
        cidade = data.get("city", "Desconhecida")
        estado = data.get("region", "Desconhecido")
        return f"{cidade} - {estado}"
    except Exception:
        return "Localização não encontrada"

def log_access(email, ip=None):
    """Registra email, data/hora, IP e localização no CSV de acessos."""
    os.makedirs(os.path.dirname(LOG_CSV), exist_ok=True)

    # busca localização
    local = get_location_from_ip(ip) if ip else "Desconhecido"

    registro = {
        "email": email,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip or "Desconhecido",
        "local": local,
    }

    write_header = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=registro.keys(), delimiter=";")
        if write_header:
            writer.writeheader()
        writer.writerow(registro)
