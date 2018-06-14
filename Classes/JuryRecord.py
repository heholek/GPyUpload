
"""
Subclass of Record, contains the extra information required to identify individual juries. Also contains raw, individual data instead of aggregate

There should be one of these objects for every single jury that takes place
"""

class JuryRecord(Record):

    def __init__(self, **kwargs):
        super().__init__(timestamp, area, semester, year, evaluation_areas, pass_rates) #Call initialization of Record class
        self.student_name = student_name
        self.record_code = record_code #Unique identifier for each jury appointment, stored as string
        self.primary_instrument = primary_instrument #Student's primary instrument; NOT necessarily the instrument for this jury
        self.jury_purpose = jury_purpose #UDP, Recital Check, Standard Jury, Piano Proficiency, etc.
        self.instructor = instructor #Student's instructor
        self.student_info_timestamp #Timestamp when student completed the student information form
        self.is_primary = is_primary #Boolean, True only if this is the jury for the studen't primary instrument/voice type
        self.repertoire = repertoire #Repertoire object

    def verifyCode(self):
        """
        Verifies that code correctly corresponds to student and area

        Code Format:

        XABCDE-FG-1
        X - First Initial
        ABCDE - First 5 of last name
        FG - Area Code
        1 - 
        """
        first_initial = self.record_code[0]
        last_name = self.record_code[1:6]
        area = self.record_code[7:8]

