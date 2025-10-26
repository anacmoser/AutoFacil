class Colaborador:
    def __init__(self, id, nome, perfil, cargo):
        self._id = id
        self._nome = nome
        self._perfil = perfil
        self._cargo = cargo

    @property
    def id(self):
        return self._id
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def perfil(self):
        return self._perfil
    
    @property
    def cargo(self):
        return self._cargo
    
admin = Colaborador('id', 'ana', 'colaborador', 'admin')

Colaboradores = [admin]