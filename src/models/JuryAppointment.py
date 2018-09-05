from ..util import search_records, zeropad_int_pairs
import functools
import datetime
import weakref
from sqlalchemy import Column, Integer, String, DateTime, Text
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
    response = Column(Text)

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
                'majorDescription', 'emphasis', 'code', 'datetime', 'response', '__weakref__')

    _instances = set()
    _dead = set()
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
        self.response = None

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
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                cls._dead.add(ref)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        if self.User == other.User and self.datetime == other.datetime:
            raise ValueError('Someone is at two places at once')
        else:
            return self.datetime < other.datetime
