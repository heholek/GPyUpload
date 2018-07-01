from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

CREDENTIALS_PATH = '../creds/client_secret.json'

class Authenticator():
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
        creds = CREDENTIALS_PATH

    def authenticateGoogle(self, credentials_path):
        """
        Establishes connection to Google services.

        Parameters:
            -credentials_path - Path to the secure credentials json file 
        """
        #Authorize the application to use Google APIs for Drive and Sheets.
        scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']
        store = file.Storage(credentials_path)
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
            result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='A1:A1').execute()
        except Exception as e:
            print(e)

