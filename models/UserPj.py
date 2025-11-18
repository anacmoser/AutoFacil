from controllers.validacoes import validacaoGeralPj
from models.User import User
from models import db
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
    Email_Corporativo = db.Column(db.String(100))
    CEP = db.Column(db.String(20))
    Logradouro = db.Column(db.String(100))
    Numero = db.Column(db.String(10))
    Complemento = db.Column(db.String(50))
    Bairro = db.Column(db.String(50))
    Estado = db.Column(db.String(50))
    Cidade = db.Column(db.String(50))
    Senha = db.Column(db.String(255))

class UserPj(User):
    def __init__(self, id, perfil, razaoSocial, nomeFantasia, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, telefone, email, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual='' ,cell='', complemento=''):
        
        if validacaoGeralPj(razaoSocial, nomeFantasia, cnpj, nomeRep, cpfRep, cargoRep, telefone, email, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual ,cell, complemento):
            
            super().__init__(id, perfil, senha, email)
            self._razaoSocial = razaoSocial
            self._nomeFant = nomeFantasia
            self._cnpj = cnpj
            self._ramo = ramo
            self._tamanho = tamanho
            self._nomeRep = nomeRep
            self._cpfRep = cpfRep
            self._cargoRep = cargoRep 
            self._phone = telefone
            self._cep = cep
            self._logra = logradouro 
            self._numero = numero
            self._bairro = bairro 
            self._estado = estado 
            self._cidade = cidade 
            self._inscricaoEstadual = inscricaoEstadual
            self._cell = cell
            self._complemento = complemento 

    @property
    def cnpj(self):
        return self._cnpj
    
    @property
    def rs(self):
        return self._razaoSocial

    @property
    def nomeRep(self):
        return self._nomeRep
    
    @property
    def telefone(self):
        return self._phone
        return self.__senha
    
    @property
    def nome(self):
        return self._nomeFant
    
    @property
    def cargo(self):
        return self._ramo
    
    @property
    def tamanho(self):
        return self._tamanho
    
    @property
    def representante(self):
        return self._nomeRep
    
    @property
    def ramo(self):
        return self._ramo
    
    @property
    def tell(self):
        return self._phone
    
    def setAttr(self, campo, valor):
        if hasattr(self, campo):
            setattr(self, campo, valor)
        else:
            raise ValueError(f'{campo} Atributo não existe') 
    
    
empresa1 = UserPj(
    id=1,
    perfil='pj',
    razaoSocial="Tech Solutions LTDA",
    nomeFantasia="TechSol",
    cnpj="04252011000110",
    ramo="Tecnologia da Informação",
    tamanho="Médio Porte",
    nomeRep="João da Silva",
    cpfRep="12345678909",
    cargoRep="Diretor Executivo",
    telefone="1140028922",
    email="contato@techsol.com.br",
    cep="04567-000",
    logradouro="Rua das Inovações",
    numero="123",
    bairro="Centro Empresarial",
    estado="SP",
    cidade="São Paulo",
    senha="senhaSegura123",
    confirmar="senhaSegura123",
    inscricaoEstadual="123456789",
    cell="11988887777",
    complemento="Sala 45"
)

USERSpj = [empresa1]

def addUserPj(novoUser): #Adicionar a verificação de duplicidade
    erros = verificarDuplicidadePj(novoUser)
    if erros:
        return erros
    USERSpj.append(novoUser)
    return True
    
def verificarDuplicidadePj(novoUser):
    erro = []
    for user in USERSpj:
        if user.cnpj == novoUser.cnpj:
            erro.append('Este CNPJ já está em uso') 
        if user.email == novoUser.email:
            erro.append('Este email já está em uso')
        if user.rs == novoUser.rs:
            erro.append('Esta Razão Social já está em uso')
        if user.telefone == novoUser.telefone:
            erro.append('Este telefone já está em uso')
    return erro

def buscarUser(id):
    for user in USERSpj:
        if user.id == id:
            return user
    return False