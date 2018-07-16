"""
Contains class Authenticator which connects to Google Resources
"""

#import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

class Authenticator():
    """
    Authentication object which connects to Google Services

    Attributes:
        self.authsession - Requests session for connecting to Google API
    """

    def __init__(self, creds_path_arg=None,
                 scopes_arg=None):
        """
        Initialize an Authenticator Object which can run REST requests against
        the Google APIs
        """
        #TODO - Load constants in a .yml rather than declaring above
        self.credentials_path = creds_path_arg
        self.scopes = []
        scope_dict = scopes_arg
        for key, value in scopes_arg.items():
            self.scopes.append(value)
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

