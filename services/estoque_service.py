# estoque_service.py
import os
import json
import requests
import time
import datetime
from api_service import get_api_auth_token, generate_signature
from utils.file_manager import read_file, write_file
from .save_service import save_stock_data # ⬅️ IMPORTAÇÃO DA NOVA FUNÇÃO
from config import BASE_URL, FILIAL, LAST_SYNC_FILE, DATA_PATH

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAST_SYNC_FILE_PATH = os.path.join(BASE_DIR, LAST_SYNC_FILE)


def get_last_sync_date() -> str | None:
    """Lê a data da última sincronização (YYYYMMDD)."""
    try:
        value = read_file(LAST_SYNC_FILE_PATH)
        if value and len(value) == 8 and value.isdigit():
            return value.strip()
        print(f"⚠️ Valor inválido no arquivo de sincronização ({value}), ignorando.")
        return None
    except FileNotFoundError:
        print("📂 Nenhum arquivo de última sincronização encontrado. Será feita busca completa.")
        return None


def save_last_sync_date(sync_time: str):
    """Salva a data da sincronização atual (YYYYMMDD)."""
    os.makedirs(os.path.join(BASE_DIR, DATA_PATH), exist_ok=True)
    write_file(LAST_SYNC_FILE_PATH, sync_time)
    print(f"💾 Data de sincronização salva: {sync_time}")


def sync_estoque():
    """Busca o estoque atualizado da API e salva os dados nos arquivos."""
    if not (token := get_api_auth_token()):
        print("❌ Falha na autenticação. A execução será interrompida.")
        return False

    todos_dados = []
    last_sync = get_last_sync_date()
    data_ate = datetime.datetime.now().strftime("%Y%m%d")
    pagina = 1

    print("🚀 Iniciando busca de dados de estoque...")

    datade_fmt = None
    dataate_fmt = datetime.datetime.strptime(data_ate, "%Y%m%d").strftime("%Y-%m-%d")

    if last_sync:
        last_sync_date = datetime.datetime.strptime(last_sync, "%Y%m%d")
        datade = last_sync_date - datetime.timedelta(days=1)
        datade_fmt = datade.strftime("%Y-%m-%d")

    while True:
        endpoint = f"{BASE_URL}/v2/estoque/{pagina}"
        timestamp = str(int(time.time()))
        signature = generate_signature('get', timestamp)
        
        headers = {
            "Authorization": f"Token {token}",
            "CodFilial": str(FILIAL),
            "Timestamp": timestamp,
            "Signature": signature,
        }

        params = {}
        if datade_fmt:
            params["datade"] = datade_fmt
            params["dataate"] = dataate_fmt

        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=45)
            response.raise_for_status()
            data = response.json()

            if data.get("tipo") == "FIM_DE_PAGINA":
                print(f"⚠️ Fim da paginação na página {pagina}.")
                break

            if not data.get("dados"):
                print(f"⚠️ Página {pagina} sem dados, interrompendo.")
                break

            print(f"✅ Página {pagina} coletada ({len(data['dados'])} registros).")
            todos_dados.extend(data["dados"])
            pagina += 1
            time.sleep(0.2)

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de rede na página {pagina}: {e}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON na página {pagina}.")
            return False

    if todos_dados:
        # 🔹 Chama a nova função para salvar os dados
        save_stock_data(todos_dados)
        save_last_sync_date(data_ate)

    return True