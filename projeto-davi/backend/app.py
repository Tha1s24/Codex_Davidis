import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

# Configuramos o Flask para reconhecer a pasta 'frontend' como local de arquivos estáticos
app = Flask(__name__, static_folder='frontend', static_url_path='')

# CORS ativado para evitar bloqueios de segurança
CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS (Ajuste para Vercel) ---
# No Vercel, o banco precisa ficar na pasta /tmp para ter permissão de escrita
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões e tabelas
init_db(app)

# Registro do Blueprint de Autenticação
app.register_blueprint(auth_bp)

# --- BANCO DE DADOS DE VERSÍCULOS ---
versiculos = {
    1: {"texto": "O SENHOR É MEU PASTOR", "ref": "Salmos 23:1"},
    2: {"texto": "A TI SENHOR LEVANTO A MINHA ALMA", "ref": "Salmos 25:1"},
    3: {"texto": "TODO SER QUE TEM FÔLEGO LOUVE AO SENHOR", "ref": "Salmos 150:6"},
    4: {"texto": "BEM-AVENTURADOS OS LIMPOS DE CORAÇÃO", "ref": "Mateus 5:8"},
    5: {"texto": "O MEU SOCORRO VEM DO SENHOR", "ref": "Salmos 121:2"}
}

# --- ROTAS DE NAVEGAÇÃO (Resolvendo o Erro 404) ---

@app.route('/')
def index():
    """Serve o arquivo index.html da pasta frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/game.html')
def game_page():
    """Serve o arquivo game.html da pasta frontend"""
    return send_from_directory('frontend', 'game.html')

@app.route('/<path:path>')
def serve_static(path):
    """Rota genérica para servir CSS, JS e imagens dentro de frontend"""
    return send_from_directory('frontend', path)

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

# Expondo o objeto para o Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)