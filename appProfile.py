#
# Serializes application settings to/from a json file
#

"""
   appProfile.py provides a class that is used to store your application settings.

   The application settings are stored in a JSON file as a JSON Text. The JSON Text is an array of section objects. the only requirement is that each section object contains a key named "section" with a text value that names 
   the section.
   This application follows a long history of initialization files. The section objects are the same as the sections in an  INI file.  
   The section objects contain key value pairs that are the same as the key value pairs in an INI file. 
   The JSON Text is the same as the text in an INI file. The JSON file is the same as the INI file.
   The appProfile class provides methods to read and write the settings.
   Using JSON text allows us much more flexibility in the types of data we can store. We are not limited to strings as in an INI file. We can store numbers, arrays, and objects as well as strings.
"""

import json
from os import closerange, path
import os
import pathlib
import sys
from pathlib import Path
from typing import Dict, Union, List, Any
from initLogger import init_logger

class appProfile:
    def __init__(self) -> None:
        """
        Initialize the attributes of the appProfile object to defaults.
        """
        self.b_init: bool = False
        self.b_text_valid: bool = False
        self.str_filename: str = ""
        self.str_app_name: str = ""
        self.r_app_version: float = 0.0
        self.profile_text: List[Dict[str, Any]] = [] # it is called _text but it can contain binary information

    def create_file(self) -> bool:
        """
        create_file is used internally to create the profile file if it does not exist.

        This function is called from set_app_name. It should not be called at any other time.
        """
        if not self.str_app_name:
            return False
        if not self.str_filename:
            return False
        if path.exists(self.str_filename): 
            return False
        newfile = [ {
                "section": "id",
                "application": self.str_app_name,
                "version": self.r_app_version,
                "indent": 2
            }
        ]
        try:
            with open(self.str_filename, "w") as f:
                json.dump(newfile, f)
        except (TypeError, IOError, ValueError):
            return False    

        return True

    def store_settings_file(self) -> bool:
        """
        store_settings_file is used to serialize the settings to the JSON file.
            
        At a minimum this function should be called when the application is 
        preparing to exit. It does not do any harm to invoke this function at
        anytime a setting has been modified. Doing so may protect you from data
        loss in the case something goes wrong.
        """
        result: bool = True
        if not self.str_filename:
            return False
        if not self.profile_text:
            return False
        ind = self.read_profile("id", "indent", 2)
        try:
            with open(self.str_filename, "w") as fp:
                json.dump(self.profile_text, fp, indent=ind)
        except (TypeError, IOError, ValueError):
            return False

        return result

    def load_settings_file(self):
        """
        load_settings_file is used to initialize the settings dictionaries.

        loadSettings should be called immediately after calling set_app_name.
        """
        result = True
        self.b_init = False
        self.b_text_valid = False
        if not self.str_filename:
            return False
        if not self.str_app_name:
            return False
        try:
            with open(self.str_filename, "r") as fp:
                self.profile_text = json.load(fp)
        except (TypeError, IOError, ValueError):
            result = False
        if result:
            self.b_init = True
            self.b_text_valid = True
        return result   

    def set_app_name(self, argv0: str) -> bool:
        """
        set_app_name Determines the path and filename of the settings file.

        set_app_name should be called with the command line sys.argv[0]. 
        This string contains the application name.
        set_app_name determines the home folder for the user and uses this 
        location to load and store the settings file.
        """
        p = pathlib.Path(argv0)
        self.str_app_name = p.name
        pyName = self.str_app_name
        jsonName = pyName.split('.')[0] + ".json"
        homePath = pathlib.Path.home().joinpath("."+pyName.split('.')[0])
        if not os.path.exists(homePath):
            os.makedirs(homePath, 0o775)
        self.str_filename = str(homePath.joinpath(jsonName))
        self.create_file()
        return True

    def get_section_list(self) -> List[Dict[str, Any]]:
        """
        get_section_list returns the json text item stored in the settings file.
        
        This is an array of section dictionaries.
        """
        return self.profile_text

    def get_section(self, sectionName: str) -> Dict[str, Any] | None:
        """
        get_section finds section sectionName and returns the dictionary.

        if the section is not found get_section returns None
        """
        if not isinstance(sectionName, str):
            return None
        for section in self.profile_text:
            if "section" in section:
                if section["section"] == sectionName:
                    return section
        return None

    def get_section_data(self, sectionName: str, dataName: str) -> Any:
        """
        get_section_data return the data named dataName from the named section.
        
        if the section is not found or the dataName is not found in the 
        section the function returns None.
        The user should read data from the sections using read_profile()
        Both sectionName and dataName are checked as string types.
        If the check fails None is returned
        """
        if not isinstance(sectionName, str):
            return None
        if not isinstance(dataName, str):
            return None
        section = self.get_section(sectionName)
        if section != None:
            if dataName in section:
                return section[dataName]
        return None

    def set_section_data(self, sectionName: str, dataName: str, dataValue: Any):
        """
        set_section_data writes the dataValue named dataName to sectionName.
        
        if the section is not found or the dataName is not found in the 
        section the function returns None.
        The user should write data from the sections using write_profile()
        Both sectionName and dataName are checked as string types.
        If the check fails None is returned
        """
        section = self.get_section(sectionName)
        if isinstance(section, dict):
            if isinstance(dataName, str):
                if dataName in section:
                    section[dataName] = dataValue
                    return True
        return False

    def write_profile(self, sectionName: str, keyName: str, newValue: Any):
        """
        write_profile writes the newValue named keyName to sectionName.
        
        if the section is not found or the dataName is not found in the 
        section the function creates it and then writes newValue to 
        <section>[keyName].
        """
 
        section = self.get_section(sectionName)
        if not isinstance(section, dict):
            self.profile_text.append({"section": sectionName, keyName : newValue})
        else:
            section[keyName] = newValue

    def read_profile(self, sectionName: str, keyName: str, defaultValue: Any):
        """
        read_profile returns the data named keyName from sectionName.
        
        if the section is not found or the dataName is not found in the 
        section the function creates it and writes the defualtValue into it and
        returns the defaultValue.
        """

        section = self.get_section(sectionName)
        if not isinstance(section, dict):
            self.profile_text.append({"section": sectionName, keyName : defaultValue})
            return defaultValue
        elif not isinstance(keyName, str):
            return defaultValue
        elif not keyName in section:
                section[keyName] = defaultValue
                return defaultValue
        else:
            return section[keyName]
 
