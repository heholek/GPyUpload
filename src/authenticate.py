"""
Contains class Authenticator which connects to Google Resources
"""

#import google.auth
import json
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from authlib.client import AssertionSession

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
        return self.authsession

    def load_credentials(self, subject=None):
        #conf_file - creds file
        #scopes
        #subject?
        with open(self.credentials_path, 'r') as f:
            creds = json.load(f)

        token_url = creds['token_uri']
        issuer = creds['client_email']
        key = creds['private_key']
        key_id = creds.get('private_key_id')

        header = {'alg': 'RS256'}
        if key_id:
            header['kid'] = key_id

        # Google puts scope in payload
        claims = {'scope': ' '.join(self.scopes)}
        self.authsession = AssertionSession(
            grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
            token_url=token_url,
            issuer=issuer,
            audience=token_url,
            claims=claims,
            subject=subject,
            key=key,
            header=header,
        )

    def load_credentials_old(self):
        """
        Loads credentials file through google-auth. See docs for details.
        DO NOT use Python Quickstart for Google APIs, documentation is
        outdated and the oauth2client support is depricated
        """
        # Authorize the application to use Google APIs for Drive and Sheets.
        if self.credentials_json == None:
            temp = service_account.Credentials.from_service_account_file(
                self.credentials_path)
        elif self.credentials_path == None:
            temp = service_account.Credentials.from_service_account_info(
                self.credentials_json)
        self.creds = temp.with_scopes(self.scopes)
        self.authsession = AuthorizedSession(self.creds)
