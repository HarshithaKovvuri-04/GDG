const API_KEY = 'YOUR_ZOOM_API_KEY';
const API_SECRET = 'YOUR_ZOOM_API_SECRET';

// Function to generate JWT token for Zoom API
function generateToken() {
    const payload = {
        iss: API_KEY,
        exp: ((new Date()).getTime() + 5000)
    };
    return jwt.sign(payload, API_SECRET);
}

// Function to create a Zoom meeting
async function createZoomMeeting() {
    const token = generateToken();
    const meetingDetails = {
        topic: 'Consultation',
        type: 1,
        duration: 30,
        timezone: 'UTC',
        agenda: 'Doctor Consultation',
    };

    try {
        const response = await axios.post('https://api.zoom.us/v2/users/me/meetings', meetingDetails, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        return response.data.join_url; // Return the join URL for the meeting
    } catch (error) {
        console.error('Error creating Zoom meeting:', error);
        return null;
    }
}

// Function to create a Google Meet link
async function createGoogleMeet() {
    const oauth2Client = new google.auth.OAuth2(
        'YOUR_CLIENT_ID',
        'YOUR_CLIENT_SECRET',
        'YOUR_REDIRECT_URL'
    );

    oauth2Client.setCredentials({ refresh_token: 'YOUR_REFRESH_TOKEN' });

    const calendar = google.calendar({ version: 'v3', auth: oauth2Client });

    const event = {
        summary: 'Doctor Consultation',
        start: {
            dateTime: new Date().toISOString(), // Set to current time for testing
            timeZone: 'UTC',
        },
        end: {
            dateTime: new Date(new Date().getTime() + 30 * 60000).toISOString(), // 30 minutes later
            timeZone: 'UTC',
        },
        conferenceData: {
            createRequest: {
                requestId: 'some-random-string',
                conferenceSolutionKey: {
                    type: 'hangoutsMeet',
                },
            },
        },
    };

    try {
        const response = await calendar.events.insert({
            calendarId: 'primary',
            resource: event,
            conferenceDataVersion: 1,
        });
        return response.data.hangoutLink; // Return the Google Meet link
    } catch (error) {
        console.error('Error creating Google Meet:', error);
        return null;
    }
}

// Event listener for the button click
document.getElementById('createMeetingBtn').addEventListener('click', async () => {
    const meetingType = document.getElementById('meetingType').value;
    let meetingLink = '';

    if (meetingType === 'zoom') {
        meetingLink = await createZoomMeeting(); // Call your Zoom function here
    } else if (meetingType === 'googleMeet') {
        meetingLink = await createGoogleMeet(); // Call your Google Meet function here
    }

    if (meetingLink) {
        document.getElementById('meetingLink').href = meetingLink;
        document.getElementById('meetingLink').innerText = meetingLink;
        document.getElementById('meetingLinkContainer').classList.remove('hidden');
    }
});