import sys
import yaml

def prompt():
    print("Setting up credentials...")
    print("Have you downloaded your client.json file from Google Cloud?")

LAST = False

OPTIONS = [
    'Yes            - (y)',
    'No             - (n)',
]

def format_as_dict(path):
    #Template
    #creds_path: [path]
    return {
        'creds_path': path
    }

def add_creds_path_to_file(formatted_dict):
    with open('src/config/main.yaml', 'a+') as config_file:
        yaml.dump(formatted_dict, config_file, default_flow_style=False)

def response(inpt):
    finished = False
    inpt_accepted = False
    if inpt == 'y':
        input_not_accepted = False
        print('''Awesome! Please enter the full path of creds.json''')
        creds_path = input()
        formatted_dict = format_as_dict(creds_path)
        add_creds_path_to_file(formatted_dict)
        finished = True
        inpt_accepted = True
    elif inpt == 'n':
        print('''Before you proceed, you need to download a credentials file from
Google Cloud. Please see the installation instructions for this
step''')
        finished = False
        inpt_accepted = True
    return finished, inpt_accepted
