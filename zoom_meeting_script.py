import os
import jwt
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ZoomAPIClient:
    def __init__(self):
        # Credentials from Zoom Developer Portal
        self.api_key = os.getenv('ZOOM_API_KEY')
        self.api_secret = os.getenv('ZOOM_API_SECRET')
        self.account_id = os.getenv('ZOOM_ACCOUNT_ID')

        # Validate credentials
        if not all([self.api_key, self.api_secret, self.account_id]):
            raise ValueError("Missing Zoom API credentials. Check your .env file.")

    def get_access_token(self):
        """Obtain OAuth access token"""
        token_url = "https://zoom.us/oauth/token"
        
        # Base64 encode credentials
        import base64
        credentials = f"{self.api_key}:{self.api_secret}"
        base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        headers = {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()  # Raise exception for bad responses
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            print(f"Response content: {response.text}")
            return None

    def create_meeting(self, topic="Test Meeting", start_time=None):
        """Create a Zoom meeting"""
        access_token = self.get_access_token()
        
        if not access_token:
            print("Failed to obtain access token")
            return None

        meeting_endpoint = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        meeting_details = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time or time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration": 60,  # Meeting duration in minutes
            "settings": {
                "host_video": True,
                "participant_video": False,
                "join_before_host": True,
                "mute_upon_entry": True,
                "waiting_room": False
            }
        }
        
        try:
            response = requests.post(meeting_endpoint, json=meeting_details, headers=headers)
            response.raise_for_status()
            meeting_data = response.json()
            
            print("Meeting Successfully Created!")
            print(f"Meeting Link: {meeting_data.get('join_url')}")
            print(f"Meeting ID: {meeting_data.get('id')}")
            
            return meeting_data
        except requests.exceptions.RequestException as e:
            print(f"Error creating meeting: {e}")
            print(f"Response content: {response.text}")
            return None

# Main execution
if __name__ == "__main__":
    try:
        zoom_client = ZoomAPIClient()
        zoom_client.create_meeting()
    except Exception as e:
        print(f"An error occurred: {e}")