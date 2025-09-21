from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, date
import re

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'

# "Banco de dados" em memória (dicionário)
veiculos_locacao = [
    # ---------------- ECONÔMICO ----------------
    {
        "id": 1,
        "tipo": "econômico",
        "categoria": "Econômico",
        "marca": "Fiat",
        "modelo": "Mobi",
        "transmissao": "manual",
        "preco_diario": 95.00,
        "nome": "Fiat Mobi",
        "imagem": "https://production.autoforce.com/uploads/version/profile_image/10921/model_main_webp_comprar-like-1-0_9eee82ebb4.png.webp",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 2,
        "tipo": "econômico",
        "categoria": "Econômico",
        "marca": "Renault",
        "modelo": "Kwid",
        "transmissao": "manual",
        "preco_diario": 100.00,
        "nome": "Renault Kwid",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348031/RENAULT_KWID_1.0_12V_SCE_FLEX_OUTSIDER_MANUAL_34803110315083122.webp",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 3,
        "tipo": "econômico",
        "categoria": "Econômico",
        "marca": "Hyundai",
        "modelo": "HB20",
        "transmissao": "manual",
        "preco_diario": 110.00,
        "nome": "Hyundai HB20",
        "imagem": "https://www.webmotors.com.br/imagens/prod/379453/HYUNDAI_HB20_1.0_TGDI_FLEX_PLATINUM_SAFETY_AUTOMATICO_3794531645596726.webp",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 4,
        "tipo": "econômico",
        "categoria": "Econômico",
        "marca": "Chevrolet",
        "modelo": "Onix",
        "transmissao": "manual",
        "preco_diario": 115.00,
        "nome": "Chevrolet Onix",
        "imagem": "https://www.chevrolet.com.br/content/dam/chevrolet/south-america/brazil/portuguese/index/portable-navigation/jellys/02-images/onix-plus-premiere-prata.jpg?imwidth=1200",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 5,
        "tipo": "econômico",
        "categoria": "Econômico",
        "marca": "Volkswagen",
        "modelo": "Gol",
        "transmissao": "manual",
        "preco_diario": 105.00,
        "nome": "Volkswagen Gol",
        "imagem": "https://cdn.motor1.com/images/mgl/YAAopq/s3/volkswagen-gol-1.0-2023.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },

    # ---------------- SEDAN ----------------
    {
        "id": 6,
        "tipo": "sedan",
        "categoria": "Sedan",
        "marca": "Toyota",
        "modelo": "Corolla",
        "transmissao": "automático",
        "preco_diario": 180.00,
        "nome": "Toyota Corolla",
        "imagem": "https://www.webmotors.com.br/imagens/prod/379444/TOYOTA_COROLLA_1.8_VVTI_HYBRID_FLEX_ALTIS_PREMIUM_CVT_37944417132188584.webp",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 7,
        "tipo": "sedan",
        "categoria": "Sedan",
        "marca": "Honda",
        "modelo": "Civic",
        "transmissao": "automático",
        "preco_diario": 185.00,
        "nome": "Honda Civic",
        "imagem": "https://di-uploads-pod33.dealerinspire.com/hendrickhondacharlotte/uploads/2021/03/mlp-img-top-2021-civic.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 8,
        "tipo": "sedan",
        "categoria": "Sedan",
        "marca": "Nissan",
        "modelo": "Sentra",
        "transmissao": "automático",
        "preco_diario": 170.00,
        "nome": "Nissan Sentra",
        "imagem": "https://www.nissan-cdn.net/content/dam/Nissan/br/site/veiculos/sentra-my25/thumbs/sentra_exclusive_int_premium.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 9,
        "tipo": "sedan",
        "categoria": "Sedan",
        "marca": "Chevrolet",
        "modelo": "Cruze",
        "transmissao": "automático",
        "preco_diario": 175.00,
        "nome": "Chevrolet Cruze",
        "imagem": "https://revistacarro.com.br/wp-content/uploads/2018/05/chevrolet_cruze_sport6_ltz.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 10,
        "tipo": "sedan",
        "categoria": "Sedan",
        "marca": "Volkswagen",
        "modelo": "Virtus",
        "transmissao": "automático",
        "preco_diario": 165.00,
        "nome": "Volkswagen Virtus",
        "imagem": "https://cadastro.motorleads.co/public/images/20240130022136-v5.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },

    # ---------------- SUV ----------------
    {
        "id": 11,
        "tipo": "suv",
        "categoria": "SUV",
        "marca": "Jeep",
        "modelo": "Compass",
        "transmissao": "automático",
        "preco_diario": 220.00,
        "nome": "Jeep Compass",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348683/JEEP_COMPASS_1.3_T270_TURBO_FLEX_S_AT6_3486831606189095.webp?s=fill&w=170&h=125&t=true",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Diesel",
        "status": "disponível"
    },
    {
        "id": 12,
        "tipo": "suv",
        "categoria": "SUV",
        "marca": "Hyundai",
        "modelo": "Creta",
        "transmissao": "automático",
        "preco_diario": 200.00,
        "nome": "Hyundai Creta",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348376/HYUNDAI_CRETA_1.6_16V_FLEX_ACTION_AUTOMATICO_34837618173811432.webp",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 13,
        "tipo": "suv",
        "categoria": "SUV",
        "marca": "Honda",
        "modelo": "HR-V",
        "transmissao": "automático",
        "preco_diario": 210.00,
        "nome": "Honda HR-V",
        "imagem": "https://production.autoforce.com/uploads/version/profile_image/9408/comprar-exl-honda-sensing_f6ae5428c9.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 14,
        "tipo": "suv",
        "categoria": "SUV",
        "marca": "Nissan",
        "modelo": "Kicks",
        "transmissao": "automático",
        "preco_diario": 195.00,
        "nome": "Nissan Kicks",
        "imagem": "https://www.nissan.com.br/content/dam/Nissan/br/site/veiculos/kicks-play/360/advance/branco-diamond/01.png.ximg.c1h.360.png",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },
    {
        "id": 15,
        "tipo": "suv",
        "categoria": "SUV",
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "transmissao": "automático",
        "preco_diario": 205.00,
        "nome": "Chevrolet Tracker",
        "imagem": "https://www.autoclachevrolet.com.br/content/dam/chevrolet/sa/br/pt/master/home/suvs/tracker/tracker-myr-2026/2-colorizer/lt-at-turbo/chevrolet-tracker-lt-preto-ouro-negro.jpg?imwidth=1920",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Flex",
        "status": "disponível"
    },

    # ---------------- LUXO ----------------
    {
        "id": 16,
        "tipo": "luxo",
        "categoria": "Luxo",
        "marca": "BMW",
        "modelo": "Série 3",
        "transmissao": "automático",
        "preco_diario": 450.00,
        "nome": "BMW Série 3",
        "imagem": "https://www.bmw.com.br/content/dam/bmw/common/all-models/3-series/sedan/2024/navigation/bmw-3-series-ice-lci-modelfinder.png",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 17,
        "tipo": "luxo",
        "categoria": "Luxo",
        "marca": "Audi",
        "modelo": "A4",
        "transmissao": "automático",
        "preco_diario": 460.00,
        "nome": "Audi A4",
        "imagem": "https://www.webmotors.com.br/imagens/prod/379665/AUDI_A4_2.0_TFSI_MHEV_S_LINE_QUATTRO_S_TRONIC_37966510582707039.webp",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 18,
        "tipo": "luxo",
        "categoria": "Luxo",
        "marca": "Mercedes-Benz",
        "modelo": "C180",
        "transmissao": "automático",
        "preco_diario": 480.00,
        "nome": "Mercedes-Benz C180",
        "imagem": "https://www.webmotors.com.br/imagens/prod/347940/MERCEDESBENZ_C_180_1.6_CGI_GASOLINA_SPORT_COUPE_9GTRONIC_34794009590838032.webp",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
    },
    {
        "id": 19,
        "tipo": "luxo",
        "categoria": "Luxo",
        "marca": "Volvo",
        "modelo": "XC60",
        "transmissao": "automático",
        "preco_diario": 500.00,
        "nome": "Volvo XC60",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348860/VOLVO_XC60_2.0_T8_RECHARGE_POLESTAR_ENGINEERED_AWD_GEARTRONIC_34886011041803311.webp",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Híbrido",
        "status": "disponível"
    },
    {
        "id": 20,
        "tipo": "luxo",
        "categoria": "Luxo",
        "marca": "Jaguar",
        "modelo": "XE",
        "transmissao": "automático",
        "preco_diario": 520.00,
        "nome": "Jaguar XE",
        "imagem": "https://www.webmotors.com.br/imagens/prod/348195/JAGUAR_XE_2.0_16V_INGENIUM_P250_GASOLINA_RDYNAMIC_S_4P_AUTOMATICO_34819510562480227.webp",
        "numero_malas": 4,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "combustivel": "Gasolina",
        "status": "disponível"
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
    # Obter parâmetros de filtro da URL
    categoria = request.args.get('categoria', '')
    marca = request.args.get('marca', '')
    modelo = request.args.get('modelo', '')
    transmissao = request.args.get('transmissao', '')
    combustivel = request.args.get('combustivel', '')
    preco_maximo = request.args.get('preco_maximo', '')
    malas_min = request.args.get('malas_min', '')
    passageiros_min = request.args.get('passageiros_min', '')
    portas_min = request.args.get('portas_min', '')
    
    # Filtrar veículos
    veiculos_filtrados = veiculos_locacao.copy()
    
    # Aplicar filtros apenas se os valores não estiverem vazios
    if categoria and categoria != 'todos':
        veiculos_filtrados = [v for v in veiculos_filtrados if v['categoria'].lower() == categoria.lower()]
    
    if marca:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['marca'].lower() == marca.lower()]
    
    if modelo:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['modelo'].lower() == modelo.lower()]
    
    if transmissao:
        veiculos_filtrados = [v for v in veiculos_filtrados if v['transmissao'].lower() == transmissao.lower()]
    
    if combustivel:
        veiculos_filtrados = [v for v in veiculos_filtrados if v.get('combustivel', '').lower() == combustivel.lower()]
    
    if preco_maximo:
        try:
            preco = float(preco_maximo)
            veiculos_filtrados = [v for v in veiculos_filtrados if v['preco_diario'] <= preco]
        except ValueError:
            pass
    
    if malas_min:
        try:
            min_malas = int(malas_min)
            veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_malas'] >= min_malas]
        except ValueError:
            pass
    
    if passageiros_min:
        try:
            min_passageiros = int(passageiros_min)
            # Ordenar por proximidade ao número solicitado (exato primeiro)
            veiculos_filtrados = sorted(
                [v for v in veiculos_filtrados if v['numero_passageiros'] >= min_passageiros],
                key=lambda x: (x['numero_passageiros'] == min_passageiros, x['numero_passageiros']),
                reverse=True
            )
        except ValueError:
            pass
    
    if portas_min:
        try:
            min_portas = int(portas_min)
            veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_portas'] >= min_portas]
        except ValueError:
            pass
    
    # Formatar os dados para o template
    veiculos_formatados = []
    for veiculo in veiculos_filtrados:
        veiculos_formatados.append({
            'id': veiculo.get('id', 0),
            'categoria': veiculo['categoria'],
            'marca': veiculo['marca'],
            'modelo': veiculo['modelo'],
            'transmissao': veiculo['transmissao'],
            'preco': f"{veiculo['preco_diario']:.2f}",
            'nome': veiculo['nome'],
            'imagem': veiculo['imagem'],
            'malas': veiculo['numero_malas'],
            'passageiros': veiculo['numero_passageiros'],
            'portas': veiculo['numero_portas'],
            'combustivel': veiculo.get('combustivel', 'Flex'),
            'status': veiculo['status']
        })
    
    return render_template('frota.html', veiculos=veiculos_formatados)

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

@app.route('/api/filtrar', methods=['POST'])
def api_filtrar():
    try:
        # Obter dados do JSON
        data = request.get_json()
        
        categoria = data.get('categoria', '')
        marca = data.get('marca', '')
        modelo = data.get('modelo', '')
        transmissao = data.get('transmissao', '')
        combustivel = data.get('combustivel', '')
        preco_maximo = data.get('preco_maximo', '')
        malas_min = data.get('malas_min', '')
        passageiros_min = data.get('passageiros_min', '')
        portas_min = data.get('portas_min', '')
        
        # Filtrar veículos
        veiculos_filtrados = veiculos_locacao.copy()
        
        # Aplicar filtros
        if categoria and categoria != 'todos':
            veiculos_filtrados = [v for v in veiculos_filtrados if v['categoria'].lower() == categoria.lower()]
        
        if marca:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['marca'].lower() == marca.lower()]
        
        if modelo:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['modelo'].lower() == modelo.lower()]
        
        if transmissao:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['transmissao'].lower() == transmissao.lower()]
        
        if combustivel:
            veiculos_filtrados = [v for v in veiculos_filtrados if v.get('combustivel', '').lower() == combustivel.lower()]
        
        if preco_maximo:
            try:
                preco = float(preco_maximo)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['preco_diario'] <= preco]
            except ValueError:
                pass
        
        if malas_min:
            try:
                min_malas = int(malas_min)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_malas'] >= min_malas]
            except ValueError:
                pass
        
        if passageiros_min:
            try:
                min_passageiros = int(passageiros_min)
                # Ordenar por proximidade ao número solicitado (exato primeiro)
                veiculos_filtrados = sorted(
                    [v for v in veiculos_filtrados if v['numero_passageiros'] >= min_passageiros],
                    key=lambda x: (x['numero_passageiros'] == min_passageiros, x['numero_passageiros']),
                    reverse=True
                )
            except ValueError:
                pass
        
        if portas_min:
            try:
                min_portas = int(portas_min)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_portas'] >= min_portas]
            except ValueError:
                pass
        
        # Formatar resposta
        resposta = []
        for veiculo in veiculos_filtrados:
            resposta.append({
                'id': veiculo.get('id', 0),
                'categoria': veiculo['categoria'],
                'marca': veiculo['marca'],
                'modelo': veiculo['modelo'],
                'transmissao': veiculo['transmissao'],
                'preco': f"{veiculo['preco_diario']:.2f}",
                'nome': veiculo['nome'],
                'imagem': veiculo['imagem'],
                'malas': veiculo['numero_malas'],
                'passageiros': veiculo['numero_passageiros'],
                'portas': veiculo['numero_portas'],
                'combustivel': veiculo.get('combustivel', 'Flex'),
                'status': veiculo['status']
            })
        
        return jsonify(resposta)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)