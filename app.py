import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

# Agora o Flask olha diretamente para a raiz ('.') para buscar arquivos
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# O banco de dados será criado na mesma pasta do app.py
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco e rotas
init_db(app)
app.register_blueprint(auth_bp)

# --- BANCO DE DADOS DE VERSÍCULOS ---
versiculos = {
    1: {"texto": "O SENHOR É MEU PASTOR", "ref": "Salmos 23:1"},
    2: {"texto": "A TI SENHOR LEVANTO A MINHA ALMA", "ref": "Salmos 25:1"},
    3: {"texto": "TODO SER QUE TEM FÔLEGO LOUVE AO SENHOR", "ref": "Salmos 150:6"},
    4: {"texto": "BEM-AVENTURADOS OS LIMPOS DE CORAÇÃO", "ref": "Mateus 5:8"},
    5: {"texto": "O MEU SOCORRO VEM DO SENHOR", "ref": "Salmos 121:2"}
}

# --- ROTAS DE NAVEGAÇÃO (Agora lendo da raiz) ---

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/game.html')
def game_page():
    return send_from_directory(app.static_folder, 'game.html')

@app.route('/<path:path>')
def serve_static(path):
    # Esta rota serve automaticamente qualquer arquivo (css/style.css, js/script.js, etc)
    return send_from_directory(app.static_folder, path)

# --- ROTA DA API DO JOGO ---

@app.route('/get_desafio/<int:nivel>', methods=['GET'])
def get_desafio(nivel):
    if nivel > 5:
        return jsonify({"erro": "Vitoria Suprema!"}), 404
        
    v = versiculos.get(nivel)
    if v:
        try:
            codigo = criptografar_versiculo(v["texto"], nivel)
            return jsonify({
                "codigo": codigo,
                "referencia": v["ref"],
                "texto_original": v["texto"]
            }), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
            
    return jsonify({"erro": "Nivel nao encontrado"}), 404

# --- INICIALIZAÇÃO PARA DEPLOY ---

if __name__ == '__main__':
    # Importante para Render, Railway e outros: usar a porta da variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)