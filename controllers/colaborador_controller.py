from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, abort
from models.Colaboradores import ColaboradorDB
from models import db
from controllers.validacoes import validarEmail, validarSenha, validarCpf, validarNome

colaborador_bp = Blueprint('colaborador_bp', __name__)


# ============================
# PÁGINA DO COLABORADOR
# ============================
@colaborador_bp.route('/colaborador', methods=['GET'])
def pgColaborador():
    if not session.get('usuario_logado'):
        return render_template('colaboradores/login_colaborador.html')

    colab = ColaboradorDB.query.get(session.get('usuario_logado'))
    if not colab:
        abort(403)

    return render_template(
        'colaboradores/colaborador.html',
        id=colab.id,
        cargo=colab.cargo,
        nome=colab.nome
    )


# ============================
# LOGIN
# ============================
@colaborador_bp.route('/loginColaborador', methods=['GET'])
def loginColaborador():
    return render_template('colaboradores/login_colaborador.html')


@colaborador_bp.route('/loginColab', methods=['POST'])
def login():
    email = request.form.get('email', '')
    senha = request.form.get('password', '')
    remember = request.form.get('lembrar')

    if not email:
        return render_template('colaboradores/login_colaborador.html', erro="Email obrigatório")

    if not senha:
        return render_template('colaboradores/login_colaborador.html', erro="Senha obrigatória")

    if not validarEmail(email):
        return render_template('colaboradores/login_colaborador.html', erro="Email inválido")

    # Busca no BD
    colab = ColaboradorDB.query.filter_by(email=email).first()
    if not colab:
        return render_template('colaboradores/login_colaborador.html', erro="Colaborador não encontrado")

    if not colab.check_senha(senha):
        return render_template('colaboradores/login_colaborador.html', erro="Senha incorreta")

    # Login OK
    session['usuario_logado'] = colab.id
    session['usuario_perfil'] = colab.perfil
    session['colab_cargo'] = colab.cargo

    if remember:
        response = make_response(redirect(url_for('colaborador_bp.pgColaborador')))
        response.set_cookie('user', colab.email, max_age=60*60*72)
        response.set_cookie('perfil', colab.perfil, max_age=60*60*72)
        response.set_cookie('cargo', colab.cargo, max_age=60*60*72)
        return response

    return redirect(url_for('colaborador_bp.pgColaborador'))


# ============================
# CADASTRO
# ============================
@colaborador_bp.route('/cadastroColab', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome', '')
    cargo = request.form.get('cargo', '')
    email = request.form.get('email', '')
    senha = request.form.get('senha', '')
    verificador = request.form.get('verificar', '')
    cpf = request.form.get('cpf', '')

    campos = [nome, cargo, email, senha, verificador, cpf]
    if not all(campos):
        return render_template(
            'colaboradores/colaborador.html',
            errosCadastro="Todos os campos são obrigatórios",
            errosUpdate="",
            errosDelete=""
        )

    # Validações
    if senha != verificador:
        return render_template('colaboradores/colaborador.html', errosCadastro="Senhas não conferem")

    if not validarNome(nome):
        return render_template('colaboradores/colaborador.html', errosCadastro="Nome inválido")

    if not validarEmail(email):
        return render_template('colaboradores/colaborador.html', errosCadastro="Email inválido")

    if not validarSenha(senha):
        return render_template('colaboradores/colaborador.html', errosCadastro="Senha inválida")

    if not validarCpf(cpf):
        return render_template('colaboradores/colaborador.html', errosCadastro="CPF inválido")

    # Verifica duplicidade no BD
    if ColaboradorDB.query.filter_by(email=email).first():
        return render_template('colaboradores/colaborador.html', errosCadastro="Email já cadastrado")

    if ColaboradorDB.query.filter_by(cpf=cpf).first():
        return render_template('colaboradores/colaborador.html', errosCadastro="CPF já cadastrado")

    # Criar
    novo = ColaboradorDB(
        nome=nome,
        cargo=cargo,
        email=email,
        cpf=cpf
    )
    novo.set_senha(senha)

    db.session.add(novo)
    db.session.commit()

    return redirect(url_for('colaborador_bp.loginColaborador'))


# ============================
# UPDATE
# ============================
@colaborador_bp.route('/updateColab', methods=['POST'])
def atualizar():
    cpf = request.form.get('cpf', '')
    campo = request.form.get('campo', '')
    novoValor = request.form.get('novoValor', '')

    if not cpf or not campo or not novoValor:
        return render_template('colaboradores/colaborador.html',
                               errosCadastro="",
                               errosUpdate="Todos os campos devem ser preenchidos",
                               errosDelete="")

    colab = ColaboradorDB.query.filter_by(cpf=cpf).first()
    if not colab:
        return render_template('colaboradores/colaborador.html', errosUpdate="Colaborador não encontrado")

    # Validações específicas
    if campo == "nome":
        if not validarNome(novoValor):
            return render_template('colaboradores/colaborador.html', errosUpdate="Nome inválido")

    if campo == "email":
        if not validarEmail(novoValor):
            return render_template('colaboradores/colaborador.html', errosUpdate="Email inválido")
        if ColaboradorDB.query.filter_by(email=novoValor).first():
            return render_template('colaboradores/colaborador.html', errosUpdate="Email já usado")

    if campo == "senha":
        if not validarSenha(novoValor):
            return render_template('colaboradores/colaborador.html', errosUpdate="Senha inválida")
        colab.set_senha(novoValor)
        db.session.commit()
        return render_template('colaboradores/colaborador.html', errosUpdate="", errosCadastro="", errosDelete="")

    # Campos diretos
    setattr(colab, campo, novoValor)
    db.session.commit()

    return render_template('colaboradores/colaborador.html', errosUpdate="", errosCadastro="", errosDelete="")


# ============================
# DELETE
# ============================
@colaborador_bp.route('/excluirColab', methods=['POST'])
def excluir():
    cpf = request.form.get('cpf', '')

    if not validarCpf(cpf):
        return render_template('colaboradores/colaborador.html', errosDelete="CPF inválido")

    colab = ColaboradorDB.query.filter_by(cpf=cpf).first()
    if not colab:
        return render_template('colaboradores/colaborador.html', errosDelete="Colaborador não encontrado")

    db.session.delete(colab)
    db.session.commit()

    return render_template('colaboradores/colaborador.html', errosDelete="", errosCadastro="", errosUpdate="")


# ============================
# BUSCAR
# ============================
@colaborador_bp.route('/buscarColab', methods=['POST'])
def buscarColab():
    cpf = request.form.get('cpf', '')

    if not validarCpf(cpf):
        return render_template('colaboradores/colaborador.html', erro="CPF inválido")

    colab = ColaboradorDB.query.filter_by(cpf=cpf).first()
    if not colab:
        return render_template('colaboradores/colaborador.html', erro="Colaborador não encontrado")

    return render_template('colaboradores/colaborador.html', colaborador=colab)
