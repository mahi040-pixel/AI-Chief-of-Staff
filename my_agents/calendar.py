from agents import Agent, function_tool
from tools.calendar_tool import prepare_calendar_event


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

    return prepare_calendar_event(
        title,
        start,
        end,
    )


calendar_agent = Agent(
    name="Calendar Agent",

    instructions="""
You are a Calendar Assistant.

Whenever the user wants to create a meeting,
ALWAYS use the calendar tool.

Your responsibility is to prepare the event details.

Extract:

1. Title
2. Start datetime
3. End datetime

Use ISO datetime format.

Example:
2026-07-30T17:00:00

IMPORTANT:

- The calendar tool only prepares an event.
- Never create an event directly.
- Never claim that an event has been scheduled.
- The application will display the event details
  and request explicit user confirmation.
- The event will only be created after confirmation.
""",

    tools=[calendar],
)