import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

SPREADSHEET_ID = '1ptY3qjZGlV7YpQDGm1ouObGHdOGsKSzT2CKA6gNTDPU'
CREDENTIALS_PATH = '../creds/client.json'
FOLDER_ID = '0ALe3WEFbwDkxUk9PVA'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

class Authenticator():
    """
    Authentication object which connects to Google Services

    Attributes:
        -service - Connection to Google APIs
    """

    def __init__(self, alternate_creds_path=None):
        """
        Initialize an Authenticator Object which can run REST requests against
        the Google APIs
        """
        #TODO - Load constants in a .yml rather than declaring above
        if alternate_creds_path != None:
            # Lets user overload the credentials Global Variable set at the
            # top of this file
            self.credentials_path = alternate_creds_path
        else:
            # Default behavior
            self.credentials_path = CREDENTIALS_PATH
        # First scope is for drive, second is sheets
        self.scopes = SCOPES
        self.authsession = None # Need to run self.connect() to create session
        self.requests = {}

    ###########################################################################
    # MAIN INTERFACE METHODS
    ###########################################################################
    # These are the main interface method for Authenticate. By passing a string
    # to this method, the user can run any GET request available to
    # Authenticator
    # TODO: let this method accept more parameters to build the request
    # You can always overload the default request "None" in the method call if
    # the particular method has not yet been implemented in buildRequests()

    def make_get_request(self, request=None):
        """
        Allow user to make a GET request
        """
        return self.authsession.get(request)

    def make_put_request(self, request=None):
        """
        Allow user to make a PUT request
        """
        return self.authsession.put(request)

    ###########################################################################
    # UTILITY AND MISC METHODS
    ###########################################################################
    def connect(self):
        """
        Loads credentials file and builds dictionary of requests
        """
        self.load_credentials()
        self.build_requests()

    def load_credentials(self):
        """
        Loads credentials file through google-auth. See docs for details.
        DO NOT use Python Quickstart for Google APIs, documentation is
        outdated and the oauth2client support is depricated
        """
        # Authorize the application to use Google APIs for Drive and Sheets.
        temp = service_account.Credentials.from_service_account_file(
            self.credentials_path)
        creds = temp.with_scopes(self.scopes)
        self.authsession = AuthorizedSession(creds)

    def build_requests(self):
        """
        Establishes connections to Google services.

        #TODO: Return to this method and build up a dictionary of useful
        requests to make, store these in a yml file
        """
        pass
        ##EXAMPLES##
        #get_main_spreadsheet = ('https://sheets.googleapis.com/v4/' +
        #                             'spreadsheets/' + MAIN_SPREADSHEET_ID)
        #drive_session_get = ('https://www.googleapis.com/drive/v3/' +
        #                          'files/' + FOLDER_ID)
