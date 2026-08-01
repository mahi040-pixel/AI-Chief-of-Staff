from agents import Agent, function_tool
from tools.calendar_tool import create_event


@function_tool
def calendar(
    title: str,
    start: str,
    end: str,
):

    return create_event(
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

Extract:

Title

Start datetime

End datetime

Use ISO format.

Example:

2026-07-30T17:00:00
""",
    tools=[calendar],
)