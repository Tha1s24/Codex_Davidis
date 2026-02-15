import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

# Configuração: static_folder diz onde estão seus arquivos de frente (HTML/CSS/JS)
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Banco de dados na pasta temporária do Vercel
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
app.register_blueprint(auth_bp)

# --- ROTAS DE SERVIÇO ---

@app.route('/')
def index():
    # Entrega o index.html que está dentro de /frontend
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/game.html')
def game_page():
    # Entrega o game.html que está dentro de /frontend
    return send_from_directory(app.static_folder, 'game.html')

@app.route('/<path:path>')
def serve_static(path):
    # Se pedir qualquer outro arquivo (como css/style.css), busca na pasta frontend
    return send_from_directory(app.static_folder, path)

# --- API DO JOGO ---
versiculos = {
    1: {"texto": "O SENHOR É MEU PASTOR", "ref": "Salmos 23:1"},
    2: {"texto": "A TI SENHOR LEVANTO A MINHA ALMA", "ref": "Salmos 25:1"},
    3: {"texto": "TODO SER QUE TEM FÔLEGO LOUVE AO SENHOR", "ref": "Salmos 150:6"},
    4: {"texto": "BEM-AVENTURADOS OS LIMPOS DE CORAÇÃO", "ref": "Mateus 5:8"},
    5: {"texto": "O MEU SOCORRO VEM DO SENHOR", "ref": "Salmos 121:2"}
}

@app.route('/get_desafio/<int:nivel>', methods=['GET'])
def get_desafio(nivel):
    v = versiculos.get(nivel)
    if v:
        codigo = criptografar_versiculo(v["texto"], nivel)
        return jsonify({"codigo": codigo, "referencia": v["ref"], "texto_original": v["texto"]})
    return jsonify({"erro": "Nivel nao encontrado"}), 404

# Essencial para o Vercel localizar o app
app = app