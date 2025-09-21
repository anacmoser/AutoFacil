from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, date
import re

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'

# "Banco de dados" em memória (dicionário)
usuarios = [{'id': 1,
             'nome': 'teste', 
             'nascimento': '1111-11-11', 
             'cpf': '00000000000', 
             'celular': '22222222', 
             'email': 'teste@gmail.com', 
             'cep': '333333', 
             'logradouro': 'testeLogradouro', 
             'numero': '444', 
             'complemento': 'testeComplemento', 
             'bairro': 'testeBairro', 
             'estado': 'testeEstado', 
             'cidade': 'testeCidade', 
             'senha': '1234'}]

# Variável global para IDs - usar com cuidado em produção
id_counter = 2


veiculos = [
    # ---------------- ECONÔMICO ----------------
    {
        "id": 1,
        "nome": "Fiat Mobi",
        "categoria": "Econômico",
        "marca": "fiat",
        "modelo": "mobi",
        "imagem": "https://production.autoforce.com/uploads/version/profile_image/10921/model_main_webp_comprar-like-1-0_9eee82ebb4.png.webp",
        "passageiros": 5,
        "malas": 2,
        "transmissao": "manual",
        "combustivel": "Flex",
        "preco": 95
    },
    {
        "id": 2,
        "nome": "Renault Kwid",
        "categoria": "Econômico",
        "marca": "renault",
        "modelo": "kwid",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348031/RENAULT_KWID_1.0_12V_SCE_FLEX_OUTSIDER_MANUAL_34803110315083122.webp",
        "passageiros": 5,
        "malas": 2,
        "transmissao": "manual",
        "combustivel": "Flex",
        "preco": 100
    },
    {
        "id": 3,
        "nome": "Hyundai HB20",
        "categoria": "Econômico",
        "marca": "hyundai",
        "modelo": "hb20",
        "imagem": "/static/img/hb20.webp",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "manual",
        "combustivel": "Flex",
        "preco": 110
    },
    {
        "id": 4,
        "nome": "Chevrolet Onix",
        "categoria": "Econômico",
        "marca": "chevrolet",
        "modelo": "onix",
        "imagem": "/static/img/onix.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "manual",
        "combustivel": "Flex",
        "preco": 115
    },
    {
        "id": 5,
        "nome": "Volkswagen Gol",
        "categoria": "Econômico",
        "marca": "volkswagen",
        "modelo": "gol",
        "imagem": "https://cdn.motor1.com/images/mgl/YAAopq/s3/volkswagen-gol-1.0-2023.jpg",
        "passageiros": 5,
        "malas": 2,
        "transmissao": "manual",
        "combustivel": "Flex",
        "preco": 105
    },

    # ---------------- SEDAN ----------------
    {
        "id": 6,
        "nome": "Toyota Corolla",
        "categoria": "Sedan",
        "marca": "toyota",
        "modelo": "corolla",
        "imagem": "/static/img/corolla.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 180
    },
    {
        "id": 7,
        "nome": "Honda Civic",
        "categoria": "Sedan",
        "marca": "honda",
        "modelo": "civic",
        "imagem": "https://di-uploads-pod33.dealerinspire.com/hendrickhondacharlotte/uploads/2021/03/mlp-img-top-2021-civic.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 185
    },
    {
        "id": 8,
        "nome": "Nissan Sentra",
        "categoria": "Sedan",
        "marca": "nissan",
        "modelo": "sentra",
        "imagem": "https://www.nissan-cdn.net/content/dam/Nissan/br/site/veiculos/sentra-my25/thumbs/sentra_exclusive_int_premium.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 170
    },
    {
        "id": 9,
        "nome": "Chevrolet Cruze",
        "categoria": "Sedan",
        "marca": "chevrolet",
        "modelo": "cruze",
        "imagem": "https://revistacarro.com.br/wp-content/uploads/2018/05/chevrolet_cruze_sport6_ltz.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 175
    },
    {
        "id": 10,
        "nome": "Volkswagen Virtus",
        "categoria": "Sedan",
        "marca": "volkswagen",
        "modelo": "virtus",
        "imagem": "https://cadastro.motorleads.co/public/images/20240130022136-v5.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 165
    },

    # ---------------- SUV ----------------
    {
        "id": 11,
        "nome": "Jeep Compass",
        "categoria": "SUV",
        "marca": "jeep",
        "modelo": "compass",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348683/JEEP_COMPASS_1.3_T270_TURBO_FLEX_S_AT6_3486831606189095.webp?s=fill&w=170&h=125&t=true",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Diesel",
        "preco": 220
    },
    {
        "id": 12,
        "nome": "Hyundai Creta",
        "categoria": "SUV",
        "marca": "hyundai",
        "modelo": "creta",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348376/HYUNDAI_CRETA_1.6_16V_FLEX_ACTION_AUTOMATICO_34837618173811432.webp",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 200
    },
    {
        "id": 13,
        "nome": "Honda HR-V",
        "categoria": "SUV",
        "marca": "honda",
        "modelo": "hrv",
        "imagem": "https://production.autoforce.com/uploads/version/profile_image/9408/comprar-exl-honda-sensing_f6ae5428c9.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 210
    },
    {
        "id": 14,
        "nome": "Nissan Kicks",
        "categoria": "SUV",
        "marca": "nissan",
        "modelo": "kicks",
        "imagem": "https://www.nissan.com.br/content/dam/Nissan/br/site/veiculos/kicks-play/360/advance/branco-diamond/01.png.ximg.c1h.360.png",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 195
    },
    {
        "id": 15,
        "nome": "Chevrolet Tracker",
        "categoria": "SUV",
        "marca": "chevrolet",
        "modelo": "tracker",
        "imagem": "https://www.autoclachevrolet.com.br/content/dam/chevrolet/sa/br/pt/master/home/suvs/tracker/tracker-myr-2026/2-colorizer/lt-at-turbo/chevrolet-tracker-lt-preto-ouro-negro.jpg?imwidth=1920",
        "passageiros": 5,
        "malas": 3,
        "transmissao": "automatico",
        "combustivel": "Flex",
        "preco": 205
    },

    # ---------------- LUXO ----------------
    {
        "id": 16,
        "nome": "BMW Série 3",
        "categoria": "Luxo",
        "marca": "bmw",
        "modelo": "serie-3",
        "imagem": "https://www.bmw.com.br/content/dam/bmw/common/all-models/3-series/sedan/2024/navigation/bmw-3-series-ice-lci-modelfinder.png",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 450
    },
    {
        "id": 17,
        "nome": "Audi A4",
        "categoria": "Luxo",
        "marca": "audi",
        "modelo": "a4",
        "imagem": "https://www.webmotors.com.br/imagens/prod/379665/AUDI_A4_2.0_TFSI_MHEV_S_LINE_QUATTRO_S_TRONIC_37966510582707039.webp",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 460
    },
    {
        "id": 18,
        "nome": "Mercedes-Benz C180",
        "categoria": "Luxo",
        "marca": "mercedes",
        "modelo": "c180",
        "imagem": "https://www.webmotors.com.br/imagens/prod/347940/MERCEDESBENZ_C_180_1.6_CGI_GASOLINA_SPORT_COUPE_9GTRONIC_34794009590838032.webp",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 480
    },
    {
        "id": 19,
        "nome": "Volvo XC60",
        "categoria": "Luxo",
        "marca": "volvo",
        "modelo": "xc60",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348860/VOLVO_XC60_2.0_T8_RECHARGE_POLESTAR_ENGINEERED_AWD_GEARTRONIC_34886011041803311.webp",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Híbrido",
        "preco": 500
    },
    {
        "id": 20,
        "nome": "Jaguar XE",
        "categoria": "Luxo",
        "marca": "jaguar",
        "modelo": "xe",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348195/JAGUAR_XE_2.0_16V_INGENIUM_P250_GASOLINA_RDYNAMIC_S_4P_AUTOMATICO_34819510562480227.webp",
        "passageiros": 5,
        "malas": 4,
        "transmissao": "automatico",
        "combustivel": "Gasolina",
        "preco": 520
    }
]


