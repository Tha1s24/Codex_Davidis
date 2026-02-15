import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

# Configuração para encontrar os arquivos HTML/CSS/JS
# Se seus arquivos estiverem na raiz ou em pastas específicas, ajustamos aqui:
app = Flask(__name__, static_folder='.', static_url_path='')

# Configuração de CORS: Permite que o frontend acesse a API
CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS (Correção para Vercel) ---
# No Vercel, o SQLite só consegue escrever na pasta /tmp
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa DB, Bcrypt e Tabelas
init_db(app)

# Registro das rotas de Autenticação
app.register_blueprint(auth_bp)

# --- BANCO DE DADOS DE VERSÍCULOS ---
versiculos = {
    1: {"texto": "O SENHOR É MEU PASTOR", "ref": "Salmos 23:1"},
    2: {"texto": "A TI SENHOR LEVANTO A MINHA ALMA", "ref": "Salmos 25:1"},
    3: {"texto": "TODO SER QUE TEM FÔLEGO LOUVE AO SENHOR", "ref": "Salmos 150:6"},
    4: {"texto": "BEM-AVENTURADOS OS LIMPOS DE CORAÇÃO", "ref": "Mateus 5:8"},
    5: {"texto": "O MEU SOCORRO VEM DO SENHOR", "ref": "Salmos 121:2"}
}

# --- ROTAS PARA SERVIR O FRONTEND (Evita o Erro 404) ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/game')
def game_page():
    return send_from_directory('.', 'game.html')

# --- ROTA DA API DO JOGO ---
@app.route('/get_desafio/<int:nivel>', methods=['GET'])
def get_desafio(nivel):
    if nivel > 5:
        return jsonify({"erro": "Vitória Suprema alcançada!"}), 404
        
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
            
    return jsonify({"erro": "Nível não encontrado!"}), 404

# Expondo o objeto app para o Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)