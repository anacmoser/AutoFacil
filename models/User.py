class User:
    def __init__(self, id, perfil):
        self._id = id
        self._perfil = perfil

    @property
    def id(self):
        return self._id
    
    @property
    def perfil(self):
        return self._perfil
    


     
        
        
        