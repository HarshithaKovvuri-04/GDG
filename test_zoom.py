import os
import jwt
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_access_token():
    api_key = os.getenv('ZOOM_API_KEY')
    api_secret = os.getenv('ZOOM_API_SECRET')
    account_id = os.getenv('ZOOM_ACCOUNT_ID')

    token_url = "https://zoom.us/oauth/token"
    import base64
    credentials = f"{api_key}:{api_secret}"
    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    return response.json().get('access_token')

def create_meeting(topic):
    access_token = get_access_token()
    
    meeting_endpoint = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    meeting_details = {
        "topic": topic,
        "type": 2,
        "start_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration": 60,
        "settings": {
            "host_video": True,
            "participant_video": False,
            "join_before_host": True
        }
    }
    
    response = requests.post(meeting_endpoint, json=meeting_details, headers=headers)
    print("Meeting Creation Response:", response.json())

if __name__ == "__main__":
    create_meeting("Test Meeting")