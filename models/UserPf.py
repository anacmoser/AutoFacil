from controllers.validacoes import validacaoGeralPf

class UserPf: 
    def __init__(self, id, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro='', numero='', complemento=''): 

        if validacaoGeralPf(nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro, numero, complemento) == True: #Tive que especificar que é igual a True porque a função de validação geral sempre retornará algo (True ou lista de erros)
            self.__id = id
            self._nome = nome
            self.__nascimento = nascimento
            self.__cpf = cpf
            self.__celular = celular
            self.__email = email
            self._cep = cep
            self._logradouro = logradouro
            self._numero = numero
            self._complemento = complemento
            self._bairro = bairro
            self._estado = estado
            self._cidade = cidade
            self.__senha = senha

########### SETTERS

    def setUserSenha(self, novaSenha):     #setters específicos para dados sensíveis
        self.__senha = novaSenha
    
    def setUserNome(self, novoNome):
        self._nome = novoNome

    def setUserContato(self, **kwargs): #campo específico
        for chave, valor in kwargs.items():
            if chave == 'celular':
                if self.validarCelular(valor):
                    self.__celular = valor
            elif chave == 'email':
                if self.validarEmail(valor):
                    self.__email = valor
            else: 
                raise ValueError('Campo inválido')

    def setUserEndereco(self, **kwargs): #no endereço muda-se tudo, não um campo específico
        for chave, valor in kwargs.items():
            if chave == 'cep':
                if self.validarCep(valor):
                    self._cep = valor
            elif chave == 'bairro':
                if self.validarTxt(valor):
                    self._bairro = valor
            elif chave == 'cidade':
                if self.validarTxt(valor):
                    self._cidade = valor
            elif chave == 'estado':
                if self.validarTxt(valor):
                    self._estado = valor
            elif chave == 'logradouro':
                if self.validarTxt(valor):
                    self._logradouro = valor
            elif chave == 'numero':
                if self.validarNum(valor):
                    self._numero = valor
            elif chave == 'complemento':
                if self.validarTxt(valor):
                    self._complemento = valor
            else:
                raise ValueError('campo inexistente')

########### GETTERS

    @property
    def user(self):
        user = {'id': self.__id, 
                 'senha': self.__senha,
                 'endereco': {'cep': self._cep, 
                               'bairro': self._bairro, 
                               'estado': self._estado, 
                               'cidade': self._cidade, 
                               'logradouro': self._logradouro,
                               'numero': self._numero,
                               'complemento': self._complemento},
                  'contato': {'celular': self.__celular, 
                              'email': self.__email},
                  'dadosPessoais': {'nome': self._nome, 
                                     'nascimento': self.__nascimento, 
                                     'cpf': self.__cpf}}
        return user
    
    @property
    def senha(self):
        return self.__senha
    
    @property
    def cpf(self):
        return self.__cpf

    @property
    def email(self):
        return self.__email
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def id(self):
        return self.__id
    
    def getUserEndereco(self, campo=''): #Menos pythonico que o getattr, mas é mais seguro
        if campo:
            if campo in self.user['endereco']:
                return self.user['endereco'][campo]
            raise ValueError(f'Campo "{campo}" não existe no endereço')
        return self.user['endereco']
    
    def getUserContato(self, campo=''):
        if campo:
            if campo in self.user['contato']:
                return self.user['contato'][campo]
            raise ValueError(f'Campo {campo} não existe em contatos')
        return self.user['contato']
    
    def getUserDados(self, campo=''):
        if campo:
            if campo in self.user['dadosPessoais']:
                return self.user['dadosPessoais'][campo]
            raise ValueError(f'Campo {campo} não existe em dados pessoais')
        return self.user['dadosPessoais']

USERSpf = []
def addUser(novoUser): #novosser é um objeto da classe user
        erros = verificarDuplicidade(novoUser)
        
        if erros:
            return erros  # Ou retornar False/lista de erros
        
        USERSpf.append(novoUser)
        return True

def verificarDuplicidade(novoUser):
        erro = []
        for user in USERSpf:
            if user.cpf == novoUser.cpf:  
                erro.append('Este CPF já está em uso')
            if user.email == novoUser.email:
                erro.append('Este email já está em uso')
            if user.nome == novoUser.nome:
                erro.append('Este nome já está em uso')
        return erro

def delUser(cpf):
        for user in USERSpf:
            if user.cpf == cpf:
                USERSpf.remove(user)
                return True
        return False

def getUserByCpf(cpf):
        for user in USERSpf:
            if user.cpf == cpf:
                return user
        return None, 'Usuario não encontrado'

def getUserByEmail(email):
        for user in USERSpf:
            if user.email == email:
                return user
        return None, 'Usuário não encontrado'


userTest = UserPf(1, 'teste da silva', '2000-10-12', '12345678909', '11923471103', 'teste@gmail.com', '12345678', 'teste Bairro', 'teste Estado', 'teste Cidade', 'Senha123', 'Senha123','teste logradouro', '2222', 'teste Complemento')
addUser(userTest)