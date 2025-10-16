class UserPj:
    def __init__(self, razaoSocial, nomeFantasia, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual='' ,cell='', complemento=''):

        #validação geral dos campos
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

############################# VALIDAÇÕES



def validarRS(self, razaoSocial):
    
        