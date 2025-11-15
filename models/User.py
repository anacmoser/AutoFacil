class User:
    def __init__(self, id, perfil, senha, email):
        self._id = id
        self._perfil = perfil
        self._senha = senha
        self._email = email

    @property
    def id(self):
        return self._id
    
    @property
    def perfil(self):
        return self._perfil
    
    @property
    def senha(self):
        return self._senha
    
    @property
    def email(self):
        return self._email
    


     
        
        
        