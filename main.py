"""
Entrypoint and primary class for the application
"""

import gspread
import sys
import os
import pathlib as p
import src.authenticate as a
import src.configuration as c
import src.importer as i
import src.filemanager as f
import src.requests as r
import src.util as util
import time
import weakref
print("Imports Successful")

class App():

    def __init__(self):
        ###Right now passing config_path to instance of configuration
        ###When installing, make a step to set an environment variable for this
        self.models = []

    def register_classes(self):
        config_path = util.full_path('src/config/main.yaml')
        config_file = p.Path(config_path)
        try:
            if config_file.is_file():
                print('Found config file, loading...')
                self.config = c.Configuration(config_path, app=weakref.ref(self))
        except OSError:
            try:
                print('No config file found, installing...')
                self.config = c.Configuration(install=True)
            except:
                print('Something went wrong loading the configuration')
                sys.exit()
        except:
            print('Something went wrong loading the configuration')
            sys.exit()
        self.config.load_config()
        print('Configuration Loaded')
        app_ref = weakref.ref(self)
        self.auth = a.Authenticator(self.config.config['creds_path'],
                                    self.config.config['scopes'],
                                    app=app_ref)
        self.filemanager = f.FileManager(app=app_ref,
                                         db_path=self.config.config['db_path'],
                                         classes=self.models)
        self.auth.connect()
        prefixes_path = util.full_path('src/config/request_prefixes.yaml')
        self.requests = r.Requests(prefixes_path, app=weakref.ref(self))
        self.requests.build_base_requests(self.config.config['files'])
        self.requests.build_base_requests(self.config.config['directories'])

    def buildUI(self, uiOptions):
        """
        Renders and delivers UI
        """
        pass

    def setModels(self, models):
        """
        Sets classes contained in models directory to be used
        """
        for model in models:
            self.models.append(model)

    def importData(self, exclusions, models=[]):
        """
        Pulls remote data for reporting, stores it internally as a list of JuryRecord objects
        """
        self.directoryImporter = i.Importer(self.config.config['directories'],
                                   app=weakref.ref(self))
        self.directoryImporter.load_directories()

    def buildReports(self, model, **kwargs):
        """
        Assembles reports and renders pdfs

        After this function, user can explore the temp directory to find all reports currently staged for delivery

        Iterate through self.allRecords and call BuildReport
        """
        for group in self.filemanager.model_groups[model.__name__]:
            self.builder = b.ReportBuilder(model, group)
            self.builder.run()

    def deliverReports(self, deliveryOptions):
        """
        Iterates through reports staged for delivery and deliver them to the appropriate parties
        """
        pass
