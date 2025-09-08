"""
filtro:

   Pegar requisição do usuário
   Verificar se o item já estava marcado (modificar por .value)
   Caso nenhum item esteja marcado, todos os veículos são válidos

   Utilizar for para percorrer todos os itens da lista de dicionários
     Caso o user tenha especificado modelo, trazer somente daquele modelo específico
     Caso o user tenha escolhido mais de um modelo, trazer todos os modelos compatíveis, etc

    O preço aumenta a depender da temporada e antecedencia da reserva


FUNÇÕES A IMPLEMENTAR: (perguntar ao gui quais as funcionalidades que teremos)
     filtros
     calculo de preço

"""

from flask import Flask, render_template, redirect, url_for, jsonify, request
app = Flask(__name__)

#Forma provisória de obter os dados dos automóveis enquanto o banco de dados não é implementado.
#Não foi adicionado um status de reserva, visto que não temos um banco de dados para fazer tal controle.
automoveis = [ #Preencher com a tabela do Gui
        {'modelo': '', 'categoria': '', 'tamanho': '', 'passageiros': '', 'portas': '', 'cambio': '', 'local_ret': '', 'combustivel': '', 'malas': '', 'preco_base': '', 'quilometragem': ''}#cota diária de quilometros que podem ser rodados
    ]

@app.route('/api/automoveis')
def dados_automoveis():
    return jsonify(automoveis)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filtros')
def aplicar_filtros():

    filtrados = []
    filtros = ['modelo', 'categoria', 'tamanho', 'passageiros', 'portas', 'cambio', 'local_ret', 'combustivel', 'malas', 'preco_base']
    
    modeloUser = request.form('modelo')  #O name no html precisa ser 'modelo' e o value conrrespondente com algum dos valores das chaves
    categoriaUser = request.form('categoria')
    tamanhoUser = request.form('tamanho')
    passageirosUser = request.form('passageiros')
    portasUser = request.form('portas')
    cambioUser = request.form('cambio')
    local_retUser = request.form('local_rest')
    combustivelUser = request.form('combustivel')
    malasUser = request.form('malas')
    preco_baseUser = request.form('preco_base') #alguns filtros não podem ser aplicados no loop, como o preço, que varia muito. 
                                                #No filtro ele deve conter dois números, um min e um max, e o python precisa verificar se o preco de um veículo é compreendido neste intervalo de preço

    # Com os valores do input do user
    filtros_aplicados = {'modelo': modeloUser, 
                         'categoria': categoriaUser, 
                         'tamanho': tamanhoUser, 
                         'passageiros': passageirosUser, 
                         'portas': portasUser, 
                         'cambio': cambioUser, 
                         'local_ret': local_retUser, 
                         'combustivel': combustivelUser, 
                         'malas': malasUser, 
                         'preco_base': preco_baseUser}

    for item in filtros_aplicados:
        if not item:
            filtros.remove(item)

    for veiculo in automoveis:
        for filtro in filtros:
            if veiculo[filtro] == filtros_aplicados[filtro]:
                if not veiculo in filtrados:
                    filtrados.append(veiculo)
            else:
                if veiculo in filtrados:
                    filtrados.remove(veiculo)

    return jsonify(filtrados)

@app.route('/preco')
def calcular_preco():
    modeloAutomovel = request.form('modelo') #procurar um identificador unico para o automovel
    tipoQuilometragem = request.form('quilometragem')
    if tipoQuilometragem == 'ilimitada':
        adicional = 30.00 #30 reais por dia, todos os números escritos são por dia


    for automovel in automoveis:
        if automovel['modelo'] == modeloAutomovel:
            preco = automovel['preco_base']



            #Pensar em mais adicionais, como local de retriada, tipo de quilometragem e opção com seguro.
            #Estação, local de retirada e antecedência de reserva podem influenciar o preço

                


    
if __name__ == '__main__':
    app.run(debug=True)