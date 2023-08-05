from email import utils
from os import chmod, listdir, walk, system, getcwd, chdir
from os.path import exists, isdir, isfile, join
import Archiver.Constants as Constants
from Archiver import myConfig


class Utilities:

    @staticmethod
    def startServer():
        """Start the server.
        """
        path = getcwd()
        chdir(Constants.PATH_TO_SERVER)
        print(getcwd())
        system("flask run")
        chdir(path)

    @staticmethod
    def displayManPage(nameOfCmd=None):
        if nameOfCmd is None:
            msg = "Usage: Archiver [OPTION]... [ARCHIVE]...\n"
        else:
            match nameOfCmd:
                case "New":
                    msg = "Usage: Archiver -n [ARCHIVE]\n"
                case "Import":
                    msg = "Usage: Archiver -i [ARCHIVE] [FOLDER]\n"
                case "Merge":
                    msg = "Usage: Archiver -m [ARCHIVE1] [ARCHIVE2]\n"
                case "Extract":
                    msg = "Usage: Archiver -e [ARCHIVE] [FOLDER]\n"  # @TODO
                case "Search":
                    msg = "Usage: Archiver -s [ARCHIVE] [KEYWORD]\n"  # @TODO
                case "Update":
                    msg = "Usage: Archiver -u [ARCHIVE]\n"  # @TODO
                case "Choose":
                    msg = "Usage: Archiver -c [ARCHIVE]\n"
                case __:
                    # Display entire help
                    msg = """ Usage : archiver [COMMAND] [ARGS]

                    Archiver - System for archiving files and folders

                    Commands:
                        -n, --new [ARCHIVE]   Create a new archive
                        -i, --import [ARCHIVE] [FOLDER]  Import a folder into an archive
                        -m, --merge [ARCHIVE1] [ARCHIVE2]  Merge two archives
                        -e, --extract [FOLDER]  Extract an archive into a folder
                        -s, --search [KEYWORD]  Search an archive for a keyword
                        -u, --update Update an archive
                        -c, --choose [ARCHIVE]  Choose an archive to work with
                        --man [COMMAND] Displays the man page of a command
                    """

        print(msg)
        pass

    @staticmethod
    def getPathOfArchive(archiveName):
        '''
        Retourne le dossier de l'archive cachée.

        paramètre:
            - archiveName: nom de l'archive cachée (.)

        retourne:
            - dossier de l'archive cachée
        '''
        return myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR) + "/" + archiveName

    @staticmethod
    def checkIfArchiveExist(archiveName):
        '''
        Vérifie si une archive existe.

        paramètres:
            - archiveName: name of the archive to check.

        retourne:
            - Vrai si l'archive existe, sinon faux.
        '''
        pathOfArchive = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR) + "/" + archiveName
        if exists(pathOfArchive):
            return True
        else:
            return False

    @staticmethod
    def getHiddenArchiveName(name):
        return Constants.HIDDEN_ARCHIVE_PREFIX + name

    @staticmethod
    def getArchiveName(name):
        return name[1:]

    @staticmethod
    def listArchivesInFolder():
        '''
        List all archives in a folder.
        '''
        folder = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR)
        if not exists(folder):
            raise Exception("Archive folder does not exist")

        if not isdir(folder):
            raise Exception("Folder is not a directory.")
        archives = []
        for folder in listdir(folder):
            archives.append(Utilities.getArchiveName(folder))
        return archives

    @staticmethod
    def checkCurrentArchive():
        name = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)
        if name == "":
            raise Exception(Constants.MESSAGE_NO_CURRENT_ARCHIVE)
        elif not Utilities.checkIfArchiveExist(name):
            raise Exception(Constants.MESSAGE_ARCHIVE_DOES_NOT_EXIST)

    @staticmethod
    def checkPath(archiveName):
        if exists(archiveName):
            return True
        return False

    @staticmethod
    def changeRightToReadOnly(path):
        #system('chmod -R 444 ' + path + '/*')

        chmod(path,0o444)#chmod(path, 0o555)
        pass

    @staticmethod
    def changeRightToReadWrite(path):
        #system('chmod -R 777 ' + path + '/*')
        chmod(path, 0o777) #0o666
        pass

    
    @staticmethod
    def changeAllRightFileAndFolderToReadWrite(path):
        Utilities.changeRightToReadWrite(path)
        for root, dirs, files in walk(path):
            for d in dirs:
                Utilities.changeRightToReadWrite(join(root, d))
            for f in files:
                Utilities.changeRightToReadWrite(join(root, f))
        pass
    
    @staticmethod
    def changeAllRightFileAndFolderToReadOnly(path):
        onlyfiles = [f for f in walk(path) if isfile(join(path, f))]
        for f in onlyfiles:
            Utilities.changeRightToReadOnly(f)
                #Utilities.changeRightToReadOnly(join(path, f))
        '''for root, dirs, files in walk(path):
            for f in files:
                Utilities.changeRightToReadOnly(join(root, f))
            for d in dirs:
                Utilities.changeAllRightFileAndFolderToReadOnly(join(root, d))
                #Utilities.changeRightToReadOnly(join(root, d))
        Utilities.changeRightToReadOnly(path)'''
        pass