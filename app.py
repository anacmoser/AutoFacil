"""
TAREFAS:
    * Arquitetura / organização MVC                      COMPLETO: view, models
    * Api de CEP para pré-preenchimento do formulário

    * Para guardar os dados no BD, deve formatar num padrão
"""

from flask import Flask, render_template, request, redirect, url_for, session, make_response, abort
import math
from models.Veiculo import Veiculos
from models.UserPj import USERSpj
from controllers.veiculo_controller import veiculo_bp
from controllers.userPf_controller import user_pf_bp
from controllers.userPj_controller import user_pj_bp
from controllers.colaborador_controller import colaborador_bp
from controllers.user_controller import user_bp
from flask import Flask, render_template, request
from models import db
from dotenv import load_dotenv
import os
from models.UserPf import UserPfDB
import cloudinary
import cloudinary.uploader


cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure=True
)


load_dotenv()  # carrega o arquivo .env

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

    
app.secret_key = 'chave_secreta_autofacil'
app.register_blueprint(veiculo_bp)
app.register_blueprint(user_pf_bp)
app.register_blueprint(user_pj_bp)
app.register_blueprint(colaborador_bp)
app.register_blueprint(user_bp)

# Rotas
@app.route('/')
def index():
    if 'usuario_logado' not in session:
        user = request.cookies.get('user', '')
        perfil = request.cookies.get('perfil')
        if user:
            session['usuario_logado'] = user
            session['usuario_perfil'] = perfil
            if perfil == 'colab':
                session['colab_cargo'] = request.cookies.get('cargo')
                return redirect(url_for('colaborador_bp.pgColaborador'))
    
    if 'usuario_logado' in session:
        if session.get('usuario_perfil') == 'colab':
            return redirect(url_for('pgColaborador'))

    return render_template('index.html')

@app.route('/aluguelMensal', methods=['GET'])
def pgAluguelMensal():
    return render_template('aluguelmensal.html')

@app.route('/empresas', methods=['GET'])
def pgEmpresas():
    return render_template('empresas.html')

@app.route('/minhasReservas', methods=['GET'])
def pgMinhasReservas():
    if session.get('usuario_logado') == None:
        abort(401)
    return render_template('minhas_reservas.html')

@app.route('/pagamento/<veiculo>', methods=['GET'])
def pgPagamento(veiculo):
    return render_template('pagamento.html', veiculo = veiculo)

@app.errorhandler(401)
def nao_autorizado(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def acesso_proibido(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def erro_interno_servidor(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

