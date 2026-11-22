from agents import Agent, function_tool
from tools.calendar_tool import (
    prepare_calendar_event,
    get_tomorrows_meetings,
)


@function_tool
def calendar(
    title: str,
    start: str,
    end: str,
):
    """
    Prepare a calendar event for user confirmation.
    Does not create the event directly.
    """
    return prepare_calendar_event(title, start, end)


@function_tool
def view_tomorrows_calendar():
    """
    Retrieve and display tomorrow's scheduled calendar meetings.
    """
    try:
        events = get_tomorrows_meetings()

        if not events:
            return "There are no meetings scheduled for tomorrow."

        meetings = []

        for event in events:
            start_info = event.get("start", {})
            start_time = (
                start_info.get("dateTime")
                or start_info.get("date")
                or "Time unavailable"
            )

            meetings.append(
                f"Meeting: {event.get('summary', 'Untitled')}\n"
                f"Time: {start_time}"
            )

        return "\n\n".join(meetings)

    except Exception as e:
        return f"Unable to retrieve calendar meetings: {str(e)}"


calendar_agent = Agent(
    name="Calendar Agent",

    instructions="""
You are a Calendar Assistant.

For requests to view tomorrow's meetings,
check the calendar using view_tomorrows_calendar.

For requests to create a meeting,
always use the calendar tool.

Extract:
1. Title
2. Start datetime
3. End datetime

Use ISO datetime format.

IMPORTANT:
- The calendar tool only prepares an event.
- Never create an event directly.
- Never claim that an event has been scheduled.
- The application will display the event details
  and request explicit user confirmation.
- The event will only be created after confirmation.
- For calendar read-only requests, use the
  appropriate calendar retrieval tool.
""",

    tools=[
        calendar,
        view_tomorrows_calendar,
    ],
)