if __name__ == "__main__":
    """
        Main is test code.
        This code is only executed when the module is run. Normally the class 
        AppProfile is used as a component of a larger application

        upper case => constants
        capitalized first letter => classes
        lowercase first word => method
    """
    import logging


    logger: logging.Logger = init_logger("ProfileTest", level=logging.DEBUG)
    logger.info("***** Creating the profile *****")
    profile = appProfile()
    logger.info("Setting the appName with " + sys.argv[0])
    profile.set_app_name(sys.argv[0])
    logger.info("Loading the settings file")
    profile.load_settings_file()

   
    ver = profile.get_section_data("id", "version")
    if not isinstance(ver, float):
        logger.warning("Version is not a float, setting to 0.0")
        ver = 0.0

    profile.write_profile(sectionName="settings", keyName="testStr", newValue="This is a test")
    profile.write_profile(sectionName="settings", keyName="testInt", newValue=555)
    profile.write_profile(sectionName="settings", keyName="testFloat", newValue=55.5)
    profile.write_profile(sectionName="settings", keyName="testArray", newValue=[5, 55, 555, 369])
    profile.write_profile(sectionName="settings", keyName="testObject", newValue={"key1": "value1", "key2": "value2"})

    saveOK = profile.store_settings_file()
    if not profile.load_settings_file():
        logger.error("Error opening the settings file")
    
    logger.info("application: " + profile.read_profile("id", "application", "Unknown"))
    logger.info("version:     " + str(profile.read_profile("id", "version", 0.0)))
    logger.info("json indent: " + str(profile.read_profile("id", "indent", -1)))
    
    logger.info("testStr: " + profile.read_profile("settings", "testStr", "not found"))
    logger.info("testInt: " + str(profile.read_profile("settings", "testInt", -1)))
    logger.info("testFloat: " + str(profile.read_profile("settings", "testFloat", -1.0)))
    logger.info("testArray: " + str(profile.read_profile("settings", "testArray", [-1])))
    logger.info("testObject: " + str(profile.read_profile("settings", "testObject", None)))

    logger.info("Success")

