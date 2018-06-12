"""
Entrypoint and primary class for the application


"""
import sys
import os
import src.UI
import src.Authenticate as auth
import src.ImportData as data
import src.ReportBuilder as ReportBuilder
import src.ReportDeliverer as ReportDeliverer
print("Imports Successful")

class EvaluationsApp():

    def __init__(self):
        self.allRecords = [] #This list will contain all imported records

    def authenticate(self, authenticationOptions):
        """
        Establishes secure connection to datasource
        """
        pass

    def buildUI(self, uiOptions):
        """
        Renders and delivers UI
        """
        pass

    def importData(self, importOptions):
        """
        Pulls remote data for reporting, stores it internally as a list of JuryRecord objects
        """
        pass

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