# Função para validar CPF (formato apenas)
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        return False
    
    return True

# Função para validar e-mail
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Função para validar telefone
def validar_telefone(telefone): 
    telefone = re.sub(r'[^0-9]', '', telefone)
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    return len(telefone) in [10, 11]

# Função para validar CEP
def validar_cep(cep):
    # Remove caracteres não numéricos
    cep = re.sub(r'[^0-9]', '', cep)
    # Verifica se tem 8 dígitos
    return len(cep) == 8

def validar_nome(nome):  
    nome = nome.strip()
    
    # Verifica comprimento e se contém apenas letras e espaços
    if len(nome) < 2 or not all(c.isalpha() or c.isspace() for c in nome):
        return False
    return True

def validar_nascimento(nascimento):
    data_str = nascimento.strip()
    
    # Verifica o formato com regex (YYYY-MM-DD)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data_str):
        return False, "Formato de data inválido. Use YYYY-MM-DD"
    
    # Extrai ano, mês e dia
    try:
        ano, mes, dia = map(int, data_str.split('-'))
    except ValueError:
        return False, "Data contém valores não numéricos"
    
    # Valida se a data existe
    try:
        data_nascimento = date(ano, mes, dia)
    except ValueError:
        return False, "Data inválida (dia, mês ou ano incorretos)"
    
    # Verifica se a data não é futura
    data_atual = date.today()
    if data_nascimento > data_atual:
        return False, "Data de nascimento não pode ser futura"
    
    # Calcula a idade
    idade = calcular_idade(ano, mes, dia)
    
    # Verifica se é maior de 18 anos
    if idade < 18:
        return False, f"Menor de idade ({idade} anos)"
    
    return True, f"Maior de idade ({idade} anos)"

