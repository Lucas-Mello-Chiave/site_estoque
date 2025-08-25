# services/log_service.py

import csv
import os
from datetime import datetime
from config import LOG_CSV

def log_access(email: str):
    """
    Registra um acesso de login bem-sucedido em um arquivo CSV.
    Adiciona uma linha com o email do usuário e o timestamp do login.
    """
    try:
        # Pega a data e hora atual e formata como uma string legível
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Define os cabeçalhos do arquivo CSV
        headers = ['email', 'timestamp']
        
        # Verifica se o arquivo já existe para decidir se precisa escrever o cabeçalho
        file_exists = os.path.exists(LOG_CSV)
        
        # Abre o arquivo em modo 'append' (a), que adiciona novas linhas sem apagar as existentes
        with open(LOG_CSV, mode='a', newline='', encoding='utf-8') as f:
            # Usamos o mesmo delimitador ';' para manter a consistência
            writer = csv.writer(f, delimiter=';')
            
            # Se o arquivo não existia, escreve o cabeçalho antes de adicionar o primeiro registro
            if not file_exists:
                writer.writerow(headers)
            
            # Escreve a nova linha com o email e o timestamp do login
            writer.writerow([email, timestamp])
            
    except Exception as e:
        # Se algo der errado (ex: permissão de escrita), imprime um erro no console do servidor
        print(f"[Log Service] Erro ao registrar acesso para {email}: {e}")