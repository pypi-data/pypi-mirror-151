from os import path
class Extension: 
    def __init__(self, id : int, name : str) -> None:
        self.id : int = id
        self.name : str = name
        pass

    def toJson(self) -> str:
        try : 
            return '{"id": "'+ str(self.id)+'", "name": "'+self.name+'"}'
        except :
            print("Error in Extension.toJson()")
            
    @staticmethod
    def getExtension(p) -> str:
        '''
        Permet de récupérer l'extension d'un fichier

        Retourne:
            - l'extension du fichier    
        '''
        return path.splitext(p)[1]