def calcular_idade(ano, mes, dia):
    hoje = date.today()
    idade = hoje.year - ano
    # Ajusta se ainda não fez aniversário este ano
    if (hoje.month, hoje.day) < (mes, dia):
        idade -= 1
    return idade

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def mudarCadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def mudarLogin():
    return render_template('login.html')

@app.route('/frota', methods=['GET'])
def mudarFrota():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('frota.html', veiculos=veiculos)

@app.route('/cadastrar', methods=['POST'])
def cadastro():
    global id_counter  # Usar a variável global
    
    # Obter dados do formulário
    nome = request.form.get('nome', '').strip()
    nascimento = request.form.get('nascimento', '')
    cpf = request.form.get('cpf', '')
    cpf = re.sub(r'[^0-9]', '', cpf)
    celular = request.form.get('celular', '')
    celular = re.sub(r'[^0-9]', '', celular)
    email = request.form.get('email', '').strip()
    cep = request.form.get('cep', '')
    logradouro = request.form.get('logradouro', '').strip()
    numero = request.form.get('numero', '').strip()
    complemento = request.form.get('complemento', '').strip()
    bairro = request.form.get('bairro', '').strip()
    estado = request.form.get('estado', '').strip()
    cidade = request.form.get('cidade', '').strip()
    senha = request.form.get('senha', '')
    confirmar_senha = request.form.get('confirmar', '')
    termos = request.form.get('termos')
    
    # Validações do servidor
    erros = []
    
    # Verificar se todos os campos obrigatórios foram preenchidos
    campos_obrigatorios = ['nome', 'nascimento', 'cpf', 'celular', 'email', 'cep', 
                          'logradouro', 'bairro', 'estado', 'cidade', 'senha']
    
    for campo in campos_obrigatorios:
        if not request.form.get(campo):
            erros.append(f'O campo {campo.replace("_", " ").title()} é obrigatório.')
    
    # VALIDAÇÃO DOS CAMPOS
    if nome and not validar_nome(nome):
        erros.append('Nome inválido. Deve conter apenas letras e espaços.')
    
    if cpf and not validar_cpf(cpf):
        erros.append('CPF inválido. Deve conter 11 dígitos.')
    
    if email and not validar_email(email):
        erros.append('E-mail inválido.')
    
    if celular and not validar_telefone(celular):
        erros.append('Número de celular inválido.')
    
    if cep and not validar_cep(cep):
        erros.append('CEP inválido. Deve conter 8 dígitos.')
    
    if nascimento:
        valido, msg = validar_nascimento(nascimento)
        if not valido:
            erros.append(msg)

    # VERIFICAÇÃO DE EMAIL E CPF JÁ CADASTRADOS
    for usuario in usuarios:
        if email and email == usuario['email']:
            erros.append('Este e-mail já está cadastrado.')
        if cpf and cpf == usuario['cpf']:
            erros.append('Este CPF já está cadastrado.')
    
    # Verificar se as senhas coincidem
    if senha and confirmar_senha and senha != confirmar_senha:
        erros.append('As senhas não coincidem.')
    
    # Verificar se a senha tem pelo menos 8 caracteres
    if senha and len(senha) < 8:
        erros.append('A senha deve ter pelo menos 8 caracteres.')
    
    # Verificar se os termos foram aceitos
    if not termos:
        erros.append('Você deve aceitar os Termos de Uso.')
    
    # Se houver erros, retornar para o formulário com mensagens de erro
    if erros:
        return render_template('cadastro.html', erros=erros)
    
    # Se não houver erros, criar novo usuário
    novo_usuario = {
        'id': id_counter,
        'nome': nome, 
        'nascimento': nascimento, 
        'cpf': cpf, 
        'celular': celular, 
        'email': email, 
        'cep': cep, 
        'logradouro': logradouro, 
        'numero': numero, 
        'complemento': complemento, 
        'bairro': bairro, 
        'estado': estado, 
        'cidade': cidade, 
        'senha': senha
    }

    id_counter += 1
    usuarios.append(novo_usuario)
    
    return redirect(url_for('login'))



