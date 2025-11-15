from controllers.validacoes import validacaoGeralPj
from models.User import User

class UserPj(User):
    def __init__(self, id, perfil, razaoSocial, nomeFantasia, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual='' ,cell='', complemento=''):
        
        if validacaoGeralPj(razaoSocial, nomeFantasia, cnpj, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual ,cell, complemento):
            
            super().__init__(id, perfil)
            self._razaoSocial = razaoSocial
            self._nomeFant = nomeFantasia
            self._cnpj = cnpj
            self._ramo = ramo
            self._tamanho = tamanho
            self._nomeRep = nomeRep
            self._cpfRep = cpfRep
            self._cargoRep = cargoRep 
            self._phone = telefone
            self._emailCop = emailCop
            self._cep = cep
            self._logra = logradouro 
            self._numero = numero
            self._bairro = bairro 
            self._estado = estado 
            self._cidade = cidade 
            self.__senha = senha
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
    def email(self):
        return self._emailCop
    
    @property
    def telefone(self):
        return self._phone
    
    @property
    def senha(self):
        return self.__senha
    
    @property
    def nome(self):
        return self._nomeFant
    
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
    emailCop="contato@techsol.com.br",
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