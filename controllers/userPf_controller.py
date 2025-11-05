#PESSOA FÍSICA

#Verificar se os campos estão vazios

#Função de cadastro
#função de login

from flask import Flask, Blueprint, render_template, request, session, make_response, redirect, url_for
from controllers.validacoes import validarEmail, validarCpf
from models.UserPf import USERSpf, UserPf, addUser
import re
from models.UserPf import db, UserPfDB

user_pf_bp = Blueprint('user_pf_bp', __name__)

id_counter_Pf = 2  

@user_pf_bp.route('/cadastrarPf', methods=['POST'])
def cadastro():
    # Obter dados do formulário
    Nome = request.form.get('nome', '').strip()
    Data_Nascimento = request.form.get('nascimento', '')
    CPF = re.sub(r'[^0-9]', '', request.form.get('cpf', ''))
    Telefone = re.sub(r'[^0-9]', '', request.form.get('celular', ''))
    Email = request.form.get('email', '').strip()
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

    # Verificar campos obrigatórios
    campos_obrigatorios = [Nome, Data_Nascimento, CPF, Telefone, Email, cep, logradouro, bairro, estado, cidade, senha, confirmar_senha]
    for campo in campos_obrigatorios:
        if not campo:
            return render_template('cadastro.html', erros='Todos os campos obrigatórios devem ser preenchidos')

    if not termos:
        return render_template('cadastro.html', erros='Você deve aceitar os Termos de Uso.')

    if senha != confirmar_senha:
        return render_template('cadastro.html', erros='As senhas não coincidem.')

    try:
        # Criar novo usuário e salvar no MySQL
        novo_usuario = UserPfDB(
            Nome=Nome,
            Data_Nascimento=Data_Nascimento,
            CPF=CPF,
            Telefone=Telefone,
            Email=Email,
            CEP=cep,
            Logradouro=logradouro,
            Numero=numero,
            Complemento=complemento,
            Bairro=bairro,
            Estado=estado,
            Cidade=cidade,
            Senha=senha
        )

        db.session.add(novo_usuario)
        db.session.commit()

        # Redirecionar após o cadastro bem-sucedido
        return redirect(url_for('pgLogin'))

    except Exception as e:
        db.session.rollback()
        return render_template('cadastro.html', erros=f'Erro ao cadastrar: {e}')

    # Caso algo inesperado ocorra e nada retorne antes
    return render_template('cadastro.html', erros='Ocorreu um erro inesperado ao cadastrar.')
