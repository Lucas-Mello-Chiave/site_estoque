# services/save_service.py
import os
import json
import csv
from config import DATA_PATH, CSV_FILE, BASE_DIR 

# --- CONFIGURAÇÃO DE CAMINHOS ---
DATA_DIRECTORY = os.path.join(BASE_DIR, DATA_PATH)
PRODUCTS_CSV_PATH = os.path.join(BASE_DIR, CSV_FILE)
OUTPUT_INCREMENTAL = os.path.join(DATA_DIRECTORY, 'dados_de_estoque_incremental.json')
OUTPUT_COMPILADO = os.path.join(DATA_DIRECTORY, 'dados_de_estoque_compilado.json')



def merge_stock_json(existing: dict, new_data: list) -> dict:
    """Atualiza o dicionário 'existing' com os novos registros da API."""
    for item in new_data:
        codigo = item.get('codigo') or item.get('codigoProduto')
        if not codigo:
            continue
        existing[codigo] = item
    return existing

def update_csv_with_stock(new_stock_data: list):
    """Atualiza a coluna ESTOQUE no CSV existente com base nos novos dados."""
    
    # 1. Carrega o conteúdo do CSV atual
    existing_products = []
    if os.path.exists(PRODUCTS_CSV_PATH):
        with open(PRODUCTS_CSV_PATH, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                existing_products.append(row)

    # 2. Cria um mapa de estoque a partir do JSON
    new_stock_map = {}
    for item in new_stock_data:
        codigo = str(item.get("codigo"))
        if not codigo:
            continue

        estoque_atual = 0
        # 🔹 Se veio no formato novo (estoqueFiliais)
        if "estoqueFiliais" in item:
            for filial in item["estoqueFiliais"]:
                if filial.get("codigoFilial") == 1:  # sua filial configurada
                    estoque_atual = filial.get("estoqueAtual", 0)
                    break
        else:
            # 🔹 Caso ainda venha no formato antigo (qtdestoque)
            estoque_atual = item.get("qtdestoque", 0)

        new_stock_map[codigo] = estoque_atual

    # 3. Atualiza os produtos do CSV
    updated_products = []
    for product in existing_products:
        product_id = product.get("Id", "").strip()
        if product_id in new_stock_map:
            product["ESTOQUE"] = new_stock_map[product_id]
        updated_products.append(product)

    # 4. Salva o CSV atualizado
    if updated_products:
        with open(PRODUCTS_CSV_PATH, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = updated_products[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(updated_products)
        print(f"📦 {len(updated_products)} produtos atualizados no arquivo CSV.")



def save_stock_data(todos_dados: list):
    """Salva os dados de estoque em arquivos JSON e atualiza o CSV."""
    if not todos_dados:
        print("ℹ️ Nenhum dado para salvar.")
        return

    os.makedirs(DATA_DIRECTORY, exist_ok=True)

    # Salva o arquivo incremental
    with open(OUTPUT_INCREMENTAL, 'w', encoding='utf-8') as f:
        json.dump(todos_dados, f, ensure_ascii=False, indent=4)
    print(f"📄 Arquivo incremental salvo: {OUTPUT_INCREMENTAL}")

    # Carrega e atualiza o arquivo compilado
    if os.path.exists(OUTPUT_COMPILADO):
        try:
            with open(OUTPUT_COMPILADO, 'r', encoding='utf-8') as f:
                compilado_dict = {str(item.get('codigo')): item
                                  for item in json.load(f)}
        except (json.JSONDecodeError, FileNotFoundError):
            compilado_dict = {}
    else:
        compilado_dict = {}

    compilado_dict = merge_stock_json(compilado_dict, todos_dados)
    dados_compilados = list(compilado_dict.values())

    with open(OUTPUT_COMPILADO, 'w', encoding='utf-8') as f:
        json.dump(dados_compilados, f, ensure_ascii=False, indent=4)
    print(f"📦 Compilado atualizado com {len(todos_dados)} registros novos. Total: {len(dados_compilados)}")

    # Atualiza o arquivo CSV
    update_csv_with_stock(todos_dados)