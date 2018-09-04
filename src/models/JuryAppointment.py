from ..util import search_records, zeropad_int_pairs
import functools
import datetime
import weakref
from sqlalchemy import Column, Integer, String, DateTime
from .base import MetaBase

"""
Class containing the information for a jury appointment. Fields to be populated with student information when provided
"""

class JuryAppointmentDB(MetaBase):
    __slots__ = []
    __tablename__ = 'JuryAppointments'

    id = Column(Integer, primary_key=True)
    meta = Column(String)
    record_group = Column(String)
    formattedTime = Column(String)
    instrument = Column(String)
    User = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    ApplicantName = Column(String)
    classStanding = Column(String)
    seniorRecital = Column(String)
    seniorRecitalYear = Column(String)
    UDP = Column(String)
    email = Column(String)
    phone = Column(String)
    majorDescription = Column(String)
    emphasis = Column(String)
    code = Column(String)
    datetime = Column(DateTime)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                print(e)
                print('Funkiness trying to set DB object attribute')

class JuryAppointment(object):
    __slots__ = ('meta', 'record_group', 'formattedTime', 'instrument', 'User', 'firstname',
                'lastname', 'ApplicantName', 'classStanding',
                'seniorRecital', 'seniorRecitalYear', 'UDP', 'email', 'phone',
                'majorDescription', 'emphasis', 'code', 'datetime', '__weakref__')

    _instances = set()
    REPORT_TYPE = 'aggregate' #Not individual reporting
    TEMPLATE_NAME = 'appointmentSchedule.tex'
    ormobject = JuryAppointmentDB

    def __init__(self, **kwargs):
        """
        Ingest all data from Rob's export
        """
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                if key == 'Applicant Name':
                    self.ApplicantName = value
        self.datetime = self.parse_date()
        self._instances.add(weakref.ref(self))

    def parse_date(self):
        year = str(datetime.date.today().year)
        date = zeropad_int_pairs(self.meta['date'] + ', ' + year)
        time = zeropad_int_pairs(self.formattedTime)
        date_obj = datetime.datetime.strptime(date, '%A, %B %d, %Y')
        time_obj = datetime.datetime.strptime(time, '%I:%M %p')
        dt = datetime.datetime.combine(date_obj, time_obj.time())
        return dt

    def as_list(self):
        temp = []
        for i in self.__slots__:
            if i != '__weakref__':
                temp.append(str(getattr(self,i)))
        return temp

    @classmethod
    def get_report_group(cls, group):
        """
        Returns list of all Jury Appointments in a given group
        """
        group_list = []
        for inst in cls.get_instances():
            if inst.record_group == group:
                group_list.append(inst)
        return group_list

    @classmethod
    def get_instances(cls):
        """
        Yields all instances of JuryAppointment
        """
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
            cls._instances -= dead

    @classmethod
    def lookup_code(cls, record, target):
        """
        Looks up the information for a given record in the target spreadsheet,
        should be attached to JuryAppointment class
        """
        try:
            target_sheet = self.app().spreadsheet_manager.open(target)
        except:
            print('Could not open ' + target + ' spreadsheet')
        located_record = search_records(target_sheet, record) # Row of most likely record
        row = self.app().spreadsheet_manager.row_values(located_record)
        return row['code']

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        if self.User == other.User and self.datetime == other.datetime:
            raise ValueError('Someone is at two places at once')
        else:
            return self.datetime < other.datetime
