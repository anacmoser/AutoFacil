from models.User import User

class Users: 
    def __init__(self, users):
        self.users = users 

    #função para verificar duplicidade ds email e cpf antes do adicionar

    def getUsers(self):
        return self.users

    def adicionar(self, novoUser): #novosser é um objeto da classe user
        erros = self.verificarDuplicidade(novoUser)
        
        if erros:
            return erros  # Ou retornar False/lista de erros
        
        self.users.append(novoUser)
        return True
    
    def verificarDuplicidade(self, novoUser):
        erro = []
        for user in self.users:
            if user.cpf == novoUser.cpf:  
                erro.append('Este CPF já está em uso')
            if user.email == novoUser.email:
                erro.append('Este email já está em uso')
        return erro

    def excluir(self, cpf):
        for user in self.users:
            if user.getUserDados('cpf') == cpf:
                self.users.remove(user)
                return True
        return False

    def getUsers(self):
        return self.users
    
    def getUserByCpf(self, cpf):
        for user in self.users:
            if user.getUserDados('cpf') == cpf:
                return user
        return None, 'Usuario não encontrado'
    
    def getUserByEmail(self, email):
        for user in self.users:
            if user.getUserDados('email') == email:
                return user
        return None, 'Usuário não encontrado'
        