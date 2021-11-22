import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


client_secret_file = 'client_secret_file.json'


class GCal:

    creds = None
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, client_secret_file):
        self.client_secret_file = client_secret_file
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'token.json', self.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build(self.API_NAME, self.API_VERSION,
                             credentials=self.creds)

    def getEventsList(self, maxResults):
        self.maxResults = maxResults
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming {} events'.format(self.maxResults))
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=self.maxResults, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start + " " + event['summary'] +
                  ", Event ID: " + event['id'])

    def createNewEvent(self, start, end, attendees, summary, description, GoogleMeet=False):
        self.start = start
        self.end = end
        self.attendees = attendees
        self.summary = summary
        self.description = description
        self.GoogleMeet = GoogleMeet

        conferenceDataVersion = 1

        if self.GoogleMeet == False:
            conferenceDataVersion = 0

        event = {
            "start": {"dateTime": self.start},
            "end": {"dateTime": self.end},
            "attendees": [self.attendees],
            "conferenceData": {"createRequest": {"requestId": "gcal-api-python", "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
            "summary": self.summary,
            "description": self.description
        }
        res = self.service.events().insert(calendarId="primary", sendUpdates="none",
                                           body=event, conferenceDataVersion=conferenceDataVersion).execute()

    def updateEventById(self, eventId, updatedSummary, updatedDescription):
        self.eventId = eventId
        self.updatedSummary = updatedSummary
        self.updatedDescription = updatedDescription

        event = self.service.events().get(
            calendarId='primary', eventId=self.eventId).execute()

        event['summary'] = self.updatedSummary
        event['description'] = self.updatedDescription

        updated_event = self.service.events().update(
            calendarId='primary', eventId=self.eventId, body=event).execute()

    def deleteEventById(self, eventId):
        self.eventId = eventId

        event = self.service.events().delete(
            calendarId="primary", eventId=self.eventId).execute()


# Testing

g = GCal("client_secret_file.json")

# Retrieving events list
g.getEventsList(20)

# Creating a new event, Google Meet link optional
# test_list = ["2021-11-23T01:00:00.000+08:00", "2021-11-23T02:30:00.000+08:00",
#              {"email": "jasoncruz98@gmail.com"}, "test event", "test description"]
# g.createNewEvent(test_list[0], test_list[1],
#                  test_list[2], test_list[3], test_list[4], GoogleMeet=True)

# Updating an event
# test_event_id = "s6g12bhtiqbgpqe80q8medmgoc"
# g.updateEventById(test_event_id, "updated summary", "updated description")

# Deleting an event
# test_event_id = "s6g12bhtiqbgpqe80q8medmgoc"
# g.deleteEventById(test_event_id)
