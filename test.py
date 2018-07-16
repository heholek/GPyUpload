"""
This single script gathers all the Class tests and prepares them for
execution. TODO: Get this darned thing into a nosetest suite, stat
"""

import google.auth
import src.authenticate
import src.config
import src.utils.files as files

AuthsessionClass = google.auth.transport.requests.AuthorizedSession

def set_up():
    """
    Create resources for testing
    """
    creds_path = files.full_path('creds/client.json')
    auth = src.authenticate.Authenticator(alternate_creds_path=creds_path)
    return auth

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

def test_load_config():
    config_path = files.full_path('utils/config.yaml')
    config_settings = src.config.load_config(config_path)
    assert isinstance(config_settings, dict)

if __name__ == "__main__":
    A = set_up()
    test_authenticator_type(A)
    test_authenticator_connection(A)
    test_load_config()
