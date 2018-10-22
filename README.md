# GPyReport 

### NOTE
GitHub migration seems to have disrupted a pull request to merge "borecki" with master. Please visit that branch for the most current code.

This project is very early in development. I haven't yet created installation
scripts. For the time being, you can use the following procedure to jig up an
installation

- In a new virtualenv, run 
```
pip install -r requirements.txt
```

- If you don't already have your own client.json file:
	1. Go to console.cloud.google.com
	2. Make sure you're logged in with your account (or whatever Google account is linked to the drive you want to upload to).
	3. You can either create a project or not, I would suggest creating one just to compartmentalize things. You can do this from 'Select a project' in the top left corner.
	4. Navigate to APIs/Services -> Library
	5. Search for and activate the Google Drive API
	6. Navigate to APIs/Services -> Credentials
	7. Create new credentials
		a. Select OAuth client ID
		b. Select 'Other' application type
		c. Follow the wizard
	8. Download the new credentials json file (download button all the way on the right of the screen)
	9. Put this file in the appropriate creds folder in `src` and rename it `client.json`.

- In `main.yaml`, ignore everything else except what's under `directories`. The first directory you see there is the root directory in your google drive. You can name it as you please. Get the id for that file from google drive in your browser. Copy this id to `main.yaml`.
- Make sure that the `CREDS_PATH` item in `main.yaml` points to the new credentials file.

- Now, you can run the script. The current `run.py` script (with appropriate commented out blocks) will automatically upload any items in `src/uploads` to the corresponding directory in your Google Drive if (1) the filename contains as a substring the name of the corresponding directory and (2) that directory is a child of the root folder you defined in `main.yaml`.
