# GCal API - Python

The files in this repo contain examples of using the Google Calendar API in Python to perform CRUD functionality, which can be used to automate certain tasks in Google Calendar.

The files in this repo contain reference to client_secret_file.json, which is unique to each application author. If you wish to use these files to modify calendar events on your own, you have to create an account with Google Cloud Platform, and generate your own client-secret file.

**gcal.py** contains example code from Google's Calendar API docs, under Python Quickstart.
Source: https://developers.google.com/calendar/api/quickstart/python]

In the Python Quickstart example above, running main() allows us to build a service object which allows us to access its resources. These resources such as "Calendars", "Events" are RESTful and allow us to access data and methods provided by the Calendar API.

**gcal.py** shows us how to read the next 10 events on an authenticated user's primary calendar.

**gcal2.py** contains methods with the following functionality:

1. Create a calendar
2. Delete a calendar
3. Add an event to an existing calendar, and create a Google Meet link for the created event.
4. Update an event (for now, just the summary and description of the event)
5. Delete an event

**boilerplate_create_service.py**

-> generates authentication token for the end-user and stores it in a pickle file.
-> contains boilerplate code for initiating a service object with any Google API.
-> contains a method to convert dates to RFC3339 standard, specifically the UTC+0 timezone.
