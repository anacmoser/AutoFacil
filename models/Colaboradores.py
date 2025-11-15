from controllers.validacoes import validacaoGeralColab
from controllers.validacoes import validarNome, validarEmail, validarSenha, validarCpf

class Colaborador:
    def __init__(self, id, nome, cargo, email, senha, verificador, cpf):
        if validacaoGeralColab(nome, senha, verificador, cpf, email):
            self._id = id
            self._nome = nome
            self._perfil = 'colab'
            self._cargo = cargo
            self._email = email
            self._senha = senha
            self._cpf = cpf

    @property
    def id(self):
        return self._id
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def perfil(self):
        return self._perfil
    
    @property
    def cargo(self):
        return self._cargo
    
    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha    
    
    @property
    def cpf(self): 
        return self._cpf    

    def updateAttr(self, campo, valor):
        setattr(self, campo, valor)
        
admin = Colaborador(1, 'Enzooo', 'admin', 'admin@gmail.com', 'Senha123', 'Senha123', '12345678909')
gerente = Colaborador(2, 'Melissa', 'gerente', 'gerente@gmail.com', 'Senha123', 'Senha123', '52998224725')
atendente = Colaborador(3, 'Ryukiii', 'atendente', 'atendente@gmail.com', 'Senha123', 'Senha123', '98765432100')
suporte = Colaborador(4, 'Nathalia', 'suporte', 'suporte@gmail.com', 'Senha123', 'Senha123', '12345678909')



Lista_Colaboradores = [admin, gerente, atendente, suporte]

def adicionarColab(novoColab):
    erros = verificarDuplicidadePj(novoColab)
    if erros:
        return erros
    Lista_Colaboradores.append(novoColab)
    return True
    
def verificarDuplicidadePj(novoColab):
    erro = []
    for colab in Lista_Colaboradores:
        if colab.cpf == novoColab.cpf:
            erro.append('Este CPF já está em uso') 
        if colab.email == novoColab.email:
            erro.append('Este email já está em uso')
        if colab.nome == novoColab.nome:
            erro.append('Este nome já está em uso')
    return erro
    
def updateColab(cpf, campo, novoValor): #Verificar se o attr existe e validar o novo valor
    for colab in Lista_Colaboradores:
        if colab.cpf == cpf:
            match campo:
                case 'nome':
                    if validarNome(novoValor):
                        for colaborador in Lista_Colaboradores:
                            if colaborador.nome == novoValor:
                                return 'Este nome já está em uso'
                        colab.updateAttr(campo, novoValor)
                        return True
                    return 'Nome inválido'
                case 'email':
                    if validarEmail(novoValor):
                        for colaborador in Lista_Colaboradores:
                                if colaborador.email == novoValor:
                                    return 'Este email já está em uso'
                        colab.updateAttr(campo, novoValor)
                        return True
                    return 'Email inválido'
                case 'cargo':
                    if novoValor == 'atendente' or novoValor == 'admin' or novoValor == 'gerente' or novoValor == 'suporte':
                        colab.updateAttr(campo, novoValor)
                        return True
                    return 'Cargo inválido'
                case 'senha':
                    if validarSenha(novoValor):
                        colab.updateAttr(campo, novoValor)
                        return True
                    return 'Senha inválida'
    return 'Colaborador não encontrado'

def deleteColab(cpf):
    if validarCpf(cpf):
        for colab in Lista_Colaboradores:
            if colab.cpf == cpf:
                Lista_Colaboradores.remove(colab)
                return True
        return 'Colaborador não encontrado'
    return 'CPF inválido'

def getColab(id):
    for colab in Lista_Colaboradores:
        if colab.id == id:
                return colab
        return False
    return 'id inválido'
