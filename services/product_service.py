import csv
from config import CSV_FILE


def get_products_from_csv():
    """Lê o arquivo CSV e retorna uma lista de produtos"""
    products = []
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as csv_file:
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
