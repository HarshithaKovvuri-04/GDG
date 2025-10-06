from flask import Flask, request, jsonify, render_template
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class ZoomAPIClient:
    def __init__(self):
        self.api_key = os.getenv('ZOOM_API_KEY')
        self.api_secret = os.getenv('ZOOM_API_SECRET')
        self.account_id = os.getenv('ZOOM_ACCOUNT_ID')

    def get_access_token(self):
        token_url = "https://zoom.us/oauth/token"
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
        
        response = requests.post(token_url, headers=headers, data=data)
        return response.json().get('access_token')

    def create_meeting(self, topic):
        access_token = self.get_access_token()
        
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
        
        # Debugging: Print the response from Zoom API
        print("Zoom API Response:", response.json())
        
        return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-meeting', methods=['POST'])
def generate_meeting():
    data = request.json
    topic = data.get('topic', 'Untitled Meeting')
    
    zoom_client = ZoomAPIClient()
    meeting_info = zoom_client.create_meeting(topic)
    
    # Check if the meeting was created successfully
    if 'join_url' in meeting_info:
        return jsonify(meeting_info)
    else:
        # Return an error message if the meeting creation failed
        return jsonify({
            "error": "Failed to create meeting",
            "details": meeting_info
        }), 400

if __name__ == '__main__':
    app.run(debug=True)