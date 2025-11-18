from flask_sqlalchemy import SQLAlchemy
from models import db
import bcrypt

class UserPfDB(db.Model):
    __tablename__ = 'UserPf'

    Id_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(100), nullable=False)
    CNH = db.Column(db.String(20))
    CPF = db.Column(db.String(11), unique=True, nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Telefone = db.Column(db.String(15))
    Data_Nascimento = db.Column(db.Date, nullable=False)
    CEP = db.Column(db.String(20))
    Logradouro = db.Column(db.String(100))
    Numero = db.Column(db.String(10))
    Complemento = db.Column(db.String(50))
    Bairro = db.Column(db.String(50))
    Estado = db.Column(db.String(50))
    Cidade = db.Column(db.String(50))
    Senha = db.Column(db.String(255), nullable=False)
    img_perfil = db.Column(db.String(2048))

    def set_senha(self, senha_plana):
        self.Senha = bcrypt.hashpw(
            senha_plana.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def verificar_senha(self, senha_plana):
        return bcrypt.checkpw(
            senha_plana.encode('utf-8'),
            self.Senha.encode('utf-8')
        )