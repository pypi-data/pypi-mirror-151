'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : FolderImport.py
    - Parcour un dossier donné et listes les fichiers
    - Permet ensuite d'archiver le dossier dans l'archive
'''
import os
from Archiver.Resource import Resource

class FolderImport : 
    def __init__(self, path) -> None:
        '''
            Constructeur de la classe FolderImport

            Paramètres:
                - path: le chemin du dossier à parcourir
        '''
        self.path : str = path
        self.nbResource : int = 0
        self.resources : list = self.__getResources()
        pass

    def __getResources(self) -> list:
        '''
            Permet de récupérer les ressources d'un dossier

            Retourne:
            - la liste des ressources
        '''
        myFile = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if not(file.startswith('.')):
                    dir = os.path.join(root, file)
                    self.nbResource += 1
                    new = Resource(dir, False)
                    myFile.append(new)
                    #print(new)
        return myFile
