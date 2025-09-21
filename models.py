#Criar o model de usuários
    #funções: adicionar, excluir, pegar todos, pegar um.
    #Para adicionar a validação continua no app.py, nesse arquivo fica somente o append
#Criar o model de veículos

#No sistema terá que constar quando o veículo está disponível com base nos campos de data de reserva

#Usar fetch para a frota
#Criar id para as páginas html para jogar todo o js num arquivo só.

#Fazer filtro de preços

"""
@app.route('/filtrar')
def frota():
    # Obter parâmetros de filtro da URL
    categoria = request.form.get('categoria', '')
    marca = request.form.get('marca', '')
    modelo = request.form.get('modelo', '')
    transmissao = request.form.get('transmissao', '')
    preco_maximo = request.form.get('preco_maximo', '')
    malas_min = request.form.get('malas_min', '')
    passageiros_min = request.form.get('passageiros_min', '')
    portas_min = request.form.get('portas_min', '')
    
    # Filtrar veículos
    veiculos_filtrados = veiculos_locacao

    filtros_aplicados = {'categoria': categoria, 'marca': marca, 'modelo': modelo, 'trnamissao': transmissao}

    for veiculo in veiculos_filtrados:
        if veiculo['preco_diario'] > preco_maximo or veiculo["numero_malas"] < malas_min or veiculo['numero_assentos'] < passageiros_min or veiculo['numero_portas'] < portas_min:
            veiculos_filtrados.remove(veiculo)
            continue

        for filtro in filtros_aplicados:
            if filtros_aplicados[filtro] != '':
                if veiculo[filtro].lower() != filtros_aplicados[filtro].lower():
                    veiculos_filtrados.remove(veiculo)
                    break

    return render_template('frota.html', veiculos=veiculos_filtrados)
"""

"""id_counter = 2

veiculos_locacao = [
    {
        "categoria": "econômico",
        "marca": "Fiat",
        "modelo": "Argo",
        "transmissao": "manual",
        "preco_diario": 89.90,
        "nome": "Fiat Argo 1.0",
        "imagem": "https://exemplo.com/imagens/fiat-argo.jpg",
        "numero_malas": 1,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "econômico",
        "marca": "Volkswagen",
        "modelo": "Gol",
        "transmissao": "automático",
        "preco_diario": 99.90,
        "nome": "VW Gol 1.0 Automatic",
        "imagem": "https://exemplo.com/imagens/vw-gol.jpg",
        "numero_malas": 1,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "sedan",
        "marca": "Toyota",
        "modelo": "Corolla",
        "transmissao": "automático",
        "preco_diario": 159.90,
        "nome": "Toyota Corolla Altis",
        "imagem": "https://exemplo.com/imagens/toyota-corolla.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "sedan",
        "marca": "Honda",
        "modelo": "Civic",
        "transmissao": "automático",
        "preco_diario": 169.90,
        "nome": "Honda Civic Touring",
        "imagem": "https://exemplo.com/imagens/honda-civic.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "indisponível"
    },
    {
        "categoria": "suv",
        "marca": "Jeep",
        "modelo": "Compass",
        "transmissao": "automático",
        "preco_diario": 199.90,
        "nome": "Jeep Compass Limited",
        "imagem": "https://exemplo.com/imagens/jeep-compass.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "suv",
        "marca": "Toyota",
        "modelo": "RAV4",
        "transmissao": "automático",
        "preco_diario": 219.90,
        "nome": "Toyota RAV4 Hybrid",
        "imagem": "https://exemplo.com/imagens/toyota-rav4.jpg",
        "numero_malas": 3,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "luxo",
        "marca": "BMW",
        "modelo": "Série 3",
        "transmissao": "automático",
        "preco_diario": 349.90,
        "nome": "BMW 320i Sport",
        "imagem": "https://exemplo.com/imagens/bmw-serie3.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "luxo",
        "marca": "Mercedes-Benz",
        "modelo": "Classe C",
        "transmissao": "automático",
        "preco_diario": 379.90,
        "nome": "Mercedes C200 Exclusive",
        "imagem": "https://exemplo.com/imagens/mercedes-classe-c.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "indisponível"
    },
    {
        "categoria": "pick-up",
        "marca": "Toyota",
        "modelo": "Hilux",
        "transmissao": "manual",
        "preco_diario": 189.90,
        "nome": "Toyota Hilux CD 2.8",
        "imagem": "https://exemplo.com/imagens/toyota-hilux.jpg",
        "numero_malas": 1,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "pick-up",
        "marca": "Ford",
        "modelo": "Ranger",
        "transmissao": "automático",
        "preco_diario": 199.90,
        "nome": "Ford Ranger XLT",
        "imagem": "https://exemplo.com/imagens/ford-ranger.jpg",
        "numero_malas": 1,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "econômico",
        "marca": "Renault",
        "modelo": "Kwid",
        "transmissao": "manual",
        "preco_diario": 79.90,
        "nome": "Renault Kwid Zen",
        "imagem": "https://exemplo.com/imagens/renault-kwid.jpg",
        "numero_malas": 1,
        "numero_passageiros": 4,
        "numero_portas": 4,
        "status": "disponível"
    },
    {
        "categoria": "suv",
        "marca": "Hyundai",
        "modelo": "Creta",
        "transmissao": "automático",
        "preco_diario": 179.90,
        "nome": "Hyundai Creta Pulse",
        "imagem": "https://exemplo.com/imagens/hyundai-creta.jpg",
        "numero_malas": 2,
        "numero_passageiros": 5,
        "numero_portas": 4,
        "status": "disponível"
    }
]
"""