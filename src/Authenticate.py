from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class Authenticate():
    """
    Authentication object which connects to Google Services

    Attributes:
        -service - Connection to Google APIs
    """

    def __init__(self):
        pass

    def connect(self):
        self.loadCredentials()
        self.authenticateGoogle()
        self.testConnection()

    def loadCredentials(self):
        """
        Locates Credentials file on local filesystem
        """
        creds = '/creds/client_secret.json'

    def authenticateGoogle(self, CREDS_PATH):
        """
        Establishes connection to Google services.

        Parameters:
            -CREDS_PATH - Path to the secure credentials json file 
        """
        #Authorize the application to use Google APIs for Drive and Sheets.
        scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']
        store = file.Storage(CREDS_PATH)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(CREDS_PATH, scopes)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

    def testConnection(self):
        """
        Tests connection to Google Services
        """
        FOLDER_ID = '1MRkFFn1zyaycxv-pswrP9qJT5WujFqLu'
        SPREADSHEET_ID = '1ptY3qjZGlV7YpQDGm1ouObGHdOGsKSzT2CKA6gNTDPU'
        #Drive

        #Sheets
        try:
            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='A1:A1').execute()
        except e:
            print(e)

