class Type:
    def __init__(self, id : int, name : str) -> None:
        self.id : int = id
        self.name : str = name
        pass

    @staticmethod
    def getType(p) -> str:
        ''' @TODO
        Permet de récupérer le type d'un fichier
        
        Retourne:
            - le type du fichier
        '''
        return "Default"