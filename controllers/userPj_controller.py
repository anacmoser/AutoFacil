#PESSOA JURÍDICA

#Verificar se os campos estão vazios

#função de cadastro
#função de login

from flask import Blueprint, request, render_template, redirect, url_for, session, make_response
from controllers.validacoes import validarEmail, validarCNPJ, validacaoGeralPj
from models.UserPj import UserPjDB, USERSpj, addUserPj, buscarUser, db
import re

user_pj_bp = Blueprint('user_pj_bp', __name__)

@user_pj_bp.route('/cadastrarPj', methods=['POST'])
def cadastroEmpresa():
    global id_counter_pj
    tipo_conta = request.args.get('tipo_conta')

    rs = request.form.get('razao_social', '').strip()
    nf = request.form.get('nome_fantasia', '').strip()
    cnpj = re.sub(r'[^0-9]', '', request.form.get('cnpj', ''))
    ie =  re.sub(r'[^0-9]', '', request.form.get('inscricao_estadual', '').strip())
    ramo = request.form.get('ramo_atividade', '')
    tamanho = request.form.get('tamanho_empresa', '')
    nomeRep = request.form.get('nome_representante', '').strip()
    cpfRep =  re.sub(r'[^0-9]', '', request.form.get('cpf_representante', ''))
    cargoRep = request.form.get('cargo_representante', '').strip()
    phone =  re.sub(r'[^0-9]', '', request.form.get('telefone_empresa', ''))
    cell =  re.sub(r'[^0-9]', '', request.form.get('celular_empresa', ''))
    email = request.form.get('email_empresa', '').strip()
    cep =  re.sub(r'[^0-9]', '', request.form.get('cep_empresa', ''))
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
    erros = validacaoGeralPj(rs, nf, cnpj, nomeRep, cpfRep, cargoRep, phone, email, cep, logra, num, bairro, estado, cidade, senha, confirmar, ie ,cell, complemento)
    if erros:
        return render_template('cadastro.html', erros = erros)
    try:
        novo_usuario = UserPjDB(
            Razao_Social=rs,
            Nome_Fantasia=nf,
            CNPJ=cnpj,
            Inscricao_Estadual=ie,
            Ramo=ramo,
            Tamanho_da_Empresa=tamanho,
            Nome=nomeRep,
            CPF=cpfRep,
            Cargo=cargoRep,
            Telefone_Comercial=phone,
            Celular=cell,
            Email_Corporativo=email,
            CEP=cep,
            Logradouro=logra,
            Numero=num,
            Complemento=complemento,
            Bairro=bairro,
            Estado=estado,
            Cidade=cidade,
            Senha=senha
)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return redirect(url_for('user_bp.pgLogin'))
    
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
 
        return render_template('cadastro.html', erros=erros, tipo_conta=tipo_conta, tipo_conta_juridica=(tipo_conta == 'juridica'))

@user_pj_bp.route('/logarPJ', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user', '')
        senha = request.form.get('password', '')
        remember = request.form.get('lembrar')

        if not user:
            return render_template('login.html', erro = 'Email obrigatório')
        if not senha:
            return render_template('login.html', erro = 'Senha obrigatória')
        
        if '@' in user:
            if not validarEmail(user):
                return render_template('login.html', erro = 'E-mail inválido')
            user = UserPjDB.query.filter_by(Email_Corporativo=user).first()
        else:
            cnpj = re.sub(r'[^0-9]', '', user)
            if not validarCNPJ(cnpj):
                return render_template('login.html', erro='CPF inválido')
            user = UserPjDB.query.filter_by(CNPJ=cnpj).first()
        # Se o usuário não foi encontrado
        if not user:
            return render_template('login.html', erro='Usuário não encontrado')

        # Verificar senha
        if user.Senha != senha:
            return render_template('login.html', erro='Senha incorreta')

        # Login bem-sucedido

        session['usuario_logado'] = user.Id_Cliente 
        session['usuario_perfil'] = 'pf'
        if remember:
            response = make_response(redirect(url_for('index')))
            response.set_cookie('user', user.Id_Cliente, max_age=60*60*72)
            response.set_cookie('perfil', 'pf', max_age=60*60*72)
            return response

        return redirect(url_for('index'))

    # Se o método for GET (abrir a página de login)
    return render_template('login.html')

@user_pj_bp.route('/updatePj')  #Colocar validação para cada alteração, adicionar outras alterações
def updatePj():
    user_id = session.get('usuario_logado')
    rs = request.form.get('razao-social', '')
    nf = request.form.get('nomeFantasia', '')
    cnpj = request.form.get('CNPJ', '')
    tell = request.form.get('telefone', '')
    email = request.form.get('email', '')
    ramo = request.form.get('ramo', '')
    tamanho = request.form.get('tamanho', '')
    rep = request.form.get('rep', '')

    user = buscarUser(user_id)

    if user.rs != rs:
        user.setAttr('_razaoSocial', rs)
    if user.nome != nf:
        user.setAttr('_nomeFant', rs)
    if user.cnpj != cnpj:
        user.setAttr('_cnpj', cnpj)
    if user.tell != tell:
        user.setAttr('_phone', tell)
    if user.email != email:
        user.setAttr('_email', email)
    if user.ramo != ramo:
        user.setAttr('_ramo', ramo)
    if user.tamanho != tamanho:
        user.setAttr('_tamanho', tamanho)
    if user.nomeRep != rep:
        user.setAttr('_nomeRep', rep)

    return render_template('portalCliente.html', user=user)
    