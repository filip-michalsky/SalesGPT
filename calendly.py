import os
import requests
from dotenv import load_dotenv
load_dotenv()

def list_available_event_type_uuids():
    '''List available event type UUIDs from the Calendly account'''
    api_key = os.getenv('CALENDLY_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.calendly.com/event_types'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        event_types = data.get('collection', [])
        uuids = [event_type['uri'].split('/')[-1] for event_type in event_types]
        return uuids
    else:
        return f"Failed to retrieve event types: {response.status_code} - {response.text}"

def generate_calendly_invitation_link(query):
    '''Generate a calendly invitation link based on the single query string'''
    event_type_uuid = os.getenv("CALENDLY_EVENT_UUID")
    if not event_type_uuid:
        available_uuids = list_available_event_type_uuids()
        if isinstance(available_uuids, str):
            return available_uuids  # Return error message if failed to retrieve UUIDs
        elif available_uuids:
            event_type_uuid = available_uuids[0]  # Use the first available UUID
        else:
            return "No available event types found in your Calendly account."

    api_key = os.getenv('CALENDLY_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.calendly.com/scheduling_links'
    payload = {
        "max_event_count": 1,
        "owner": f"https://api.calendly.com/event_types/{event_type_uuid}",
        "owner_type": "EventType"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        data = response.json()
        return f"url: {data['resource']['booking_url']}"
    else:
        return f"Failed to create Calendly link: {response.status_code} - {response.text}"
    
print(generate_calendly_invitation_link('test'))

