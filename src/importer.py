import os
import gspread
import requests
from .util import full_path, assign_code, search_records
import yaml
from ast import literal_eval
import weakref
from .models.JuryAppointment import JuryAppointment

class Importer():

    def __init__(self, files_dict, app):
        """
        Main Importing object, contains methods for fetching, importing,
        processing, and exporting data

        Parameters:
            files_dict: dict of files to be recognized by importer. This comes
                        from main.yaml
            app: weakref to main app for accessing higher resources

        Attributes:
            app: weakref to main app for accessing higher resources
            files: dict of files recognized by importer
                Each file has two states: loaded and not loaded. Loaded is when
                a GET request has been made, not loaded is before any request
                has been made
            empty_records: any records deemed "empty" during processing
        """
        self.app = app
        self.files = {}
        self.sheets = {}
        self.empty_records = []
        self.temp = {}
        self.spreadsheet_manager = gspread.Client(None,
                                                  self.app().auth.authsession)
        #This loop builds up the dictionary of recognized files
        for key, value in files_dict.items():
            #Supported file types are 'sheets' for Google Sheets and generic
            #drive file for anything else
            if value['type'] == 'sheets':
                #File is a spreadsheet
                self.files[key] = Spreadsheet(_type=value['type'],
                                              _id=value['id'],
                                              contents=None,
                                              loaded=False,
                                              ingested=False,
                                              app=self.app)
            else:
                #File is anything else
                self.files[key] = File(_type=value['type'],
                                       _id=value['id'],
                                       contents=None,
                                       loaded=False,
                                       ingested=False,
                                       app=self.app)

    def load_files(self, exclusions=[]):
        """
        Makes initial GET requests for all recognized files in main.yaml

        Parameters:
            exclusions: list of files to ignore during loading. Exclusions are
            referenced by key (that is, their name in main.yaml)
        """
        #Loop through all recognized files
        for key, _file in self.files.items():
            #Check if file is loaded and not in exclusions
            if not _file.loaded and key not in exclusions:
                app = self.app() #Loads app from weakref
                #Requests are stored in the main app
                request = app.requests.requests[key]
                #Load file contents
                contents = app.auth.make_get_request(request=request)
                _file.contents = contents
                _file.loaded = True

    def ingest_spreadsheets(self, exclusions=[]):
        """
        Ingests all spreadsheets present in the dict of recognized files
        """
        #Get the file containing all metadata flags
        self.get_flag_file()
        for key, _file in self.files.items():
            #Check if the filetype is sheets, not excluded, and not ingested
            if _file._type == 'sheets' and key not in exclusions and not _file.ingested:
                #Set 'current' attributes
                self.current_filename = key
                self.current_file_id = _file._id
                #Ingest sheet
                self.ingest_single_spreadsheet()
                _file.ingested = True
        #Clean up 'current' attributes
        self.current_filename = None
        self.current_file_id = None

    def ingest_single_spreadsheet(self):
        """
        Sets current spreadsheet and runs ingestion
        """
        #Get current spreadsheet using gspread
        self.current_spreadsheet = self.spreadsheet_manager.open_by_key(
                                        self.current_file_id)
        if self.current_spreadsheet.title == 'AppointmentData':
            self.assigning = True
        else:
            self.assigning = False
        for j in self.current_spreadsheet.worksheets():
            self.current_worksheet = j
            for i in self.flags:
                self.set_current_sheet_flags(i)
                for flag_name, flag_content in self.current_sheet_flags.items():
                    self.set_current_sheet_flags(i)
                    if flag_name == 'model':
                        self.temp[flag_name] = flag_content
                    elif flag_name != 'records':
                        self.temp[flag_name] = self.run_flag(flag_name,
                                                             flag_content)
                    else:
                        self.temp['records'] = self.run_flag_records(flag_content,
                                                        self.current_worksheet.title)
                print('Set flag data for ' + j.title)
                self.sheets[j.title] = self.temp
                self.temp = {}
        #Clean up Attributes for next iteration
        self.current_spreadsheet = None
        self.current_worksheet = None
        self.temp = {}

    def set_current_sheet_flags(self, i):
        """
        Get the appropriate flags for current sheet (passed in as i)

        Parameters:
            i: dict representation of loaded flagfile
        """
        try:
            self.current_sheet_flags = i[self.current_filename]
        except KeyError:
            print('No flags found for ' + self.current_filename)
            self.current_sheet_flags = {}

    def get_flag_file(self):
        """
        Retrieve all flagfiles.
        """
        flag_file_path = full_path('src/config/flagfiles/')
        flags = []
        for i in os.listdir(flag_file_path):
            with open(flag_file_path + i) as f:
                print(f)
                flags.append(yaml.load(f))
        self.flags = flags

    def run_flag_records(self, flag_dict, sheet_title):
        """
        Gets header row for the sheet's records
        """
        cell = self.current_worksheet.find(flag_dict['flag_string'])
        row = cell.row
        records = self.current_worksheet.get_all_records(head=row)
        deletions = []
        k = 1
        for (i, record) in enumerate(records):
            if self.check_record_empty(record):
                deletions.append(i)
            #CAREFUL, THIS NEXT LINE IS HARDCODED AND CAN CAUSE ISSUES
            elif self.assigning==True:
                record['code'] = assign_code(record, k, self.temp['location'],
                                         sheet_title)
                k += 1
        for j in sorted(deletions, reverse=True):
            print('Deleting ' + str(j))
            del records[j]
        return records

    def check_record_empty(self, record):
        """
        Checks all fields in the current record. If more than 50% are blank,
        registers the record as empty

        Parameters:
            record: Dictionary representation of current record to be tested

        Returns:
            boolean: if record is deemed to be empty
        """
        counter = 0.0
        length = len(record.items())
        for key, value in record.items():
            if not value:
                counter += 1.0
        if counter / length >= 0.5:
            self.empty_records.append(record)
            return True
        else:
            return False

    def run_flag(self, flag_name, flag_dict):
        """
        For a given flag, extracts the vector for identifying data and
        retrieves that value
        """
        cell = self.current_worksheet.find(flag_dict['flag_string'])
        vector = (int(flag_dict['flag_data_row']),
                  int(flag_dict['flag_data_column']))
        (row, col) = cell.row, cell.col
        (data_row, data_col) = (row + vector[0], col + vector[1])
        data_cell = self.current_worksheet.cell(data_row, data_col)
        flag_cell = self.current_worksheet.cell(row, col)
        return data_cell.value

####CODE BELOW THIS LINE SHOULD BE REFACTORED
class File(object):
    __slots__ = '_type', '_id', 'contents', 'loaded', 'ingested', 'app'
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

