from agents import Agent

review_agent = Agent(
    name="Review Agent",
    instructions="""
Review the response.

Check:

Grammar

Formatting

Completeness

Return polished output.
"""
)