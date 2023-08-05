from os import path
class PathName: 
    def __init__(self, id, path) -> None:
        self.id : int = id
        self.path : str = path
        pass


    def getFolders(self) -> list:
        '''
        Permet de récupérer les dossiers d'un dossier
        
        Retourne:
            - la liste des dossiers
        '''
        return self.path.split("/")
    
    def toJson(self) -> str:
        try:
            return '{"id": "'+ str(self.id)+'", "name": "'+self.path+'"}'
        except :
            print("Error in PathName.toJson()")


    @staticmethod
    def getPathName(p) -> str:
        '''
            Permet de récupérer le chemin du repertoire du fichier @TODO
        
            Paramètres:
                - p: le chemin du fichier
            
            Retourne:
                - le chemin du repertoire du fichier
        '''
        return path.dirname(p)