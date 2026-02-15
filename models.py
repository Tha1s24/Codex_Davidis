from database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nivel_atual = db.Column(db.Integer, default=1)
    pontuacao = db.Column(db.Integer, default=0)
    tentativas = db.Column(db.Integer, default=5)

    def __init__(self, username, password):
        self.username = username
        self.password = password