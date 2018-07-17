"""
Provides interface for managing config file
"""

import sys
import os
import argparse
import ast
import yaml

class Configuration():

    def __init__(self, config_path=None, app=None):
        self.app = app
        if config_path == None:
            try:
                self.path = os.environ['GPYREPORT_CONFIG_PATH']
            except KeyError:
                print('''Be sure to set your environment variable for
                      GPYREPORT_CONFIG_PATH. This usually occurs during
                      installation.''')
                sys.exit()
        else:
            self.path = config_path
    ###############################################################################
    # INSTALLATION METHODS
    ###############################################################################

    def install_config(self):
        """
        Run first time, establish config file etc.
        """
        print('Installing...')

    ###############################################################################
    # CONFIG METHODS
    ###############################################################################

    def get_config(self, **kwargs):
        """
        Return config file, passed the file's path
        """
        try:
            return self.load_config(**kwargs)
        except TypeError:
            print('''Load Config didn't get a proper path. Make sure to either
                  pass a path directly to the method or set the environment
                  variable for GPYREPORT_CONFIG_PATH''')
            sys.exit()
        except FileNotFoundError:
            print('''Load Config didn't get a path to a real file. Make sure
                  the environment variable for GPYREPORT_CONFIG_PATH is
                  properly set''')
            print('Received path: ' + path)
            sys.exit()

    def load_config(self, path=None, readonly=True):
        """
        Load config file, passed the file's path
        """
        if path == None:
            if readonly:
                stream = open(self.path, 'r')
            else:
                stream = open(self.path, 'r+')
            config = yaml.load(stream)
            self.config = config
            return config
        else:
            if readonly:
                stream = open(path, 'r')
            else:
                stream = open(path, 'r+')
            config = yaml.load(stream)
            self.config = config
            return config

    def add_scope(self, scope):
        """
        Add a scope to the config file
        """
        print('Adding scope to config.yml: ' + str(scope))

    def add_request(self, request):
        """
        Add a scope to the config file
        """
        print('Adding request to config.yml: ' + str(request))

    def add_folder(self, folder):
        """
        Add a scope to the config file
        """
        print('Adding folder to config.yml: ' + str(folder))

    def add_file(self, _file):
        """
        Add a file to the config file
        """
        print('Adding file to config.yml: ' + str(_file))

    ###############################################################################
    # SPECIAL METHODS
    ###############################################################################

    def __repr__(self):
        return yaml.dump(self.config)
