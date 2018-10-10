import main
import os
import json
from apiclient.http import MediaFileUpload

UPLOADS_PATH = 'src/uploads/'

if __name__ == "__main__":
    app = main.App()
#    app.setModels([JuryAppointment, StudentResponse])
    app.register_classes()
    parent_folder_id = '1d-lLioPih504aD6Hao9mk4Dg7ahch5EJ'
    request_string = 'https://www.googleapis.com/drive/v3/files?q="' + parent_folder_id + '"+in+parents'
    r = app.auth.authsession.get(request_string)
    response_dict = json.loads(r.text)
    directories = response_dict['files']
    uploads = os.listdir(UPLOADS_PATH)
    for i in uploads:
        for j in directories:
            if j['name'] in i:
                print("Uploading " + i + " to " + j['name'])
    print('Does this look correct? (y for yes, n for no)')
    choice = input()
    if choice.lower() == 'y':
        upload_files = []
        print('Uploading...')
        for i in uploads:
            for j in directories:
                if j['name'] in i:
                    metadata = {
                        'name': i,
                        'parents': [j['id']]
                    }
                    print(metadata)
                    media = MediaFileUpload(UPLOADS_PATH + i, resumable=True)
                    upload_files.append(media)
                    app.auth.drive_service.files().create(body=metadata,
                                                      media_body=media).execute()
    else:
        print('Aborting')
