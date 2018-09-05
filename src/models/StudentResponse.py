"""
Model for the student response information, to be joined with JuryAppointment
"""

from ..util import search_records
import datetime
import weakref
from sqlalchemy import Column, Integer, String, Text, DateTime
from .base import MetaBase

class StudentResponseDB(MetaBase):
    __slots__ = []
    __tablename__ = 'StudentResponse'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    email = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    student_id = Column(String)
    primary_area = Column(String)
    primary_inst_voice = Column(String)
    program = Column(String)
    purpose = Column(String)
    instructor = Column(String)
    repertoire = Column(Text)
    makeup = Column(String)
    semester = Column(String)
    year = Column(String)
    is_primary = Column(String)
    date = Column(String)
    time = Column(String)
    datetime = Column(DateTime)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                print(e)
                print('Funkiness trying to set DB object attribute')

class StudentResponse(object):
    __slots__ = ('timestamp', 'email', 'firstname', 'lastname', 'student_id',
                 'primary_area', 'primary_inst_voice', 'program', 'purpose',
                 'instructor', 'repertoire', 'makeup', 'semester', 'year',
                 'is_primary', 'date', 'time', 'datetime', '__weakref__')

    _instances = set()
    REPORT_TYPE = 'individual' #Individual reporting
    TEMPLATE_NAMES = ['appointmentSchedule.tex', 'juryReport.tex']
    ormobject = StudentResponseDB

    def __init__(self, **kwargs):
        """
        Ingest all data from Google Spreadsheet of responses
        """
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError as e:
                print(e)
        self.parse_date()
        self._instances.add(weakref.ref(self))

    def as_list(self):
        temp = []
        for i in self.__slots__:
            if i != '__weakref__':
                temp.append(str(getattr(self,i)))
        return temp

    def parse_date(self):
        month = int(self.date[0:2])
        day = int(self.date[3:5])
        year = int(self.date[6:10])
        hour = int(self.time[0:2])
        minute = int(self.time[3:5])
        ampm = self.time[9:]
        if ampm == 'PM':
            hour += 12
        self.datetime = datetime.datetime(year, month, day, hour, minute)

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
