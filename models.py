#1. Criação do objeto usuário, com campos validados
#2. Adiciona o objeto usuário em users

#Fail-fast: Fazer validação específica para a inicialização do obj
    #Criar métodos de validação e chamá-los no construtor e nos setters

#Verificar se o campo existe: Fazer isso no próprio app.py e no front

#nascimento

import re
from datetime import datetime, date

class User: #retornará campos inválidos
    def __init__(self, id, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro='', numero='', complemento=''):

        if self.validacaoGeral(nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro, numero, complemento):

            self.__id = id
            self.nome = nome
            self.__nascimento = nascimento
            self.__cpf = cpf
            self.__celular = celular
            self.__email = email
            self.cep = cep
            self.logradouro = logradouro
            self.numero = numero
            self.complemento = complemento
            self.bairro = bairro
            self.estado = estado
            self.cidade = cidade
            self.__senha = senha
        
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

        for validade, mensagem in validacoes:
            if not validade:
                raise ValueError(mensagem)
    
    def validarNome(self, nome):
        return (isinstance(nome, str) and len(nome.strip()) >= 5 and len(nome) <= 100)

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
            return 18 <= idade <= 120  # Exemplo: entre 13 e 120 anos
        except ValueError:
            return False

    def validarCpf(self,cpf):
        cpf_limpo = ''.join(filter(str.isdecimal, str(cpf))) #Verifica se é dígito, não se é int!
        return len(cpf_limpo) == 11 and cpf_limpo != cpf_limpo[0] * 11
    
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

        
    def setUserSenha(self, novaSenha):     #setters específicos para dados sensíveis
        self.__senha = novaSenha
    
    def setUserNome(self, novoNome):
        self.nome = novoNome

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
                    self.cep = valor
            elif chave == 'bairro':
                if self.validarTxt(valor):
                    self.bairro = valor
            elif chave == 'cidade':
                if self.validarTxt(valor):
                    self.cidade = valor
            elif chave == 'estado':
                if self.validarTxt(valor):
                    self.estado = valor
            elif chave == 'logradouro':
                if self.validarTxt(valor):
                    self.logradouro = valor
            elif chave == 'numero':
                if self.validarNum(valor):
                    self.numero = valor
            elif chave == 'complemento':
                if self.validarTxt(valor):
                    self.complemento = valor
            else:
                raise ValueError('campo inexistente')
        
    @property
    def user(self):
        user = {'id': self.__id, 
                 'senha': self.__senha,
                 'endereco': {'cep': self.cep, 
                               'bairro': self.bairro, 
                               'estado': self.estado, 
                               'cidade': self.cidade, 
                               'logradouro': self.logradouro,
                               'numero': self.numero,
                               'complemento': self.complemento},
                  'contato': {'celular': self.__celular, 
                              'email': self.__email},
                  'dadosPessoais': {'nome': self.nome, 
                                     'nascimento': self.__nascimento, 
                                     'cpf': self.__cpf}}
        return user
    
    @property
    def senha(self):
        return self.__senha
    
    
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
    
class Users: #retornará invalidade por duplicidade, return 'Usuário já existe', retornar como erro
    def __init__(self, users):
        self.users = users

    #função para verificar duplicidade ds email e cpf antes do adicionar

    def getUsers(self):
        return self.users

    def adicionar(self, novoUser): #novosser é um objeto da classe user
        erros = self.verificarDuplicidade(novoUser)
        
        if erros:
            raise ValueError(erros)  # Ou retornar False/lista de erros
        
        self.users.append(novoUser)
        return True
    
    def verificarDuplicidade(self, novoUser): #Verificar por nome também
        erro = []
        for user in self.users:
            if user.getUserDados('cpf') == novoUser.getUserDados('cpf'):
                erro.append('Este CPF já está em uso')
            if user.getUserContato('email') == novoUser.getUserContato('email'):
                erro.append('Este email já está em uso')
        return erro

    def excluir(self, cpf):
        for user in self.users:
            if user.getUserDados('cpf') == cpf:
                self.users.remove(user)
                return True
        return False

    def getUsers(self):
        return self.users
    
    def getUserByCpf(self, cpf):
        for user in self.users:
            if user.getUserDados('cpf') == cpf:
                return user
        return None, 'Usuario não encontrado'
    
    def getUserByEmail(self, email):
        for user in self.users:
            if user.getUserDados('email') == email:
                return user
        return None, 'Usuário não encontrado'
        
class Veiculo:
    def __init__(self, id, tipo, categoria, marca, modelo, transmissao, precoDiario, nome, imagem, nMalas, nPasageiros, nPortas, combustivel, status):
        self.id = id
        self.tipo = tipo
        self.categoria= categoria
        self.marca = marca
        self.modelo = modelo
        self.transmissao = transmissao
        self.precoDiario = precoDiario
        self.nome = nome
        self.img = imagem
        self.nMala = nMalas   
        self.nPassageiros = nPasageiros
        self.nPortas = nPortas
        self.combustivel = combustivel
        self.status = status  

        self.veiculo = {"id": self.id,
                        "tipo": self.tipo,
                        "categoria": self.categoria,
                        "marca": self.marca,
                        "modelo": self.modelo,
                        "transmissao": self.transmissao,
                        "precoDiario": self.precoDiario,
                        "nome": self.nome,
                        "imagem": self.img,
                        "nMalas": self.nMala,
                        "nPassageiros": self.nPassageiros,
                        "nPortas": self.nPortas,
                        "combustivel": self.combustivel,
                        "status": self.status}
        
        self.campos = ['id', 'tipo', 'categoria', 'marca', 'modelo', 'transmissao', 'precoDiario', 'nome', 'imagem', 'nMalas', 'nPassageiros', 'nPoetas', 'combustivel', 'status']

    def getVeiculo(self):
        return self.veiculo 

    def getVeiculoStt(self):
        return self.status
    
    def getVeiCampo(self, campo):
        if campo in self.campos:
            return getattr(self, campo)
    
    def setVeiAtt(self, campo, novoValor):
        if campo in self.campos:
            setattr(self, campo, novoValor)
    
class Veiculos:
    def __init__(self):
        self.veiculos = []

    def getVeiculos(self):
        return self.veiculos

    def adicionar(self, veiculo): #Como em users, veículo é um objeto da classe veiculo
        self.veiculos.append(veiculo)
    
    def remover(self, id):
        for veiculo in self.veiculos:
            if veiculo.id == id:
                self.veiculos.remove(veiculo)
            else:
                return 'Veículo não encontrado'

    def getVeiById(self, id):
        for veiculo in self.veiculos:
            if id == veiculo.id:
                return veiculo
        return 'Nenhum id correspondente'


           

    
    