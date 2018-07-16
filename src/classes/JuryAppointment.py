
"""
Class containing the information for a jury appointment. Fields to be populated with student information when provided
"""

class JuryAppointment():

    def __init__(self, **kwargs):
        """
        Ingest all data from Rob's export 
        """
        self.date = date
        self.time = time
        self.room = room
        self.instrument = instrument
        self.first_name = first_name #Student first name
        self.last_name = last_name
        self.class_standing = class_standing
        self.senior_recital_semester = senior_recital_semester
        self.senior_recital_year = senior_recital_year
        self.is_udp = is_udp
        self.student_email = student_email
        self.student_phone = student_phone
        self.student_major = student_major
        self.student_emphasis = student_emphasis
