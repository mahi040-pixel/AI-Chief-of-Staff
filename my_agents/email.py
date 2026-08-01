from agents import Agent, function_tool
from tools.gmail_tool import send_email


@function_tool
def gmail(
    to: str,
    subject: str,
    body: str
):

    return send_email(
        to,
        subject,
        body
    )


email_agent = Agent(
    name="Email Agent",
    instructions="""
You are an Email Assistant.

Whenever the user asks to send an email,
ALWAYS use the gmail tool.

Never write the email without using the tool.
""",
    tools=[gmail]
)