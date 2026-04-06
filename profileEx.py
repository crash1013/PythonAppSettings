"""

profileEx extends the profileApp adding functionality to modify the settings stored
in the profile using command line arguments.

"""

from appProfile import appProfile

from typing import List, Dict, Any, Union
from dataclasses import dataclass, field


import argparse

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
        """ call like this apx.parse(list(sys.argv)) 
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
        

