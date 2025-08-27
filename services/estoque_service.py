# estoque_service.py

import requests
import time
import datetime
from config import BASE_URL, FILIAL, LAST_SYNC_FILE
from utils.file_manager import read_file, write_file


def get_last_sync_date():
    """Lê a última data de sincronização"""
    return read_file(LAST_SYNC_FILE)


def save_last_sync_date():
    """Salva a data/hora atual como última sincronização"""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    write_file(LAST_SYNC_FILE, now)


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
            time.sleep(0.005)

        except Exception as e:
            print(f"Erro na sincronização: {e}")
            # 🔹 LEVANTA A EXCEÇÃO NOVAMENTE PARA QUE O app.py POSSA CAPTURÁ-LA
            raise e

    # Esta linha só será executada se a sincronização for bem-sucedida
    save_last_sync_date()
    return todos_dados