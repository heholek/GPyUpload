import requests

class Importer():

    def __init__(self, files_dict, app):
        self.app = app
        self.files = {}
        for key, value in files_dict.items():
            if value['type'] == 'sheets':
                self.files[key] = Spreadsheet(_type=value['type'],
                                              _id=value['id'],
                                              contents=None,
                                              loaded=False,
                                              app=self.app)
            else:
                self.files[key] = File(_type=value['type'],
                                       _id=value['id'],
                                       contents=None,
                                       loaded=False,
                                       app=self.app)

    def load_files(self, exclusions=None):
        for key, _file in self.files.items():
            if not _file.loaded:
                contents = self.app().auth.make_get_request(request=self.app().requests.requests[key])
                _file.contents = contents
                _file.loaded = True

    def load_spreadsheets(self):
        for key, _file in self.files.items():
            if _file._type == 'sheets':
                sheets = _file.contents.json()['sheets']
                _file.set_sheet_names([i['properties']['title'] for i in sheets])

    def load_spreadsheet_values(self):
        for key, _file in self.files.items():
            if _file._type == 'sheets':
                for name in _file.sheet_names:
                    request = _file.get_values(name=name)
                    _file.values[name] = self.app().auth.make_get_request(request=request)

class File(object):
    __slots__ = '_type', '_id', 'contents', 'loaded', 'app'
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Spreadsheet(File):
    __slots__ = 'sheet_names', 'values'
    def __init__(self, **kwargs):
        super(Spreadsheet, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.values = {}

    def set_sheet_names(self, names):
        self.sheet_names = names

    def get_values(self, name=None, _range=None):
        if _range == None:
            #Return the entire sheet
            request=self.app().requests.base(_type='sheets',
                                  _id = self._id,
                                  suffix='/values/' + name)
        elif name == None:
            request=self.app().requests.base(_type='sheets',
                                  _id = self._id,
                                  suffix='/values/' + _range)
        else:
            raise ValueError('Need a range for the sheets request!')
        return request

    def parse_sheet(self, field):
        """
        Parses an individual sheet in spreadsheet object until the requested
        field is found. CASE SENSITIVE
        """

