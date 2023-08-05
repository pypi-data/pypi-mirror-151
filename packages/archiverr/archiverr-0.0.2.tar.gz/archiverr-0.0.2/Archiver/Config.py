from configparser import ConfigParser

import Archiver.Constants as Constants
from os import path
class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config_file = Constants.NAME_OF_CONFIG_FILE
        
        
        if not path.isfile(Constants.NAME_OF_CONFIG_FILE):
            self.__initSectionsAndOptions()

        self.config.read(Constants.NAME_OF_CONFIG_FILE)
        pass

    def getOption(self, section, option):
        return self.config.get(section, option)
    
    def setOption(self, section, option, value):
        self.config.set(section, option, value)
        self.__updateConfig()
        pass

    def __initSectionsAndOptions(self):
        for section in Constants.DICT_OF_CONFIG_SECTIONS:
            if not self.config.has_section(section):
                self.__addSection(section)
            for option in Constants.DICT_OF_CONFIG_SECTIONS[section]:
                if not self.config.has_option(section, option):
                    self.setOption(section, option, Constants.DICT_OF_CONFIG_SECTIONS[section][option])
        self.__updateConfig()
        
        pass

    def __addSection(self, section):
        self.config.add_section(section)
        pass

    def __updateConfig(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        self.config.read(Constants.NAME_OF_CONFIG_FILE)
        pass