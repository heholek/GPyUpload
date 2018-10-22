# GPyReport 

This is an in-progress script to automate uploading documents to Google Drive. Currently it does 2 things:
1. Uploads all files contained in the `uploads` directory to the authenticated Google account's connected Google Drive.
2. Sorts the files into PRE-EXISTING subdirectories where the subdirectory name is a substring of the filename
	(e.g.: A file named `awesome_file.txt` would be sorted into the directory named `awesome` IF `awesome` was a pre-existing subdirectory in the user's Google drive.)

## Getting Started

### Prerequisites
You will need an OAuth ID ("other"-type app) from your Google Cloud dashboard. See [this page](https://cloud.google.com/docs/authentication/end-user) for more details. Specifically, you need the `client-secret.json` file described in "Creating your client credentials" step 6. That file will go in the `creds` directory and get pointed to during installation.

### Installation
Run the installation script with

```
bash install.sh
```

and follow the prompts on the screen. If you encounter any errors you can't resolve, please open an issue!

## Files
`README.md` - this file  
`LICENSE` - the MIT license for this project  
`install.sh` - BASH installation script, run during setup
`main.py` - core app initialization
`planningNotes.md` - a scratchpad for future/in progress features
`requirements.txt` - pip requirements
`run.py` - upload script
`test.py` - the beginnings of a test framework
`src` - source files
* `authenticate.py` - class for Google authentication, generates authorized REST requests
* `configuration.py` - configuration class for application
* `importer.py` - file importer class
* `requests.py` - class that contains REST requests for the application
* `util.py` - generic utility functions
* `config` - contains configuration files
	* `main.yaml` - main configuration file 
* `creds` - contains credential files
	* `client.json` - main credentials file
* `uploads` - container for items to be uploaded to Google drive

## Testing - TODO, URGENT

I will be implementing a nosetests suite as my next task on this project.

# Contributing

Still working on setting up Contribution guidelines, but feel free to open issues in the meantime!

## Maintainers

The current maintainers of this repository are:

* **Aaron Grisez** - [Aaron Grisez](https://github.com/aarongrisez)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
