# This single script gathers all the Class tests and prepares them for
# execution. TODO: Get this darned thing into a nosetest suite, stat

import authenticate

def setUp():
    return authenticate.Authenticator()

def testAuthenticator(a):
    """
    Gets passed Authenticator instance and runs the connect() method
    """
    a.connect()

if __name__ == "__main__":
    a = setUp()
    testAuthenticator(a)
