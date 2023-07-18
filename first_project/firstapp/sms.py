import requests
import os
from dotenv import load_dotenv 

load_dotenv()

print(os.getenv('sms_key'))

def send_text(phone,msg):
    headers = {
        'h_api_key': os.getenv('sms_key'),
        'Content-Type': 'application/json',
    }

    json_data = {
        'mobile': phone,
        'response_type': 'json',
        'sender_name': '23107',
        'service_id': 0,
        'message': msg,
    }

    response = requests.post('https://api.mobitechtechnologies.com/sms/sendsms', headers=headers, json=json_data)
    return response.json()