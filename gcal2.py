from pprint import pprint
from boilerplate_create_service import Create_Service

CLIENT_SECRET_FILE = 'client_secret_file.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

request_body = {
    'summary': 'Event 1'
}

'''
To create a calendar
'''
response = service.calendars().insert(body=request_body).execute()
print(response)

'''
To delete a calendar 
'''
service.calendars().delete(
    calendarId='c_m78uvh7vhuahujigal3rvpcq20@group.calendar.google.com').execute()

# Harcoded calendar ID -> should be changed

'''
Add event + Google Meet key
'''
event = {
    "start": {"dateTime": "2021-09-24T00:00:00.000+09:00"},
    "end": {"dateTime": "2021-09-24T00:30:00.000+09:00"},
    "attendees": [{"email": "jasoncruz98@gmail.com"}],
    "conferenceData": {"createRequest": {"requestId": "sample123", "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
    "summary": "sample event with Meet link",
    "description": "sample description"
}
res = service.events().insert(calendarId="primary", sendNotifications=True,
                              body=event, conferenceDataVersion=1).execute()
print(res)

eventId = res['id']

'''
Update event
'''

res['summary'] = "sample event with Meet link has been changed"
res['description'] = "sample description has been changed"
service.events().update(calendarId="primary", eventId=eventId, body=res).execute()

'''
Delete an event
'''
service.events().delete(calendarId="primary", eventId=eventId).execute()
