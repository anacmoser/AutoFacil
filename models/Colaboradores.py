class Colaborador:
    def __init__(self, id, nome, cargo, email, senha):
        self._id = id
        self._nome = nome
        self._perfil = 'colab'
        self._cargo = cargo
        self._email = email
        self._senha = senha

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
    
    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha    
    
admin = Colaborador('id', 'ana', 'admin', 'admin@gmail.com', 'Senha123')

Lista_Colaboradores = [admin]