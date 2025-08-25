import requests
import time
import datetime
import os

BASE_URL = "http://127.0.0.1:60500"
FILIAL = 1
LAST_SYNC_FILE = "last_sync.txt"

def get_last_sync_date():
    """Retorna a data/hora da última sincronização salva ou None se não existir"""
    if os.path.exists(LAST_SYNC_FILE):
        with open(LAST_SYNC_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_sync_date():
    """Salva a data/hora atual no arquivo de controle"""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(LAST_SYNC_FILE, "w") as f:
        f.write(now)

def sync_estoque():
    """Busca o estoque atualizado da API com paginação"""
    ultima_execucao = get_last_sync_date()
    data_de = ultima_execucao if ultima_execucao else None
    data_ate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    pagina = 1
    todos_dados = []

    while True:
        if data_de:
            endpoint = f"{BASE_URL}/v2/estoque/{pagina}?&codfilial={FILIAL}&datade={data_de}&dataate={data_ate}"
        else:
            endpoint = f"{BASE_URL}/v2/estoque/{pagina}?&codfilial={FILIAL}"

        try:
            response = requests.get(endpoint, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("tipo") == "FIM_DE_PAGINA" or not data.get("dados"):
                break

            todos_dados.extend(data.get("dados", []))
            pagina += 1
            time.sleep(0.005)  # evita flood no servidor

        except Exception:
            break

    save_last_sync_date()
    return todos_dados
