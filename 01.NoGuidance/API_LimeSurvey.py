import requests
import base64
import json

API_URL = "https://visualizationliteracy.limesurvey.net/admin/remotecontrol"

def get_session_key(username, password):
    payload = {"method": "get_session_key", "params": [username, password], "id": 1}
    response = requests.post(API_URL, json=payload, headers={"content-type": "application/json"})
    return response.json().get("result") if response.status_code == 200 else None

def release_session_key(session_key):
    payload = {"method": "release_session_key", "params": [session_key], "id": 2}
    requests.post(API_URL, json=payload, headers={"content-type": "application/json"})

def fetch_responses(session_key, survey_id):
    payload = {
        "method": "export_responses",
        "params": [
            session_key,
            survey_id,
            "json",
            {}  # Add filters like "language" or "completed" if needed
        ],
        "id": 3
    }
    response = requests.post(API_URL, json=payload, headers={"content-type": "application/json"})
    if response.status_code == 200:
        return decode_base64_response(response.json().get("result"))
    else:
        return None

def decode_base64_response(encoded_response):
    try:
        decoded_bytes = base64.b64decode(encoded_response)
        decoded_string = decoded_bytes.decode('utf-8')
        return json.loads(decoded_string)
    except Exception as e:
        print(f"Error decoding response: {e}")
        return None
