import re
from datetime import datetime, date
    
def validarNome(nome):
    if not nome:
        return False
    if not isinstance(nome, str) or len(nome.strip()) <= 5 or len(nome) >= 100:
        return False
    nome = nome.replace(' ', '')
    pattern = r'^[a-zA-ZÀ-ÿ&]+$'
    return bool(re.match(pattern, nome.strip()))

def validarCelular(cell):
    if not cell:
        return False
    cell_limpo = ''.join(filter(str.isdecimal, str(cell)))
    return len(cell_limpo)==11 

def validarTelefone(telefone):
    telefone_limpo = ''.join(filter(str.isdecimal, str(telefone)))
    return len(telefone_limpo)==10  

def validarEmail(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validarNascimento(nascimento):
    if not nascimento:
        return False
    try:
        data_nasc = datetime.strptime(nascimento, '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return 18 <= idade <= 120  
    except ValueError:
        return False

def validarCpf(cpf):
    if not cpf:
        return False
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

def validarCNPJ(cnpj):
    if not cnpj:
        return False
    cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
        
    if len(cnpj_limpo) != 14:
        return False
        
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False
        
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj_limpo[i]) * peso
        peso = 9 if peso == 2 else peso - 1  
        
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto  
        
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
    
def validarCep(cep):
    if not cep:
        return False
    cep_limpo = ''.join(filter(str.isdigit, str(cep)))
    return len(cep_limpo)==8 

def validarTxt(texto): 
    if not isinstance(texto, str) or not texto.strip():
        return False
    pattern = r'^[a-zA-ZÀ-ÿ\s\-]+$'
    return bool(re.match(pattern, texto.strip()))

def validarNum(num):
    return num.strip().isdecimal()

def validarIe(ie):
    ie_limpo = ''.join(filter(str.isdecimal, str(ie)))
    return len(ie_limpo) <= 14 and len(ie_limpo) >= 8

def validarSenha(senha):
    return len(senha)>=8 and re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', senha)

def verificarSenha(senha, verificador):  
    return senha == verificador               

def validarComplemento(complemento):
    if not isinstance(complemento, str) or not complemento.strip():
        return False
    pattern = r'^[a-zA-ZÀ-ÿ\s\d\-]+$'
    return bool(re.match(pattern, complemento.strip()))
    

def validacaoGeralPf(nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, verificador, logradouro='', numero='', complemento=''):
        validacoes = [
            (validarNome(nome), 'Nome inválido'), 
            (validarNascimento(nascimento), 'Nascimento inválido'),
            (validarCpf(cpf), 'CPF inválido'),
            (validarCelular(celular), 'Celular inválido'),
            (validarEmail(email), 'Email inválido'),
            (validarCep(cep), 'CEP inválido'),
            (validarTxt(bairro), 'Bairro inválido'),
            (validarTxt(estado), 'Estado inválido'),
            (validarTxt(cidade), 'Cidade inválido'),
            (validarSenha(senha), 'Senha inválida'),
            (verificarSenha(senha, verificador), 'As senhas não coincidem')
        ]

        if logradouro:
            validacoes.append((validarTxt(logradouro), 'Logradouro inválido'))
        if numero:
            validacoes.append((validarNum(numero), 'Número inválido'))
        if complemento:
            validacoes.append((validarComplemento(complemento), 'Complemento inválido'))

        erros = []
        for validade, mensagem in validacoes:
            if not validade:
                erros.append(mensagem)

        if erros:
            raise ValueError(erros)
        return True

def validacaoGeralPj(RS, NF, cnpj, nome, cpf, cargo, phone, email, cep, logra, num, bairro, estado, cidade, senha, verificador, ie='', cell='', complemento=''):
            
            validacoes = [
                (validarNome(RS), 'Razão social inválida'), 
                (validarNome(NF), 'Nome fantasia inválido'),
                (validarCNPJ(cnpj), 'CNPJ inválido'),
                (validarNome(nome), 'Nome do representante inválido'),
                (validarCpf(cpf), 'CPF do representante inválido'),
                (validarTxt(cargo), 'Cargo inválido'),
                (validarTelefone(phone), 'Telefone inválido'),
                (validarEmail(email), 'Email inválido'),
                (validarCep(cep), 'CEP inválido'),
                (validarTxt(logra), 'Logradouro inválido'),
                (validarNum(num), 'Número inválido'),
                (validarTxt(bairro), 'Bairro inválido'),
                (validarTxt(estado), 'Estado inválido'),
                (validarTxt(cidade), 'Cidade inválido'),
                (validarSenha(senha), 'Senha inválida'),
                (verificarSenha(senha, verificador), 'As senhas não coincidem')
            ]

            if ie:
                validacoes.append((validarIe(ie), 'Inscrição estadual inválido'))
            if cell:
                validacoes.append((validarCelular(cell), 'Celular inválido'))
            if complemento:
                validacoes.append((validarComplemento(complemento), 'Complemento inválido'))

            erros = []
            for validade, mensagem in validacoes:
                if not validade:
                    erros.append(mensagem)

            if erros:
                raise ValueError(erros)
            return True

