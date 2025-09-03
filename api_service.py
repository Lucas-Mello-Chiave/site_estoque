# api_service.py

import hmac
import hashlib
import base64
import time
import requests
from config import BASE_URL, FILIAL, API_SENHA, API_SERIE

def generate_signature(method: str, timestamp: str, body_content: str = "") -> str:
    """Gera a assinatura de segurança para a requisição da API."""
    base64_body = base64.b64encode(body_content.encode('utf-8')).decode('utf-8') if body_content else ""
    raw_signature = f"{method.lower()}{timestamp}{base64_body}"
    hashed = hmac.new(API_SENHA.encode('utf-8'), raw_signature.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(hashed).decode('utf-8')

def get_api_auth_token() -> str | None:
    """Busca o token de autenticação da API."""
    endpoint = f"{BASE_URL}/auth/"
    timestamp = str(int(time.time()))
    signature = generate_signature('get', timestamp)

    headers = {
        "Signature": signature,
        "Timestamp": timestamp,
        "CodFilial": str(FILIAL),
    }
    params = {"serie": API_SERIE, "codfilial": FILIAL}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("sucesso"):
            return response_data.get("dados", {}).get("token")
        print(f"Falha na autenticação da API: {response_data.get('mensagem', 'Erro desconhecido')}")
    except Exception as e:
        print(f"Erro na autenticação da API: {e}")
    return None