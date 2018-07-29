# GPyReport [![Build Status](https://travis-ci.org/aarongrisez/GPyReport.svg?branch=master)](https://travis-ci.org/aarongrisez/GPyReport)
This project is very early in development. I haven't yet created installation
scripts. For the time being, you can use the following procedure to jig up an
installation

## Prerequisites:
This app connects to Google resources through a Google Cloud service account.
Be sure that you have a service account created and that at least the Drive and
Sheets API are activated for that account. You will need the json file for one
of that account's associated keys to connect this app to Google Cloud. 

### Steps to connecting Google Cloud:

0. [Make a Google Cloud Project](https://cloud.google.com/resource-manager/docs/creating-managing-projects), If you use the wizard for step 1, you can automatically create a Cloud Project there.
1. [Add Drive to Project](https://console.developers.google.com/flows/enableapi?apiid=drive.googleapis.com), If you created a project in step 0, find that project and add Drive. If you did not create a project already, do so in this step.
2. [Add Sheets to Project](https://console.developers.google.com/flows/enableapi?apiid=sheets.googleapis.com)
3. From the dashboard of your new Google Cloud Project, navigate to IAM & admin.
4. Navigate to Service Accounts.
5. Create new service account. Name it as you wish, and select "Furnish new private key". The option for .json should be automatically selected. If it isn't, select it.o
6. A .json file should automatically start downloading. This is the file you need to connect GPyReport. Rename it `client.json`

## Current Steps to Installation:
1. In the `/src` directory, create a directory `/config`.
    * Create two .yaml files, one named `main.yaml` and one named `request_prefixes.yaml`.
    * You should put some default values in these files to make test.py run correctly.

```yaml
#main.yaml
creds_path: /absolute/path/to/creds/client.json
scopes:
    drive: https://www.googleapis.com/auth/drive
    sheets: https://www.googleapis.com/auth/spreadsheet
files:
    MainSheet:
        id: sheet_id_here
        type: sheets
    Appointments:
        id: sheet_id_here
        type: sheets

```

```yaml
#request_prefixes.yaml
sheets: https://sheets.googleapis.com

```
2. In the `/src` directory, create a directory `/creds`. Move `client.json` to this new directory
