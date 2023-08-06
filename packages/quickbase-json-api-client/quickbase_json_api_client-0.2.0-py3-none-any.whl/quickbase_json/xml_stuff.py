import base64

import requests


def xml_upload():
    headers = {
        'Content-Type': 'application/xml',
        'QUICKBASE-ACTION': 'API_UploadFile'
    }


    with open('xmlstuff.xml') as xml:
        new_file_b64 = open('287.jpeg', 'rb')
        xml = xml.read().replace('{{base64}}', base64.b64encode(new_file_b64.read()).decode())
        print(xml)

        r = requests.post(url='https://synctivate.quickbase.com/db/bqs5cbduv', headers=headers, data=xml)

    print(r)
    print(r.text)

