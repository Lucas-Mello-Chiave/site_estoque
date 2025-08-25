import csv
from config import AUTH_CSV


def validate_user(email: str, password: str) -> bool:
    """
    Valida email e senha contra o arquivo CSV AUTH_CSV.
    Espera um CSV com cabeçalho; aceitável: 'email' e 'password' (delimitador ';').
    Comparação de email é case-insensitive; senha é comparada literal.
    """
    try:
        with open(AUTH_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                row_email = (row.get("email") or row.get("Email") or "").strip()
                row_password = (row.get("password") or row.get("Password") or "").strip()
                if row_email.lower() == email.lower() and row_password == password:
                    return True
    except FileNotFoundError:
        print(f"[auth_service] Arquivo de autenticação não encontrado: {AUTH_CSV}")
    except Exception as e:
        print(f"[auth_service] Erro ao validar usuário: {e}")

    return False
