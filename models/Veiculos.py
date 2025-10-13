from models.Veiculo import Veiculo

class Veiculos:
    def __init__(self):
        self.veiculos = []

    def getVeiculos(self):
        return self.veiculos

    def adicionar(self, veiculo): #Como em users, veículo é um objeto da classe veiculo
        self.veiculos.append(veiculo)
    
    def remover(self, id):
        for veiculo in self.veiculos:
            if veiculo.id == id:
                self.veiculos.remove(veiculo)
            else:
                return 'Veículo não encontrado'

    def getVeiById(self, id):
        for veiculo in self.veiculos:
            if id == veiculo.id:
                return veiculo
        return 'Nenhum id correspondente'