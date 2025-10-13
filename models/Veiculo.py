class Veiculo:
    def __init__(self, id, tipo, categoria, marca, modelo, transmissao, precoDiario, nome, imagem, nMalas, nPasageiros, nPortas, combustivel, status):
        self.id = id
        self.tipo = tipo
        self.categoria= categoria
        self.marca = marca
        self.modelo = modelo
        self.transmissao = transmissao
        self.precoDiario = precoDiario
        self.nome = nome
        self.img = imagem
        self.nMala = nMalas   
        self.nPassageiros = nPasageiros
        self.nPortas = nPortas
        self.combustivel = combustivel
        self.status = status  

        self.veiculo = {"id": self.id,
                        "tipo": self.tipo,
                        "categoria": self.categoria,
                        "marca": self.marca,
                        "modelo": self.modelo,
                        "transmissao": self.transmissao,
                        "precoDiario": self.precoDiario,
                        "nome": self.nome,
                        "imagem": self.img,
                        "nMalas": self.nMala,
                        "nPassageiros": self.nPassageiros,
                        "nPortas": self.nPortas,
                        "combustivel": self.combustivel,
                        "status": self.status}
        
        self.campos = ['id', 'tipo', 'categoria', 'marca', 'modelo', 'transmissao', 'precoDiario', 'nome', 'imagem', 'nMalas', 'nPassageiros', 'nPoetas', 'combustivel', 'status']

    def getVeiculo(self):
        return self.veiculo 

    def getVeiculoStt(self):
        return self.status
    
    def getVeiCampo(self, campo):
        if campo in self.campos:
            return getattr(self, campo)
    
    def setVeiAtt(self, campo, novoValor):
        if campo in self.campos:
            setattr(self, campo, novoValor)