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

    def __init__(self, alternate_creds_path=None):
        if alternate_creds_path != None:
            # Lets user overload the credentials Global Variable set at the
            # top of this file
            self.credentials_path = alternate_creds_path
        else:
            # Default behavior
            self.credentials_path = CREDENTIALS_PATH

    def connect(self):
        self.loadCredentials()
        self.buildService()
        self.testConnection()

    def loadCredentials(self):
        """
        Loads credentials file through oauth2client. See Google API
        Quickstarts for Python for more details
        """
        # Authorize the application to use Google APIs for Drive and Sheets.
        # First scope is for drive, second is sheets
        scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                  'https://www.googleapis.com/auth/spreadsheets.readonly']
        store = file.Storage(self.credentials_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.credentials_path,
                                                  scopes)
            self.creds = tools.run_flow(flow, store)

    def buildService(self):
        """
        Establishes connection to Google services.
        """
        self.driveService = build('drive', 'v3', http=self.creds.authorize(Http()))
        self.sheetsService = build('sheets', 'v4', http=self.creds.authorize(Http()))

    def testConnection(self):
        """
        Tests connection to Google Services
        """
        FOLDER_ID = '1MRkFFn1zyaycxv-pswrP9qJT5WujFqLu'
        SPREADSHEET_ID = '1ptY3qjZGlV7YpQDGm1ouObGHdOGsKSzT2CKA6gNTDPU'
        #Drive

        #Sheets
        try:
            spreadsheet_service = self.sheetsService.spreadsheets()
            values = spreadsheet_service.values()
            result = values.get(spreadsheetId=SPREADSHEET_ID, range='A1:A1')
            result.execute()
        except Exception as e:
            print(e)
