from controllers.validacoes import validacaoGeralPj
import re

class UserPj:
    def __init__(self, id, razaoSocial, nomeFantasia, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual='' ,cell='', complemento=''):

        if validacaoGeralPj(razaoSocial, nomeFantasia, cnpj, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual ,cell, complemento):
        #validação geral dos campos
            self._id = id
            self._razaoSocial = razaoSocial
            self._nomeFant = nomeFantasia
            self._cnpj = cnpj
            self._ramo = ramo
            self._tamanho = tamanho
            self._nomeRep = nomeRep
            self.__cpfRep = cpfRep
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

############################# VALIDAÇÕES - devem retornar true ou false

    @property
    def id(self):
        return self._id

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

USERSpj = []

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