import csv
import os
import requests
from datetime import datetime
# 🔹 Importação direta e correta para o seu ambiente
from config import LOG_CSV, DATA_PATH, BASE_DIR

def get_location_from_ip(ip):
    """Consulta a API externa e retorna cidade/estado a partir do IP."""
    try:
        if ip == "127.0.0.1":
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
    log_csv_path = os.path.join(BASE_DIR, DATA_PATH, LOG_CSV)
    os.makedirs(os.path.dirname(log_csv_path), exist_ok=True)

    local = get_location_from_ip(ip) if ip else "Desconhecido"

    registro = {
        "email": email,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip or "Desconhecido",
        "local": local,
    }

    write_header = not os.path.exists(log_csv_path)
    with open(log_csv_path, mode="a", newline="", encoding="utf-8") as f:
        fieldnames = ["email", "data_hora", "ip", "local"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        if write_header:
            writer.writeheader()
        writer.writerow(registro)
