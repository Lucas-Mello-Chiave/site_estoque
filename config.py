# config.py

import os

BASE_URL = "http://201.22.86.125:60000"

#BASE_URL = "http://201.22.86.125:60000"
FILIAL = 1

# --- CREDENCIAIS DA API ---
API_SENHA = "V7!xL9@qP#zR2$wM"
API_SERIE = "HIEAPA-605662-FWKD"

# --- CONFIGURAÇÃO DE CAMINHOS DE ARQUIVO ---
# Defina o caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# O caminho de dados agora inclui a pasta 'salva'
DATA_PATH = os.path.join("data")

# Arquivos que serão salvos dentro da pasta DATA_PATH
CSV_FILE = os.path.join(DATA_PATH, "database.csv")
AUTH_CSV = "auth.csv"
LAST_SYNC_FILE = "last_sync.txt"
LOG_CSV = "registro_acessos.csv"