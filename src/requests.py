import yaml

class Requests():

    def __init__(self, path, app):
        self.app = app
        try:
            stream = open(path)
        except:
            print('Something went wrong when loading request prefixes')
        self.prefixes = yaml.load(stream)
        self.requests = {}

    def base(self, _type, _id, suffix=None):
        if suffix == None:
            return self.prefixes[_type] + _id
        else:
            return self.prefixes[_type] + _id + suffix

    def build_base_requests(self, files_dict):
        """
        Establishes connections to Google services for all files included in
        the config.yaml file
        """
        for key, value in files_dict.items():
            self.requests[key] = self.base(_type=value['type'], _id=value['id'])
