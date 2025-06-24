class LivreInexistantError(Exception):
    def __init__(self,message="Le livre n'existe pas "):
        super().__init__(message)

class LivreIndisponibleError(Exception):
    def __init__(self,message="Le livre est déja emprunté"):
        super().__init__(message)

    

class MembreInexistantError(Exception):
    def __init__(self,message="Le membre n'existe pas"):
        super().__init(message)

    
class QuotaEmpruntDepasseError(Exception):
    def __init__(self,message="Le membre a déja emprunté 3 livres ou plus"):
        super().__init__(message)