"""
Provides interface for managing config file
"""

import argparse
import yaml
import ast

###############################################################################
# INSTALLATION METHODS
###############################################################################

def install_config():
    """
    Run first time, establish config file etc.
    """
    print('Installing...')

###############################################################################
# CONFIG METHODS
###############################################################################

def load_config(path, readonly=True):
    """
    Load config file, passed the file's path
    """
    if readonly:
        stream = open(path, 'r')
    else:
        stream = open(path, 'r+')
    config = yaml.load(stream)
    return config

def add_scope(scope):
    """
    Add a scope to the config file
    """
    print('Adding scope to config.yml: ' + str(scope))

def add_request(request):
    """
    Add a scope to the config file
    """
    print('Adding request to config.yml: ' + str(request))

def add_folder(folder):
    """
    Add a scope to the config file
    """
    print('Adding folder to config.yml: ' + str(folder))

def add_file(file):
    """
    Add a file to the config file
    """
    print('Adding file to config.yml: ' + str(file))

###############################################################################
# SCRIPT METHODS
###############################################################################

def parse_cla():
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install',
                        help='Run setup script for the first time, bool',
                        default=True)
    # The following lines bring strings into the script from the command line.
    # This is meant to give a quick interface for appending config files
    # Dict Format = {'name':_, 'url':_}
    parser.add_argument('-s', '--scope',
                        help='Add the given dict to authentication scopes',
                        default=None)
    # Dict Format = {'name':_, 'string':_}
    parser.add_argument('-r', '--request',
                        help='Add the given dict to authentication requests',
                        default=None)
    # Dict Format = {'name':_, 'id':_}
    parser.add_argument('-fo', '--folder',
                        help='Add the given dict to authentication folders',
                        default=None)
    # Dict Format = {'name':_, 'id':_, 'type':_}
    parser.add_argument('-fi', '--file',
                        help='Add the given dict to authentication folders',
                        default=None)
    return parser.parse_args()

def dictify_args(argument_dict):
    """
    This method takes all command line arguments that were passed as strings
    and evaluates them into dictionaries using ast. There might be a better way
    of doing this using yaml directly
    """
    config_changes = {}
    for arg_key in argument_dict:
        if argument_dict[arg_key] != None:
            try:
                temp = ast.literal_eval(argument_dict[arg_key])
                config_changes[arg_key] = temp
            except ValueError:
                print('Make sure you pass the correctly formatted dict!' + 
                      'Couldn\'t parse ' + str(argument_dict[arg_key]))
    return config_changes

if __name__ == "__main__":
    ARGS = parse_cla()
    CONFIG = load_config()
    ARGUMENT_DICT = {'scope': ARGS.scope,
                     'request': ARGS.request,
                     'folder': ARGS.folder,
                     'file': ARGS.file}
    CONFIG_CHANGES = dictify_args(ARGUMENT_DICT)
    print('Making the following changes to config: ' + str(CONFIG_CHANGES))
    for config_key in CONFIG_CHANGES:
        section = CONFIG_CHANGES[config_key]
        for change in section:
            pass
