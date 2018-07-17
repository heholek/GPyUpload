"""
Entrypoint and primary class for the application


"""
import sys
import os
import src.UI
import src.authenticate as a
import src.configuration as c
import src.importer as i
import src.requests as r
import src.util as util
import weakref
print("Imports Successful")

class App():

    def __init__(self):
        ###Right now passing config_path to instance of configuration
        ###When installing, make a step to set an environment variable for this
        pass

    def register_classes(self):
        config_path = util.full_path('src/config/main.yaml')
        self.config = c.Configuration(config_path, app=weakref.ref(self))
        self.config.load_config()
        print('Configuration Loaded')
        self.auth = a.Authenticator(self.config.config['creds_path'],
                                    self.config.config['scopes'],
                                    app=weakref.ref(self))
        self.auth.connect()
        prefixes_path = util.full_path('src/config/request_prefixes.yaml')
        self.requests = r.Requests(prefixes_path, app=weakref.ref(self))
        self.requests.build_base_requests(self.config.config['files'])

    def buildUI(self, uiOptions):
        """
        Renders and delivers UI
        """
        pass

    def importData(self, **kwargs):
        """
        Pulls remote data for reporting, stores it internally as a list of JuryRecord objects
        """
        self.importer = i.Importer(self.config.config['files'],
                                   app=weakref.ref(self))

    def buildReports(self, buildOptions):
        """
        Assembles reports and renders pdfs

        After this function, user can explore the temp directory to find all reports currently staged for delivery

        Iterate through self.allRecords and call BuildReport
        """
        pass

    def deliverReports(self, deliveryOptions):
        """
        Iterates through reports staged for delivery and deliver them to the appropriate parties
        """
        pass
