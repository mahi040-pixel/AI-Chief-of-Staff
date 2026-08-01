from agents import Agent, function_tool
from tools.search_tool import search_web


@function_tool
def web_search(query: str) -> str:
    results = search_web(query)

    output = ""

    for item in results:
        output += f"Title: {item['title']}\n"
        output += f"URL: {item['url']}\n"
        output += f"Content: {item['content']}\n\n"

    return output


research_agent = Agent(
    name="Research Agent",
    instructions="""
You are an expert researcher.

Always use the web_search tool.

Summarize the findings.

Return concise bullet points.
""",
    tools=[web_search]
)