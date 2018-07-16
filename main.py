"""
Entrypoint and primary class for the application


"""
import sys
import os
import src.UI
import src.authenticate as a
import src.configuration as c
import src.requests as r
import src.utils.files as files
print("Imports Successful")

class EvaluationsApp():

    def __init__(self):
        self.allRecords = [] #This list will contain all imported records
        ###Right now passing config_path to instance of configuration
        ###When installing, make a step to set an environment variable for this
        config_path = files.full_path('utils/config.yaml')
        self.config = c.Configuration(config_path)
        self.config.load_config()
        print('Configuration Loaded')
        self.auth = a.Authenticator(self.config.config['creds_path'],
                                    self.config.config['scopes'])
        self.auth.connect()
        prefixes_path = files.full_path('utils/request_prefixes.yaml')
        self.requests = r.Requests(prefixes_path)
        self.requests.build_base_requests(self.config.config['files'])

    def authenticate(self, authenticationOptions):
        """
        Establishes secure connection to datasource
        """
        self.authenticator = auth.Authenticator()

    def buildUI(self, uiOptions):
        """
        Renders and delivers UI
        """
        pass

    def importData(self, **kwargs):
        """
        Pulls remote data for reporting, stores it internally as a list of JuryRecord objects
        """
        self.sheet = self.auth.make_get_request(self.requests.requests['MainSheet'])

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