@app.route('/logar', methods=['GET', 'POST']) #Completo
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('password')

        if '@' in user:
            #verificação por email
            if not validar_email(user):
                return render_template('login.html', erro = 'E-mail inválido')
            for usuario in usuarios:
                if usuario['email'] == user :
                    if usuario['senha'] == senha:
                        session['usuario_logado'] = usuario
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')
        else: 
            #verificação por cpf
            cpf = re.sub(r'[^0-9]', '', user)
            if not validar_cpf(cpf):
                return render_template('login.html', erro = 'Digite e-mail ou CPF inválidos')
            for usuario in usuarios:
                if usuario['cpf'] == cpf:
                    if usuario['senha'] == senha:
                        session['usuario_logado'] = usuario
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')        
    
    return render_template('login.html')

@app.route('/filtrar')
def frota():
    # Verificar se o usuário está logado
    
    
    # Obter parâmetros de filtro da URL
    categoria = request.args.get('categoria', '')
    marca = request.args.get('marca', '')
    modelo = request.args.get('modelo', '')
    transmissao = request.args.get('transmissao', '')
    preco_max = request.args.get('preco_max', '')
    
    # Filtrar veículos
    veiculos_filtrados = veiculos
    
    if categoria and categoria != 'Todos':
        veiculos_filtrados = [v for v in veiculos_filtrados if v['categoria'].lower() == categoria.lower()]
    
    if marca:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['marca'] == marca]
    
    if modelo:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['modelo'] == modelo]
    
    if transmissao:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['transmissao'] == transmissao]
    
    if preco_max:
        try:
            preco_max = float(preco_max)
            veiculos_filtrados = [v for v in veiculos_filtrados if v['preco'] <= preco_max]
        except ValueError:
            pass
    
    return render_template('frota.html', veiculos=veiculos_filtrados)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)