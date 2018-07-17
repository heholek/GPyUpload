
class Record():
    """
    Base class for all records; defines the interface for interacting with a record
    """

    def __init__(self, **kwargs):
        self.timestamp = timestamp #Time that this record was created. For Individual juries, this should be submission time of the faculty jury form. For aggregate records, this is the time that the record was generated
        self.area = area #Area of conservatory for this jury, for individual student this is primary area
        self.semester = semester #Fall or Spring for this jury; if it's a makeup jury, this is the semester it's making up for, not necessarily the semester when it actually occurred
        self.year = year #Year this jury took place; same as above if makeup
        self.evaluation_areas = evaluation_areas #This object is a dictionary that contains for each evaluation area the student's achieved value for this jury (i.e.: { ..., "Musicality": 3, ...})
        self.pass_rates = pass_rates #This object is a dictionary that contains for each evaluation type (e.g.: Jury, UDP, Recital Check, etc.) one of the following: (a) 1 or 0 if the student passed or failed respectively (b) None if the student did not attempt that evaluation type
