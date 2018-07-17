## Notes to Self:
* Need to figure out how to grant permissions to edit files in team drive
  without link-sharing the file to the public

## Packages to Use:
* jinja
* google-api-python-client

## Modules:
* setup.py - Installs Package and all Requirements
* main.py
	* On application start, runs authentication
	* Contains functions:
		* buildUI(uiOptions)
		* importData(importOptions)
			* Mode 1 - Code Assignment, schedule generation
			* Mode 2 - Record Sorting, report generation
		* buildReports(buildOptions)
		* deliverReports(deliveryOptions)
* UI.py - Lightweight GUI for main
* Authenticate.py - Connects to data source, Contains global constant links to the
		    appropriate spreadsheets that contain data
* ImportData.py - Pulls all current data for analysis
* BuildReports.py - Builds report from one of the templates
* DeliverReports.py - Sends reports to appropriate parties	

## Classes

### Mode 1 Important Classes:
	1. JuryAppointment.py
### Mode 2 Important Classes:
	1. Record.py - Base class for JuryRecord, both aggregate and individual
	2. JuryRecord.py - Subclass of Record, contains the interface for sorting data for a particular jury
## Templates
1.  studentReports.py - Template Class associated with a studentReport
2. learningOutcomeAssessment.py - Template Class associated with a LOAreport
3. areaDirectorReports.py - Template Class associated with a collection of student reports for a given area director
4. HTML/
	* studentReport.html
	* learningOutcomeAssessment.html
## Test
	test_Authentication.py
	test_studentReport.py
	test_learningOutcomeAssessment.py
	test_deliverReports.py
