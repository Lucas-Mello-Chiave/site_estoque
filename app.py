# app.py

from flask import Flask, render_template, jsonify, request
from services.product_service import get_products_from_csv
from services.auth_service import validate_user
from services.log_service import log_access
from services.estoque_service import sync_estoque
from config import AUTH_CSV, CSV_FILE, LOG_CSV

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/products")
def get_products():
    products = get_products_from_csv()
    return jsonify(products)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    if not email or not password:
        return jsonify({"success": False, "message": "Credenciais ausentes"}), 400
    
    if validate_user(email, password):
        user_ip = request.remote_addr
        log_access(email, user_ip)

        # 🔹 dispara a sincronização
        sync_ok = True
        try:
            sync_estoque()
        except Exception as e:
            print(f"Erro ao atualizar estoque: {e}")
            sync_ok = False

        # 🔹 retorna se sincronizou ou não
        return jsonify({"success": True, "sync_success": sync_ok})
    else:
        return jsonify({"success": False, "message": "Credenciais inválidas"}), 401


# --- Rotas de Gerenciamento (auth.csv) ---
@app.route("/get-auth-file")
def get_auth_file():
    try:
        with open(AUTH_CSV, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        return "Arquivo de autenticação não encontrado.", 404


@app.route("/save-auth-file", methods=["POST"])
def save_auth_file():
    data = request.get_json()
    if data is None or "content" not in data:
        return jsonify({"status": "error", "message": "Conteúdo ausente."}), 400
    try:
        with open(AUTH_CSV, "w", encoding="utf-8") as f:
            f.write(data["content"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao salvar o arquivo: {e}"}), 500


# --- Rotas de Edição de Produtos (database.csv) ---
@app.route("/get-database-file")
def get_database_file():
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        return "Arquivo de produtos não encontrado.", 404


@app.route("/save-database-file", methods=["POST"])
def save_database_file():
    data = request.get_json()
    if data is None or "content" not in data:
        return jsonify({"status": "error", "message": "Conteúdo ausente."}), 400
    try:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write(data["content"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao salvar o arquivo: {e}"}), 500


# --- NOVA ROTA de Visualização de Log (registro_acessos.csv) ---
@app.route("/get-access-log-file")
def get_access_log_file():
    """API para ler e retornar o conteúdo do arquivo registro_acessos.csv."""
    try:
        with open(LOG_CSV, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        # Se o arquivo ainda não foi criado (ninguém logou), retorna uma string vazia.
        return "", 200


if __name__ == "__main__":
    app.run(debug=True)