"""
TAREFAS:
    * Validações mais robustas, principalmente de senha
"""

import re
from datetime import datetime, date

class UserPf: 
    def __init__(self, id, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro='', numero='', complemento=''): 

        if self.validacaoGeral(nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro, numero, complemento) == True: #Tive que especificar que é igual a True porque a função de validação geral sempre retornará algo (True ou lista de erros)
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

########### VALIDAÇÕES

    def validacaoGeral(self, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro='', numero='', complemento=''):
        validacoes = [
            (self.validarNome(nome), 'Nome inválido'), 
            (self.validarNascimento(nascimento), 'Nascimento inválido'),
            (self.validarCpf(cpf), 'CPF inválido'),
            (self.validarCelular(celular), 'Celular inválido'),
            (self.validarEmail(email), 'Email inválido'),
            (self.validarCep(cep), 'CEP inválido'),
            (self.validarTxt(bairro), 'Bairro inválido'),
            (self.validarTxt(estado), 'Estado inválido'),
            (self.validarTxt(cidade), 'Cidade inválido'),
            (self.validarSenha(senha), 'Senha inválida'),
            (self.verificarSenha(senha, verificador), 'As senhas não coincidem')
        ]

        if logradouro:
            validacoes.append((self.validarTxt(logradouro), 'Logradouro inválido'))
        if numero:
            validacoes.append((self.validarNum(numero), 'Número inválido'))
        if complemento:
            validacoes.append((self.validarTxt(complemento), 'Complemento inválido'))

        erros = []
        for validade, mensagem in validacoes:
            if not validade:
                erros.append(mensagem)

        if erros:
            raise ValueError(erros)
        return True
    
    def validarNome(self, nome):
        if not isinstance(nome, str) or len(nome.strip()) <= 5 or len(nome) >= 100:
            return False
        nome = nome.replace(' ', '')
        pattern = r'^[a-zA-ZÀ-ÿ]+$'
        return bool(re.match(pattern, nome.strip()))

    def validarCelular(self,cell):
        cell_limpo = ''.join(filter(str.isdecimal, str(cell)))
        return len(cell_limpo)==11 #contando DDD

    def validarEmail(self,email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validarNascimento(self, nascimento):
        try:
            data_nasc = datetime.strptime(nascimento, '%Y-%m-%d').date()
            hoje = date.today()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            return 18 <= idade <= 120  
        except ValueError:
            return False

    def validarCpf(self,cpf):
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
        if len(cpf_limpo) != 11:
            return False
        
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf_limpo[9]) != digito1:
            return False
        
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf_limpo[10]) == digito2
    
    def validarSenha(self,senha):
        return len(senha)>=8
    
    def validarCep(self,cep):
        cep_limpo = ''.join(filter(str.isdigit, str(cep)))
        return len(cep_limpo)==8 
    
    def validarTxt(self,texto): #verifica se há somente letras na entrada
        if not isinstance(texto, str) or not texto.strip():
            return False
        # Permite letras, espaços, hífens e acentos
        pattern = r'^[a-zA-ZÀ-ÿ\s\-]+$'
        return bool(re.match(pattern, texto.strip()))

    def validarNum(self,num):
        return num.strip().isdecimal()
    
    def verificarSenha(self, senha, verificador):  #Não posso usar self.senha por que a função é executada antes do obj 
        return senha == verificador                #ser instanciado, logo, self.senha ainda não existe

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


userTest = UserPf(1, 'teste da silva', '2000-10-12', '12345678909', '11923471103', 'teste@gmail.com', '12345678', 'teste Bairro', 'teste Estado', 'teste Cidade', '12345678', '12345678','teste logradouro', '2222', 'teste Complemento')
addUser(userTest)