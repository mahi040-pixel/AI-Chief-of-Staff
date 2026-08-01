from agents import Agent, function_tool
from tools.meeting_tool import prepare_meeting


@function_tool
def meeting_brief(topic: str) -> str:
    return prepare_meeting(topic)


meeting_agent = Agent(
    name="Meeting Preparation Agent",
    instructions="""
You are ONLY responsible for meeting preparation.

IMPORTANT:
For EVERY meeting-related request, you MUST call the meeting_brief tool.

Do NOT generate your own response.

Pass the meeting topic to the tool.

Return the tool output exactly as it is.
""",
    tools=[meeting_brief],
)