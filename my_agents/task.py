from agents import Agent, function_tool
from tools.task_tool import add_task, show_tasks


@function_tool
def create_task(task: str):

    return add_task(task)


@function_tool
def list_tasks():

    return show_tasks()


task_agent = Agent(
    name="Task Agent",

    instructions="""
You are the Task Management Agent.

Whenever the user asks to:
- create tasks
- add a task
- make a checklist
- create a to-do list

use create_task.

Whenever the user asks to:
- show tasks
- list tasks
- display tasks

use list_tasks.

Return the final answer in a clean checklist format.
""",

    tools=[
        create_task,
        list_tasks
    ]
)