import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

# --- LÓGICA DE CAMINHOS PARA DEPLOY ---
# Descobre onde o app.py está localizado (dentro de /backend)
backend_dir = os.path.abspath(os.path.dirname(__file__))

# Define o caminho para a pasta frontend (volta um nível e entra em /frontend)
# Isso corrige o erro 'Not Found' no Render
frontend_dir = os.path.abspath(os.path.join(backend_dir, "..", "frontend"))

app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Cria o banco de dados dentro da pasta backend para persistência básica
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(backend_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados e as rotas de autenticação
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

# --- ROTAS DE NAVEGAÇÃO (Front-end) ---

@app.route('/')
def index():
    """Entrega o index.html da pasta frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/game.html')
def game_page():
    """Entrega o game.html da pasta frontend"""
    return send_from_directory(app.static_folder, 'game.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve arquivos CSS, JS e Imagens da pasta frontend"""
    return send_from_directory(app.static_folder, path)

# --- ROTA DA API DO JOGO ---

@app.route('/get_desafio/<int:nivel>', methods=['GET'])
def get_desafio(nivel):
    if nivel > 5:
        return jsonify({"erro": "Vitória Suprema!"}), 404
        
    v = versiculos.get(nivel)
    if v:
        try:
            # A lógica de criptografia usa o nível para mudar a dificuldade
            codigo = criptografar_versiculo(v["texto"], nivel)
            return jsonify({
                "codigo": codigo,
                "referencia": v["ref"],
                "texto_original": v["texto"]
            }), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
            
    return jsonify({"erro": "Nível não encontrado"}), 404

# --- INICIALIZAÇÃO DO SERVIDOR ---

if __name__ == '__main__':
    # O Render exige que o app rode na porta definida pela variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)