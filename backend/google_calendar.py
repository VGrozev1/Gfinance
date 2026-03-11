"""Create events in Google Calendar."""
import logging
import os
from datetime import datetime
from typing import List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import GOOGLE_CALENDAR_ID, GOOGLE_SERVICE_ACCOUNT_FILE

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
logger = logging.getLogger(__name__)


def create_event(
    summary: str,
    start_datetime: datetime,
    end_datetime: datetime,
    description: str = "",
    attendee_emails: Optional[List[str]] = None,
) -> Optional[str]:
    """Create a calendar event. Returns event id or None on failure."""
    if not GOOGLE_CALENDAR_ID or not GOOGLE_SERVICE_ACCOUNT_FILE:
        logger.warning("Google Calendar skipped: GOOGLE_CALENDAR_ID or GOOGLE_SERVICE_ACCOUNT_FILE not set")
        return None
    if not os.path.isfile(GOOGLE_SERVICE_ACCOUNT_FILE):
        logger.warning("Google Calendar skipped: credentials file not found: %s", GOOGLE_SERVICE_ACCOUNT_FILE)
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        body = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Europe/Sofia",
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Europe/Sofia",
            },
        }
        if attendee_emails:
            body["attendees"] = [{"email": e} for e in attendee_emails]
        event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=body).execute()
        logger.info("Created Google Calendar event: %s", event.get("id"))
        return event.get("id")
    except Exception as e:
        logger.exception("Google Calendar create_event failed: %s", e)
        return None
