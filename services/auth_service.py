import csv
import os
# 🔹 Importação direta e correta para o seu ambiente
from config import AUTH_CSV, DATA_PATH, BASE_DIR

def validate_user(email: str, password: str) -> bool:
    """
    Valida email e senha contra o arquivo CSV AUTH_CSV.
    """
    auth_csv_path = os.path.join(BASE_DIR, DATA_PATH, AUTH_CSV)

    try:
        with open(auth_csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                row_email = (row.get("email") or row.get("Email") or "").strip()
                row_password = (row.get("password") or row.get("Password") or "").strip()
                if row_email.lower() == email.lower() and row_password == password:
                    return True
    except FileNotFoundError:
        print(f"[auth_service] Arquivo de autenticação não encontrado: {auth_csv_path}")
    except Exception as e:
        print(f"[auth_service] Erro ao validar usuário: {e}")

    return False
