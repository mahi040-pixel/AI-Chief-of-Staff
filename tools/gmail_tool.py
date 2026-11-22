import os
import json
import base64

import streamlit as st

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

    # 1. Use local token if available
    if os.path.exists("token.json"):

        try:
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        except (ValueError, OSError):
            creds = None

    # 2. Load token from Streamlit Cloud Secrets
    elif "GOOGLE_TOKEN_B64" in st.secrets:

        token_data = base64.b64decode(
            st.secrets["GOOGLE_TOKEN_B64"]
        ).decode("utf-8")

        token_info = json.loads(token_data)

        creds = Credentials.from_authorized_user_info(
            token_info,
            SCOPES
        )

    # 3. Refresh expired credentials
    if creds and creds.expired and creds.refresh_token:

        try:
            creds.refresh(Request())

        except RefreshError:
            creds = None

    # 4. Local OAuth fallback
    if not creds or not creds.valid:

        if not os.path.exists("credentials.json"):
            raise RuntimeError(
                "Google authentication failed. "
                "Please check GOOGLE_TOKEN_B64 in Streamlit Secrets."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

    # 5. Save refreshed token locally
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