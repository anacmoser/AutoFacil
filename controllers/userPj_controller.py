#PESSOA JURÍDICA

#Verificar se os campos estão vazios

#função de cadastro
#função de login

from flask import Blueprint, request, render_template, redirect, url_for
from models.UserPj import UserPj, USERSpj, addUserPj

user_pj_bp = Blueprint('user_pj_bp', __name__)

@user_pj_bp.route('/cadastrarPj', methods=['POST'])
def cadastroEmpresa():
    global id_counter_pj
    tipo_conta = request.args.get('tipo_conta')

    rs = request.form.get('razao_social', '').strip()
    nf = request.form.get('nome_fantasia', '').strip()
    cnpj = request.form.get('cnpj', '')
    ie = request.form.get('inscricao_estadual', '').strip()
    ramo = request.form.get('ramo_atividade', '')
    tamanho = request.form.get('tamanho_empresa', '')
    nomeRep = request.form.get('nome_representante', '').strip()
    cpfRep = request.form.get('cpf_representante', '')
    cargoRep = request.form.get('cargo_representante', '').strip()
    phone = request.form.get('telefone_empresa', '')
    cell = request.form.get('celular_empresa', '')
    email = request.form.get('email_empresa', '').strip()
    cep = request.form.get('cep_empresa', '')
    logra = request.form.get('logradouro_empresa', '')
    num = request.form.get('numero_empresa', '')
    complemento = request.form.get('complemento_empresa', '')
    bairro = request.form.get('bairro_empresa', '').strip()
    estado = request.form.get('estado_empresa', '').strip()
    cidade = request.form.get('cidade_empresa', '').strip()
    senha = request.form.get('senha_empresa', '')
    confirmar = request.form.get('confirmar_empresa', '')
    termos = request.form.get('termos')
    autorizacao = request.form.get('autorizacao')

    campos_obrigatorios = [rs, nf, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, phone, email, cep, logra, num, bairro, estado, cidade, senha, confirmar]
    for campo in campos_obrigatorios:
        if not campo:
            return render_template('cadastro.html', erros='Todos os campos obrigatórios devem ser preenchidos')

    if not termos:
        return render_template('cadastro.html', erros='Você deve aceitar os Termos de Uso.')
    if not autorizacao:
        return render_template('cadastro.html', erros='Você deve aceitar a Autorização.')
    try:
        novoUser = UserPj(id_counter_pj, rs, nf, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, phone, email, cep, logra, num, bairro, estado, cidade, senha, confirmar, ie ,cell, complemento)
        adicao = addUserPj(novoUser) #Verificar por nome também (já existe por email e cpf)
        if adicao == True: #Se não for true será a lista de erros
            id_counter_pj += 1
            return redirect(url_for('login'))
        else:
            return render_template('cadastro.html', erros=adicao)
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
        
        return render_template('cadastro.html', erros=erros, tipo_conta=tipo_conta, tipo_conta_juridica=(tipo_conta == 'juridica'))

@user_pj_bp('/logarPJ')
def login():
