from agents import Agent, function_tool

from tools.strategy_tool import add_goal, list_goals, update_goal_status


@function_tool
def add_strategic_goal(goal: str, owner: str = "CEO", deadline: str = "Not set") -> str:
    return add_goal(goal, owner, deadline)


@function_tool
def list_strategic_goals() -> str:
    goals = list_goals()

    if not goals:
        return "No strategic goals tracked yet."

    output = ""

    for g in goals:
        output += f"- {g['goal']} | Owner: {g['owner']} | Deadline: {g['deadline']} | Status: {g['status']}\n"

    return output


@function_tool
def update_strategic_goal(goal: str, status: str, note: str = "") -> str:
    return update_goal_status(goal, status, note if note else None)


strategy_agent = Agent(
    name="Strategy Tracker Agent",
    instructions="""
You are the Strategy Tracker Agent.

You monitor the CEO's strategic goals / OKRs.

Whenever the user asks to:
- add a strategic goal
- track a goal
- set an objective / OKR

use add_strategic_goal.

Whenever the user asks to:
- show goals
- list strategic goals
- what are our priorities / OKRs

use list_strategic_goals.

Whenever the user asks to:
- update progress on a goal
- mark a goal done / at risk / in progress

use update_strategic_goal.

IMPORTANT: Return the tool's output exactly as it is. Do NOT invent,
reformat, or add fields (such as a "Status" value) that the tool did not
return. If you want to add a short one-line confirmation, add it AFTER
the raw tool output, never instead of it.
""",
    tools=[
        add_strategic_goal,
        list_strategic_goals,
        update_strategic_goal,
    ],
)