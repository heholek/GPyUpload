from os.path import dirname, join

MAIN_DIRECTORY = dirname(dirname(__file__))
def full_path(*path):
    return join(MAIN_DIRECTORY, *path)
