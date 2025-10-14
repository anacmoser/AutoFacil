class Veiculo: 
    def __init__(self, id, tipo, categoria, marca, modelo, transmissao, precoDiario, nome, imagem, nMalas, nPasageiros, nPortas, combustivel, status):
        self._id = id
        self._tipo = tipo
        self._categoria= categoria
        self._marca = marca
        self._modelo = modelo
        self._transmissao = transmissao
        self._precoDiario = precoDiario
        self._nome = nome
        self._img = imagem
        self._nMala = nMalas   
        self._nPassageiros = nPasageiros
        self._nPortas = nPortas
        self._combustivel = combustivel
        self._status = status  

    @property
    def id(self):
        return self._id
    
    @property
    def tipo(self):
         return self._tipo
    
    @property
    def categoria(self):
         return self._categoria
    
    @property
    def marca(self):
         return self._marca
    
    @property
    def modelo(self):
         return self._modelo
    
    @property
    def transmissao(self):
         return self._transmissao

    @property
    def preco(self):
         return self._precoDiario
    
    @property
    def nome(self):
         return self._nome
    
    @property
    def imagem(self):
         return self._img
    
    @property
    def malas(self):
         return self._nMala
    
    @property
    def passageiros(self):
         return self._nPassageiros
    
    @property
    def portas(self):
         return self._nPortas
    
    @property
    def combustivel(self):
         return self._combustivel
    
    @property
    def status(self):
         return self._status

    @preco.setter
    def novoPreco(self, value):
        if value < 0:
            raise ValueError("Preço não pode ser negativo")
        self._precoDiario = value

    @id.setter
    def novoId(self, value):
        for vei in VEICULOS:
            if vei.id == value:
                raise ValueError(f'O id {value} já está em uso')
        self._id = value

    @status.setter   #Usar quando alugarem um veículo
    def sttUpdate(self):
        if self._status == 'disponível':
            self._status = 'indisponível'
        else:
            self._status = 'disponível'
             
    
    
    """def setVeiAtt(self, campo, novoValor):
        if campo in self.campos:
            setattr(self, campo, novoValor)
        else:
            return False
"""
VEICULOS = [Veiculo(1, "econômico", "Econômico", "Fiat", "Mobi", "manual", 95.00, "Fiat Mobi", "https://production.autoforce.com/uploads/version/profile_image/10921/model_main_webp_comprar-like-1-0_9eee82ebb4.png.webp", 2, 5, 4, "Flex", "disponível"),
            Veiculo(2, "econômico", "Econômico","Renault", "Kwid", "manual", 100.00,"Renault Kwid","https://www.webmotors.com.br/imagens/prod/348031/RENAULT_KWID_1.0_12V_SCE_FLEX_OUTSIDER_MANUAL_34803110315083122.webp", 2, 5, 4, "Flex","disponível"),
            Veiculo(3, "econômico", "Econômico", "Hyundai", "HB20", "manual", 110.00, "Hyundai HB20", "/static/img/hb20.webp", 3, 5, 4, "Flex", "disponível"),
            Veiculo(4, "econômico", "Econômico", "Chevrolet", "Onix", "manual", 115.00, "Chevrolet Onix", "/static/img/onix.png", 3, 5, 4, "Flex", "disponível"),
            Veiculo(5, "econômico", "Econômico", "Volkswagen", "Gol", "manual", 105.00, "Volkswagen Gol", "https://cdn.motor1.com/images/mgl/YAAopq/s3/volkswagen-gol-1.0-2023.jpg", 2, 5, 4, "Flex", "disponível"),
            Veiculo(6, "sedan", "Sedan", "Toyota", "Corolla", "automático", 180.00, "Toyota Corolla", "/static/img/corolla.png", 3, 5, 4, "Gasolina", "disponível"),
            Veiculo(7, "sedan", "Sedan", "Honda", "Civic", "automático", 185.00, "Honda Civic", "https://di-uploads-pod33.dealerinspire.com/hendrickhondacharlotte/uploads/2021/03/mlp-img-top-2021-civic.png", 3, 5, 4, "Gasolina", "disponível"),
            Veiculo(8, "sedan", "Sedan", "Nissan", "Sentra", "automático", 170.00, "Nissan Sentra", "https://www.nissan-cdn.net/content/dam/Nissan/br/site/veiculos/sentra-my25/thumbs/sentra_exclusive_int_premium.png", 3, 5, 4, "Flex", "disponível"),
            Veiculo(9, "sedan", "Sedan", "Chevrolet", "Cruze", "automático", 175.00, "Chevrolet Cruze", "https://revistacarro.com.br/wp-content/uploads/2018/05/chevrolet_cruze_sport6_ltz.png", 3, 5, 4, "Flex", "disponível"),
            Veiculo(10, "sedan", "Sedan", "Volkswagen", "Virtus", "automático", 165.00, "Volkswagen Virtus", "https://cadastro.motorleads.co/public/images/20240130022136-v5.png", 3, 5, 4, "Flex", "disponível"),
            Veiculo(11, "suv", "SUV", "Jeep", "Compass", "automático", 220.00, "Jeep Compass", "https://www.webmotors.com.br/imagens/prod/348683/JEEP_COMPASS_1.3_T270_TURBO_FLEX_S_AT6_3486831606189095.webp?s=fill&w=170&h=125&t=true", 4, 5, 4, "Diesel", "disponível"),
            Veiculo(12, "suv", "SUV", "Hyundai", "Creta", "automático", 200.00, "Hyundai Creta", "https://www.webmotors.com.br/imagens/prod/348376/HYUNDAI_CRETA_1.6_16V_FLEX_ACTION_AUTOMATICO_34837618173811432.webp", 3, 5, 4, "Flex", "disponível"),
            Veiculo(13, "suv", "SUV", "Honda", "HR-V", "automático", 210.00, "Honda HR-V", "https://production.autoforce.com/uploads/version/profile_image/9408/comprar-exl-honda-sensing_f6ae5428c9.png", 3, 5, 4, "Gasolina", "disponível"),
            Veiculo(14, "suv", "SUV", "Nissan", "Kicks", "automático", 195.00, "Nissan Kicks", "https://www.nissan.com.br/content/dam/Nissan/br/site/veiculos/kicks-play/360/advance/branco-diamond/01.png.ximg.c1h.360.png", 3, 5, 4, "Flex", "disponível"),
            Veiculo(15, "suv", "SUV", "Chevrolet", "Tracker", "automático", 205.00, "Chevrolet Tracker", "https://www.autoclachevrolet.com.br/content/dam/chevrolet/sa/br/pt/master/home/suvs/tracker/tracker-myr-2026/2-colorizer/lt-at-turbo/chevrolet-tracker-lt-preto-ouro-negro.jpg?imwidth=1920", 3, 5, 4, "Flex", "disponível"),
            Veiculo(16, "luxo", "Luxo", "BMW", "Série 3", "automático", 450.00, "BMW Série 3", "https://www.bmw.com.br/content/dam/bmw/common/all-models/3-series/sedan/2024/navigation/bmw-3-series-ice-lci-modelfinder.png", 4, 5, 4, "Gasolina", "disponível"),
            Veiculo(17, "luxo", "Luxo", "Audi", "A4", "automático", 460.00, "Audi A4", "https://www.webmotors.com.br/imagens/prod/379665/AUDI_A4_2.0_TFSI_MHEV_S_LINE_QUATTRO_S_TRONIC_37966510582707039.webp", 4, 5, 4, "Gasolina", "disponível"),
            Veiculo(18, "luxo", "Luxo", "Mercedes-Benz", "C180", "automático", 480.00, "Mercedes-Benz C180", "https://www.webmotors.com.br/imagens/prod/347940/MERCEDESBENZ_C_180_1.6_CGI_GASOLINA_SPORT_COUPE_9GTRONIC_34794009590838032.webp", 4, 5, 4, "Gasolina", "disponível"),
            Veiculo(19, "luxo", "Luxo", "Volvo", "XC60", "automático", 500.00, "Volvo XC60", "https://www.webmotors.com.br/imagens/prod/348860/VOLVO_XC60_2.0_T8_RECHARGE_POLESTAR_ENGINEERED_AWD_GEARTRONIC_34886011041803311.webp", 4, 5, 4, "Híbrido", "disponível"),
            Veiculo(20, "luxo", "Luxo", "Jaguar", "XE", "automático", 520.00, "Jaguar XE", "https://www.webmotors.com.br/imagens/prod/348195/JAGUAR_XE_2.0_16V_INGENIUM_P250_GASOLINA_RDYNAMIC_S_4P_AUTOMATICO_34819510562480227.webp", 4, 5, 4, "Gasolina", "disponível")
            ]

def addVeiculo(veiculo): #Como em users, veículo é um objeto da classe veiculo
        VEICULOS.append(veiculo)

def removerVeiculo(id):
        for veiculo in VEICULOS:
            if veiculo.id == id:
                VEICULOS.remove(veiculo)
            else:
                return 'Veículo não encontrado'
            
def getVeiById(id):
        for veiculo in  VEICULOS:
            if id == veiculo.id:
                return veiculo
        return 'Nenhum id correspondente'