#filemanager.py

class FileManager():

    def __init__(self, app, db_path, classes):
        self.app = app
        self.model_groups = {}
        self.models = {}
        self.classes = classes

