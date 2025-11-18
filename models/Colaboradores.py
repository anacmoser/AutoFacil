from controllers.validacoes import validacaoGeralColab
from controllers.validacoes import validarNome, validarEmail, validarSenha, validarCpf
from models import db
class ColaboradorDB(db.Model):
    __tablename__ = 'Colaborador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(20), default='colab')
    cargo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    
