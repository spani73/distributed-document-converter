from mailjet_rest import Client
import os
import json

api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def notification(message):
    try:
        message = json.loads(message)
        download_fid = message['download_fid']
        sender_address = os.environ.get('EMAIL')
        receiver_address = message['username']
        
        data = {
        'Messages': [
                    {
                            "From": {
                                    "Email": f"{sender_address}",
                                    "Name": "DarkPdf"
                            },
                            "To": [
                                    {
                                            "Email": f"{receiver_address}",
                                            "Name": "User"
                                    }
                            ],
                            "Subject": "Your DarkPdf is ready!!!",
                            "TextPart": f"Your download is ready. Download it using this file_id : {download_fid} from /download url.",
                    }
            ]
        }

        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        return None
        
    except Exception as e:
        print("err", e)
        return e