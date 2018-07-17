"""
This single script gathers all the Class tests and prepares them for
execution. TODO: Get this darned thing into a nosetest suite, stat
"""

import google.auth
import src.authenticate
import src.configuration
import src.util as util
import main

AuthsessionClass = google.auth.transport.requests.AuthorizedSession

def set_up_auth():
    """
    Create auth resources for testing
    """
    creds_path = util.full_path('src/creds/client.json')
    scopes = {'test': 'https://www.googleapis.com/auth/drive.readonly'}
    auth = src.authenticate.Authenticator(creds_path_arg=creds_path,
                                          scopes_arg=scopes)
    return auth

def set_up_config():
    """
    Create auth resources for testing
    """
    config_path = util.full_path('src/config/main.yaml')
    return src.configuration.Configuration(config_path=config_path)

def test_authenticator_type(auth):
    """
    Gets passed Authenticator instance and runs the connect() method
    """
    authsession = auth.connect()
    assert isinstance(authsession, AuthsessionClass)
    return authsession

def test_authenticator_connection(auth):
    """
    Gets passed Authenticator instance and makes a request for Drive
    The decoding is a bit messy, but here's the idea: decode the response
    with json(), then access the user element from the response (in this case
    that's the only element), then access the kind of user it is.
    #TODO: Make a more robust user testing procedure that ensures permissions
    are properly set up
    """
    test = 'https://www.googleapis.com/drive/v3/about'
    p_load = {'fields':'user'}
    result = auth.make_get_request(request=test, payload=p_load)
    assert result.json()['user']['kind'] == 'drive#user'
    return result

def test_get_config_from_instance(config):
    """
    Tries to load config file from instance when it was generated in setup
    """
    config_settings = config.get_config()
    assert isinstance(config_settings, dict)
    return config_settings

def test_get_config_from_arg(config):
    """
    Tries to load config file from argument passed directly to load method
    """
    config_path = util.full_path('src/config/main.yaml')
    config_settings = config.get_config(path=config_path)
    assert isinstance(config_settings, dict)
    return config_settings

def test_main_connected():
    app = main.App()
    app.register_classes()
    app.auth.connect()
    print('Main Script Connected')

if __name__ == "__main__":
    A = set_up_auth()
    C = set_up_config()
    test_authenticator_type(A)
    test_authenticator_connection(A)
    test_get_config_from_instance(C)
    test_get_config_from_arg(C)
    test_main_connected()
