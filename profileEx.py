"""

profileEx extends the profileApp adding functionality to modify the settings stored
in the profile using command line arguments.

"""

import logging
import sys
from appProfile import appProfile

from typing import List, Dict, Any, Union
from dataclasses import dataclass, field


import argparse

from initLogger import init_logger

@dataclass
class arg_descriptor:
    section: str
    item: str
    short_option: str
    long_option: str
    enable_arg: bool
    help_info: str = field(default="This string is displayed when help is invoked")

class profileEx(appProfile):
    """ profileEx extends the profileApp adding functionality to modify the settings stored
    in the profile using command line arguments. 
    """

    def __init__(self, descriptors: List[arg_descriptor] = []):
        super().__init__()        
        self.arg_descriptors = [ d for d in descriptors if isinstance(d, arg_descriptor)]
        self.parser: argparse.ArgumentParser = self.init_argparse()
        self.args: Union[argparse.Namespace, None] = None

    def init_argparse(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Command line options for profileEx")
        for d in self.arg_descriptors:
            if d.enable_arg:
                parser.add_argument("-" + d.short_option, "--" + d.long_option, help=d.help_info, required=False)
            else:
                parser.add_argument("-" + d.short_option, "--" + d.long_option, help=d.help_info, action="store_true", required=False)
        return parser

    def set_descriptors(self, descriptors) -> bool:
        self.arg_descriptors = [ d for d in descriptors if isinstance(d, arg_descriptor)]
        return len(self.arg_descriptors) > 0

    def add_descriptor(self, section, item, short_option, long_option, enable_arg, help_arg):
        assert(isinstance(section, str))
        assert(isinstance(item, str))
        assert(isinstance(short_option, str))
        assert(isinstance(long_option, str))
        assert(isinstance(enable_arg, bool))
        self.arg_descriptors.append(
            arg_descriptor(
                section=section,
                item=item,
                short_option=short_option,
                long_option=long_option,
                enable_arg=enable_arg,
                help_info=help_arg
            )
        )

    def add_descriptor_list(self, descriptors):
        """ add_descriptor_list adds a list of descriptors to the current list of descriptors.
            add_descriptor_list returns True if at least one descriptor was added to the list.
        """
        new_descriptors = [ d for d in descriptors if isinstance(d, arg_descriptor) ]
        if len(new_descriptors) > 0:
            self.arg_descriptors = new_descriptors
            return True
        return False
    
    def parse(self):
        """ call like this apx.parse() 
            short options may have the option argument appended to the option -xargument or -x argument
            long options will fail if the option argument is appended to the option --optionargument will fail
            long option must be like this --option argument
        """
        self.args = self.parser.parse_args()
        for d in self.arg_descriptors:
            if d.enable_arg:
                value = getattr(self.args, d.long_option.replace("-", "_"))
                if value is not None:
                    self.set_section_data(d.section, d.item, value)
            else:
                flag = getattr(self.args, d.long_option.replace("-", "_"))
                if flag:
                    self.set_section_data(d.section, d.item, True)
                else:
                    self.set_section_data(d.section, d.item, False)
        

if __name__ == "__main__":
    from initLogger import init_logger
    test_settings = [ {"section": "id", "application": "ProfileTest", "version": 1.0, "indent": 2},
                      {"section": "general", "verbose": False} , 
                      {"section" : "settings", 
                       "testStr": "This is a test string", "testInt": 42, "testFloat": 3.14, "testBool": True, "testList": [1, 2, 3], "testDict": {"key": "value"}}
                    ]
    test_descriptors: list[arg_descriptor] = [
        arg_descriptor(
            section="id",
            item="application",
            short_option="a",
            long_option="application",
            enable_arg=True,
            help_info="Set the application name"
        ),
        arg_descriptor(
            section="general",
            item="verbose",
            short_option="v",
            long_option="verbose",
            enable_arg=False,
            help_info="Enable verbose output"
        ),
        arg_descriptor(
            section="settings",
            item="testStr",
            short_option="s",
            long_option="testStr",
            enable_arg=True,
            help_info="Set the test string"
        ),
        arg_descriptor(
            section="settings",
            item="testInt",
            short_option="i",
            long_option="testInt",
            enable_arg=True,
            help_info="Set the test integer"
        ),
        arg_descriptor(
            section="settings",
            item="testFloat",
            short_option="f",
            long_option="testFloat",
            enable_arg=True,
            help_info="Set the test float"
        ),
        arg_descriptor(
            section="settings",
            item="testBool",
            short_option="b",
            long_option="testBool",
            enable_arg=False,
            help_info="Set the test boolean"
        ),
        arg_descriptor(
            section="settings",
            item="testList",
            short_option="l",
            long_option="testList",
            enable_arg=True,
            help_info="Set the test list"
        ),
        arg_descriptor(
            section="settings",
            item="testDict",
            short_option="d",
            long_option="testDict",
            enable_arg=True,
            help_info="Set the test dictionary"
        )
    ]
    logger: logging.Logger = init_logger("ProfileTest", level=logging.DEBUG)
    logger.info("***** Creating the profile *****")

    apx = profileEx(descriptors=test_descriptors)
    apx.set_app_name(sys.argv[0])
    for s in test_settings:
        for k, v in s.items():
            logger.info(f"Setting section {s['section']}, item {k} to value {v}")
            section = str(s["section"])
            if k != "section":
                logger.info(f"Setting section {section}, item {k} to value {v}")
                apx.set_section_data(section, k, v)
    apx.set_descriptors(test_descriptors)
    logger.info("Loading the settings file")
    apx.load_settings_file()
    apx.parse()