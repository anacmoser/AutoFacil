import re

class UserPj:
    def __init__(self, id, razaoSocial, nomeFantasia, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual='' ,cell='', complemento=''):

        if self.validacaoGeral(razaoSocial, nomeFantasia, cnpj, nomeRep, cpfRep, cargoRep, telefone, emailCop, cep, logradouro, numero, bairro, estado, cidade, senha, confirmar, inscricaoEstadual ,cell, complemento):
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

    def validacaoGeral(self, RS, NF, cnpj, nome, cpf, cargo, phone, email, cep, logra, num, bairro, estado, cidade, senha, verificador, ie='', cell='', complemento=''):
            
            validacoes = [
                (self.validarNome(RS), 'Razão social inválida'), 
                (self.validarNome(NF), 'Nome fantasia inválido'),
                (self.validarCNPJ(cnpj), 'CNPJ inválido'),
                (self.validarNomeRep(nome), 'Nome do representante inválido'),
                (self.validarCPF(cpf), 'CPF do representante inválido'),
                (self.validarTxt(cargo), 'Cargo inválido'),
                (self.validarTelefone(phone), 'Telefone inválido'),
                (self.validarEmail(email), 'Email inválido'),
                (self.validarCep(cep), 'CEP inválido'),
                (self.validarTxt(logra), 'Logradouro inválido'),
                (self.validarNum(num), 'Número inválido'),
                (self.validarTxt(bairro), 'Bairro inválido'),
                (self.validarTxt(estado), 'Estado inválido'),
                (self.validarTxt(cidade), 'Cidade inválido'),
                (self.validarSenha(senha), 'Senha inválida'),
                (self.verificarSenha(senha, verificador), 'As senhas não coincidem')
            ]

            if ie:
                validacoes.append((self.validarIe(ie), 'Inscrição estadual inválido'))
            if cell:
                validacoes.append((self.validarCelular(cell), 'Celular inválido'))
            if complemento:
                validacoes.append((self.validarTxt(complemento), 'Complemento inválido'))

            erros = []
            for validade, mensagem in validacoes:
                if not validade:
                    erros.append(mensagem)

            if erros:
                raise ValueError(erros)
            return True

    def validarNome(self, nome): #Para razão social e nome fantasia
        if not isinstance(nome, str) or len(nome) >= 100:
            return False
        pattern = r'^[a-zA-ZÀ-ÿ0-9&]+$'
        nome = nome.replace(' ', '')
        return bool(re.match(pattern, nome.strip()))

    def validarCNPJ(self, cnpj):
        cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
        
        if len(cnpj_limpo) != 14:
            return False
        
        if cnpj_limpo == cnpj_limpo[0] * 14:
            return False
        
        # PRIMEIRO DÍGITO - CORRIGIDO
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj_limpo[i]) * peso
            peso = 9 if peso == 2 else peso - 1  # ✅ Correção da lógica do peso
        
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto  # ✅ Correção do cálculo
        
        if digito1 != int(cnpj_limpo[12]):
            return False
        
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj_limpo[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        if digito2 != int(cnpj_limpo[13]):
            return False
        
        return True

    def validarNomeRep(self, nomeRep):
        if not isinstance(nomeRep, str) or len(nomeRep.strip()) <= 5 or len(nomeRep) >= 100:
                return False
        nomeRep = nomeRep.replace(' ', '')
        pattern = r'^[a-zA-ZÀ-ÿ]+$'
        return bool(re.match(pattern, nomeRep.strip()))

    def validarCPF(self, cpf):
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

    def validarTxt(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            return False
        # Permite letras, espaços, hífens e acentos
        pattern = r'^[a-zA-ZÀ-ÿ\s\-]+$'
        return bool(re.match(pattern, texto.strip()))

    def validarCelular(self,cell):
        cell_limpo = ''.join(filter(str.isdecimal, str(cell)))
        return len(cell_limpo)==11 

    def validarTelefone(self,telefone):
        telefone_limpo = ''.join(filter(str.isdecimal, str(telefone)))
        return len(telefone_limpo)==10  

    def validarEmail(self,email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validarCep(self,cep):
        cep_limpo = ''.join(filter(str.isdigit, str(cep)))
        return len(cep_limpo)==8 

    def validarNum(self,num):
        return num.strip().isdecimal()

    def validarSenha(self,senha):
        return len(senha)>=8 and re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', senha)

    def verificarSenha(self, senha, verificador):
        return senha == verificador

    def validarIe(self, ie):
        ie_limpo = ''.join(filter(str.isdecimal, str(ie)))
        return len(ie_limpo) <= 14

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