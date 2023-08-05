from os import path
class FileName:
    def __init__(self, id : int, fileName : str) -> None:
        self.id : int = id
        self.name : str = fileName
        pass

    def toJson(self) -> str:
        try:
            return {"id": "'+ str(self.id)+'", "name": "'+self.name+'"}
        except :
            print("Error in FileName.toJson()")
    @staticmethod
    def getFileName(p) -> str:
        '''
        Permet de récupérer le nom d'un fichier

        Retourne:
            - le nom du fichier
        '''
        return path.basename(path.splitext(p)[0])

