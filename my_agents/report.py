from agents import Agent, function_tool

from tools.report_tool import generate_executive_report


@function_tool
def executive_report() -> str:
    return generate_executive_report()


report_agent = Agent(
    name="Report Generator Agent",
    instructions="""
You are ONLY responsible for generating executive summary reports.

For EVERY request about:
- executive summary
- daily report / weekly report
- summarize everything
- status report

you MUST call the executive_report tool.

Do NOT generate your own summary from scratch.

Return the tool output exactly as it is.
""",
    tools=[executive_report],
)