from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db, init_db
from auth import auth_bp
from cipher_logic import criptografar_versiculo

app = Flask(__name__)

# Configuração de CORS: Essencial para permitir que o Live Server (5500) acesse o Flask (5000)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configurações do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa as extensões (DB, Bcrypt e Tabelas)
init_db(app)

# Registro das rotas de Autenticação (Login/Cadastro)
app.register_blueprint(auth_bp)

# --- BANCO DE DADOS DE VERSÍCULOS (5 NÍVEIS COM ACENTUAÇÃO) ---
versiculos = {
    1: {"texto": "O SENHOR É MEU PASTOR", "ref": "Salmos 23:1"},
    2: {"texto": "A TI SENHOR LEVANTO A MINHA ALMA", "ref": "Salmos 25:1"},
    3: {"texto": "TODO SER QUE TEM FÔLEGO LOUVE AO SENHOR", "ref": "Salmos 150:6"},
    4: {"texto": "BEM-AVENTURADOS OS LIMPOS DE CORAÇÃO", "ref": "Mateus 5:8"},
    5: {"texto": "O MEU SOCORRO VEM DO SENHOR", "ref": "Salmos 121:2"}
}

@app.route('/get_desafio/<int:nivel>', methods=['GET'])
def get_desafio(nivel):
    """
    Retorna o desafio criptografado para o nível solicitado.
    """
    v = versiculos.get(nivel)
    
    if v:
        try:
            # A função de criptografia recebe o texto acentuado. 
            # Dica: No cipher_logic.py, você pode remover os acentos antes de gerar os números 
            # para manter a simplicidade do jogo, mas o frontend exibirá a referência correta.
            codigo = criptografar_versiculo(v["texto"], nivel)
            
            return jsonify({
                "codigo": codigo,
                "referencia": v["ref"],
                "texto_original": v["texto"]
            }), 200
        except Exception as e:
            return jsonify({"erro": f"Erro na criptografia: {str(e)}"}), 500
            
    return jsonify({"erro": "Nível não encontrado no Reino!"}), 404

# Rota de teste para verificar se o servidor está online
@app.route('/')
def home():
    return jsonify({"status": "Servidor do Reino de Davi está online!"}), 200

if __name__ == '__main__':
    # Rodando em 0.0.0.0 para garantir visibilidade na rede local se necessário
    app.run(debug=True, host='0.0.0.0', port=5000)