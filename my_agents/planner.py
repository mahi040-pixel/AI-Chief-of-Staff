from agents import Agent

from .research import research_agent
from .email import email_agent
from .calendar import calendar_agent
from .task import task_agent
from .review import review_agent
from .meeting import meeting_agent
from .strategy import strategy_agent
from .report import report_agent

planner_agent = Agent(
    name="Planner Agent",
    instructions="""
You are the AI Chief of Staff.

IMPORTANT ROUTING RULES:

If the user says:
- prepare meeting brief
- meeting brief
- executive brief
- agenda
- discussion points
- prepare me for a meeting
- briefing
- summarize tomorrow's meeting

ALWAYS handoff to Meeting Preparation Agent.

If the user says:
- schedule meeting
- create meeting
- add meeting
- calendar
- event

ALWAYS handoff to Calendar Agent.

If the user says:
- send email
- draft email

→ Email Agent

If the user says:
- research
- latest news
- search

→ Research Agent

If the user says:
- task
- todo
- checklist

→ Task Agent

If the user says:
- review
- summarize text
- improve writing

→ Review Agent

Never choose Calendar Agent for "meeting brief".
""",
    handoffs=[
        meeting_agent,
        calendar_agent,
        research_agent,
        email_agent,
        task_agent,
        review_agent,
        strategy_agent,
        report_agent,
    ],
)