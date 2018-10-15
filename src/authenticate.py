"""
Contains class Authenticator which connects to Google Resources
"""

#import google.auth
import json
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
from authlib.client import AssertionSession, OAuth2Session
from googleapiclient.discovery import build
import webbrowser

class Authenticator():
    """
    Authentication object which connects to Google Services

    Attributes:
        self.authsession - Requests session for connecting to Google API
    """

    def __init__(self, creds_path_arg=None,
                 scopes_arg=None, app=None,
                 creds_arg=None):
        """
        Initialize an Authenticator Object which can run REST requests against
        the Google APIs
        """
        #TODO - Load constants in a .yml rather than declaring above
        if creds_arg == None:
            self.credentials_path = creds_path_arg
            self.credentials_json = None
        else:
            self.credentials_json = json.loads(creds_arg)
            self.credentials_path = None
        self.scopes = []
        self.app = app
        scope_dict = scopes_arg
        for key, value in scopes_arg.items():
            self.scopes.append(value)
        print(self.scopes)
        self.authsession = None # Need to run self.connect() to create session

    ###########################################################################
    # MAIN INTERFACE METHODS
    ###########################################################################
    # These are the main interface method for Authenticate. By passing a string
    # to this method, the user can run any GET request available to
    # Authenticator
    # TODO: let this method accept more parameters to build the request
    # You can always overload the default request "None" in the method call if
    # the particular method has not yet been implemented in buildRequests()

    def make_get_request(self, request=None, payload=None):
        """
        Allow user to make a GET request
        """
        return self.authsession.get(request, params=payload)

    def make_put_request(self, request=None, payload=None):
        """
        Allow user to make a PUT request
        """
        return self.authsession.put(request, params=payload)

    ###########################################################################
    # UTILITY AND MISC METHODS
    ###########################################################################
    def connect(self):
        """
        Loads credentials file and builds dictionary of requests
        """
        self.load_credentials()
        self.token = self.authsession.refresh_token(url='https://www.googleapis.com/oauth2/v3/token')
        return self.authsession

    def load_credentials(self, subject=None):
        #Load items from file
        with open(self.credentials_path, 'r') as f:
            creds = json.load(f)
        creds = creds['installed']
        client_id = creds['client_id']
        client_secret = creds['client_secret']
        redirect_uri = creds['redirect_uris'][0]
        token_uri = creds['token_uri']
        authorize_url = creds['auth_uri']

        #Create Authorized Session
        self.authsession = self.create_authsession(client_id,
                                                  client_secret,
                                                  self.scopes,
                                                  redirect_uri)

        #Get Authorization URL
        self.uri, self.state = self.authsession.authorization_url(authorize_url)

        #Open Authorization URL
        webbrowser.open(self.uri)

        #Get authorization Code
        code = input('Please enter code...')
        print('Using code ' + code)

        #Get access token
        self.token = self.authsession.fetch_access_token(url='https://www.googleapis.com/oauth2/v4/token',
                                            code=code)

        #Create Credentials Object
        self.creds = Credentials(self.token['access_token'])

        #Build Services
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    @classmethod
    def create_authsession(cls, client_id, client_secret, scope, redirect_uri):
        return OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect_uri=redirect_uri
        )


