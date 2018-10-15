# GPyReport 
This project is very early in development. I haven't yet created installation
scripts. For the time being, you can use the following procedure to jig up an
installation

- If you don't already have your own client.json file:
	1. Go to console.cloud.google.com
	2. Make sure you're logged in with your Chapman account (or whatever google account is linked to the drive you want to upload to).
	3. You can either create a project or not, I would suggest creating one just to compartmentalize things. You can do this from 'Select a project' in the top left corner.
	4. Navigate to APIs/Services -> Library
	5. Search for and activate the Google Drive API
	6. Navigate to APIs/Services -> Credentials
	7. Create new credentials
		a. Select OAuth client ID
		b. Select 'Other' application type
		c. Follow the wizard
	8. Download the new credentials json file (download button all the way on the right of the screen)
	9. Put this file in the appropriate creds folder in 'src'.

- In main.yaml, ignore everything else except what's under 'directories'. The first directory you see there is the root directory in your google drive. You can name it as you please. Get the id for that file from google drive in your browser.


