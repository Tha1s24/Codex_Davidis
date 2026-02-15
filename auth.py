from flask import Blueprint, request, jsonify
from database import db, bcrypt 
from models import Usuario
import re  # Essencial para a validação de segurança

auth_bp = Blueprint('auth', __name__)

def validar_senha(password):
    """
    Regra: Mínimo 6 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 especial.
    """
    regra = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
    return re.match(regra, password)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"erro": "Preencha todos os campos!"}), 400

        # Validação de Segurança da Senha
        if not validar_senha(password):
            return jsonify({
                "erro": "Senha fraca! Use no mínimo 6 caracteres, com maiúsculas, minúsculas, números e símbolos (@$!%*?&)."
            }), 400

        # Verifica se o usuário já existe
        if Usuario.query.filter_by(username=username).first():
            return jsonify({"erro": "Este escriba já existe!"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        novo_usuario = Usuario(
            username=username,
            password=hashed_password
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({"mensagem": "Escriba registrado com sucesso!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro interno ao processar cadastro"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        usuario = Usuario.query.filter_by(username=data['username']).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, data['password']):
            return jsonify({
                "mensagem": "Login realizado!",
                "id": usuario.id,
                "username": usuario.username,
                "nivel": usuario.nivel_atual
            }), 200
        
        return jsonify({"erro": "Usuário ou senha inválidos"}), 401
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor"}), 500