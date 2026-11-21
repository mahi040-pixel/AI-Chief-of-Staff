
import os
import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


# ---------------- GMAIL AUTHENTICATION ---------------- #

def gmail_service():

    creds = None

    if os.path.exists("token.json"):

        try:
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        except (ValueError, OSError):
            print("Invalid token. Starting fresh authentication.")
            creds = None

    if creds and creds.expired and creds.refresh_token:

        try:
            creds.refresh(Request())
            print("Gmail token refreshed successfully.")

        except RefreshError:
            print("Token expired. Reauthentication required.")
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

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


# ---------------- PREPARE EMAIL ---------------- #

def prepare_email(to, subject, body):

    return {
        "status": "pending_confirmation",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "Email draft prepared. Waiting for user confirmation."
    }


# ---------------- SEND CONFIRMED EMAIL ---------------- #

def send_email(to, subject, body):

    service = gmail_service()

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return "Email sent successfully."
