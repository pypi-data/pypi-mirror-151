from Archiver import myConfig
from Archiver.Utilities import Utilities
from Archiver.Resource import Resource
from Archiver.FolderImport import FolderImport
from Archiver.Archive import Archive
from Archiver.Metadata import Metadata
import Archiver.Constants as Constants

from toml import load
from datetime import datetime, timezone
from time import mktime
import getopt
import sys
from os import system
from os.path import exists, abspath, isdir, isfile

def main():
    '''
    Main function of Archiver.
    '''
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    commands = load(open(Constants.NAME_OF_COMMANDS_FILE))
    
    # Options
    options = commands["commands"]["short_options"]
 

    # Long options
    long_options = commands["commands"]["long_options"]


    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        if len(arguments) == 0:
            raise Exception("No arguments given")
        currentArgument = arguments[0][0]

        if currentArgument in (commands["new"]["short_option"], commands["new"]["long_option"]):
            nameHidden = Utilities.getHiddenArchiveName(values[0])
            if Utilities.checkIfArchiveExist(nameHidden):
                raise Exception(Constants.MESSAGE_ARCHIVE_ALREADY_EXIST)
            Archive(nameHidden)

        elif currentArgument in (commands["import"]["short_option"], commands["import"]["long_option"]):
            Utilities.checkCurrentArchive()
            absPath = abspath(values[0])
            nameOfArchive = myConfig.getOption(
                Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)

            Utilities.checkPath(absPath)
            if not exists(absPath):
                raise Exception(Constants.MESSAGE_FOLDER_FILE_DOES_NOT_EXIST)
            if isdir(absPath):
                myArchive = Archive(nameOfArchive)
                myArchive.archiveFolder(FolderImport(absPath))
            elif isfile(absPath):
                Archive(nameOfArchive).archiveResource(
                    Resource(absPath, False))

        elif currentArgument in (commands["merge"]["short_option"], commands["merge"]["long_option"]):
            nameHidden1 = Utilities.getHiddenArchiveName(values[0])
            nameHidden2 = Utilities.getHiddenArchiveName(values[1])
            if not Utilities.checkIfArchiveExist(nameHidden1):
                raise Exception(Constants.MESSAGE_ARCHIVE_FIRST_DOES_NOT_EXIST)

            if not Utilities.checkIfArchiveExist(nameHidden2):
                raise Exception(
                    Constants.MESSAGE_ARCHIVE_SECOND_DOES_NOT_EXIST)

            Archive(nameHidden1) + Archive(nameHidden2)

        elif currentArgument in (commands["search"]["short_option"], commands["search"]["long_option"]):
            Utilities.checkCurrentArchive()
            filters = dict()
            if len(values) != 0:
                filters = dict(x.split(':') for x in values)                     
            myArchive = Archive(myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME))
            resources = myArchive.search(filters)
            
            myArchive.saveToExtract(resources)
            for res in resources:
                print(res.fileName.name+res.extension.name)
            # @TODO
            pass
        elif currentArgument in (commands["extract"]["short_option"], commands["extract"]["long_option"]):
            Utilities.checkCurrentArchive()
            resources = []
            #absPath = abspath(values[0])
            nameOfArchive = myConfig.getOption(
                Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)
            myArchive = Archive(nameOfArchive)
            arraySha1AndIdMeta = myArchive.loadFromFileToExtract()
            for sha1AndIdMeta in arraySha1AndIdMeta:
                resources.append(myArchive.getResourceBySha1WithMetadataById(sha1AndIdMeta[0], sha1AndIdMeta[1]))
            myArchive.extractResources(resources)
            pass

        elif currentArgument in (commands["update"]["short_option"], commands["update"]["long_option"]):
            # @TODO
            pass

        elif currentArgument in (commands["choose"]["short_option"], commands["choose"]["long_option"]):
            nameHidden = Utilities.getHiddenArchiveName(values[0])
            if not Utilities.checkIfArchiveExist(nameHidden):
                raise Exception(Constants.MESSAGE_ARCHIVE_DOES_NOT_EXIST)
            myConfig.setOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME, nameHidden)
            pass
        
        elif currentArgument in commands["man"]["long_option"]: #currentArgument in (commands["man"]["short_option"],
            nameOfCmd = ""
            if len(values) != 0:
                nameOfCmd = values[0]
            Utilities.displayManPage(nameOfCmd)
        
        elif commands["serve"]["long_option"]:
            Utilities.startServer()
            pass

        elif currentArgument in (commands["list"]["short_option"], commands["list"]["long_option"]):
            for archive in Utilities.listArchivesInFolder():
                print(archive)
            pass

    except Exception as err: #Exepction
        # output error, and return with an error code
        # @TODO : Print usage manual
        if err != None:
            print(err)
            sys.exit() 
        else:
            Utilities.displayManPage()
            sys.exit()
        pass




    '''
    
    myArchiveA = Archive("archiveA")
    myFolderA = FolderImport("A")
    myArchiveA.archiveFolder(myFolderA)


    myArchiveB = Archive("./archiveB")
    myFolderB = FolderImport("./B")
    myArchiveB.archiveFolder(myFolderB)

    # myArchiveC = myArchiveA + myArchiveB

    
    betweenDate = {"start": "2022/04/06", "end": "2022/04/07"}

    betweenSize = {"start": "1", "end": "200000000000", "unit": "B"}

    options = {"size": betweenSize}
    
    reslut = myArchiveA.search(options)
    
    myArchiveA.extractResources(reslut)
   

    myArchiveB = Archive("./archiveB")
    myFolderB = FolderImport("./B")
    myArchiveB.archiveFolder(myFolderB)

    myArchiveC = myArchiveA + myArchiveB
   
    for r in reslut:
       
        print("name: " + r.universalMetadata.name)
        print("size: " + str(r.universalMetadata.size))
        print("extension: " + r.universalMetadata.extension)
        print("\n")
    
    myArchiveB = Archive("./archiveB")
    myFolderB = FolderImport("./B")
    myArchiveB.archiveFolder(myFolderB)

    myArchiveC = myArchiveA + myArchiveB

    myArchiveB.extractResource("metadataExistmetadataExist")

    
    currentArchvive = None
    while true:
        x = input("Entrez une commande:")
        match x:
            case "exit":
                break

            case "select":
                currentArchvive = Archive(input("Entrez le chemin de l'archive:"))
                print("Archive selectionnée")
            case "create":
                path = input("Entrez le chemin de l'archive:")
                Archive(path)
            
            case "import":
                if currentArchvive is None:
                    print("Vous devez séléctionner une archive avant d'importer des fichiers")
                else:
                    path = input("Entrez le chemin du dossier à importer:")
                    FolderImport(path)
    '''






