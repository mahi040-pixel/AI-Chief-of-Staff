import os

from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
]


# ---------------- CALENDAR AUTHENTICATION ---------------- #

def calendar_service():

    creds = None

    if os.path.exists("token.json"):

        try:
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        except (ValueError, OSError):
            creds = None

    if creds and creds.expired and creds.refresh_token:

        try:
            creds.refresh(Request())

        except RefreshError:
            creds = None

    if not creds or not creds.valid:

        if not os.path.exists("credentials.json"):
            raise FileNotFoundError("credentials.json not found.")

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


# ---------------- PREPARE CALENDAR EVENT ---------------- #

def prepare_calendar_event(summary, start, end):

    return {
        "status": "pending_confirmation",
        "title": summary,
        "start": start,
        "end": end,
        "message": "Calendar event prepared. Waiting for confirmation."
    }


# ---------------- CREATE CONFIRMED EVENT ---------------- #

def create_event(summary, start, end):

    service = calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end,
            "timeZone": "Asia/Kolkata"
        }
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return "Meeting created successfully."


# ---------------- GET TOMORROW'S MEETINGS ---------------- #

def get_tomorrows_meetings():

    service = calendar_service()

    tomorrow = datetime.now() + timedelta(days=1)

    start = datetime(
        tomorrow.year,
        tomorrow.month,
        tomorrow.day,
        0,
        0,
        0
    ).isoformat() + "Z"

    end = datetime(
        tomorrow.year,
        tomorrow.month,
        tomorrow.day,
        23,
        59,
        59
    ).isoformat() + "Z"

    events = service.events().list(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events.get("items", [])