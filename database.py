from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instanciamos os objetos fora da função para que outros arquivos 
# (como models.py e auth.py) possam importá-los facilmente.
db = SQLAlchemy()
bcrypt = Bcrypt()

def init_db(app):
    """
    Inicializa o banco de dados e as extensões com a configuração do App.
    """
    db.init_app(app)
    bcrypt.init_app(app)
    
    # O app_context é essencial para que o SQLAlchemy saiba qual 
    # banco de dados usar no momento da criação das tabelas.
    with app.app_context():
        try:
            # Importamos o models aqui dentro para garantir que o SQLAlchemy
            # 'leia' as classes Usuario antes de criar as tabelas.
            import models 
            
            db.create_all()
            print("✅ Banco de dados inicializado e tabelas verificadas/criadas!")
        except Exception as e:
            print(f"❌ Erro ao inicializar o banco de dados: {e}")