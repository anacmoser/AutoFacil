from controllers.validacoes import validacaoGeralPj
from models.User import User
from models import db
import bcrypt

class UserPjDB(db.Model):
    __tablename__ = 'UserPj'

    Id_Cliente = db.Column(db.Integer, primary_key=True)
    Razao_Social = db.Column(db.String(100))
    Nome_Fantasia = db.Column(db.String(100))
    CNPJ = db.Column(db.String(14), unique=True)
    Inscricao_Estadual = db.Column(db.String(20))
    Ramo = db.Column(db.String(100))
    Tamanho_da_Empresa = db.Column(db.String(50))
    Nome = db.Column(db.String(100))
    CPF = db.Column(db.String(11))
    Cargo = db.Column(db.String(50))
    Telefone_Comercial = db.Column(db.String(15))
    Celular = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    CEP = db.Column(db.String(20))
    Logradouro = db.Column(db.String(100)) 
    Numero = db.Column(db.String(10))
    Complemento = db.Column(db.String(50))
    Bairro = db.Column(db.String(50))
    Estado = db.Column(db.String(50))
    Cidade = db.Column(db.String(50))
    Senha = db.Column(db.String(255))

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

