# config.py

BASE_URL = "http://127.0.0.1:60500"
FILIAL = 1

DATA_PATH = "data"
CSV_FILE = f"{DATA_PATH}/database.csv"
LAST_SYNC_FILE = f"{DATA_PATH}/last_sync.txt"

# CSV com emails e senhas (formato: cabeçalho "email;password")
AUTH_CSV = f"{DATA_PATH}/auth.csv"

# NOVO: Arquivo para registrar os logins bem-sucedidos
LOG_CSV = f"{DATA_PATH}/registro_acessos.csv"