import csv
from config import CSV_FILE
import os
from config import CSV_FILE, BASE_DIR
def get_products_from_csv():
    products = []
    # Use o caminho absoluto combinando BASE_DIR com CSV_FILE
    csv_path = os.path.join(BASE_DIR, CSV_FILE)
    
    try:
        with open(csv_path, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=";")

            for row in csv_reader:
                # Valida ID
                id_val = row.get("Id", "").strip()
                if not id_val or id_val.upper() == "N/A":
                    continue

                # Converte estoque
                estoque_val = row.get("ESTOQUE", "").strip()
                try:
                    row["ESTOQUE"] = int(float(estoque_val)) if estoque_val else 0
                except (ValueError, TypeError):
                    row["ESTOQUE"] = 0

                products.append(row)

    except FileNotFoundError:
        print(f"Erro: O arquivo {CSV_FILE} não foi encontrado.")
        return []

    return products
