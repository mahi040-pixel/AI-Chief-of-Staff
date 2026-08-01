from datetime import datetime

from tools.task_tool import show_tasks
from tools.strategy_tool import list_goals
from memory.memory import load_memory


def generate_executive_report():

    tasks = show_tasks()
    goals = list_goals()
    memory = load_memory()

    report = "# Executive Summary Report\n\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    report += "## Strategic Goals\n"

    if goals:
        for g in goals:
            report += f"- {g['goal']} — {g['status']} (Owner: {g['owner']}, Deadline: {g['deadline']})\n"
    else:
        report += "No strategic goals tracked.\n"

    report += "\n## Pending Tasks\n"

    if tasks:
        for t in tasks:
            report += f"- {t}\n"
    else:
        report += "No pending tasks.\n"

    report += "\n## Recent Activity\n"

    if memory:
        for item in memory[-5:]:
            report += f"- Request: {item['user']}\n"
    else:
        report += "No recent activity logged.\n"

    report += "\n## Key Takeaways\n"
    report += "- Review at-risk goals first.\n"
    report += "- Confirm owners for all open tasks.\n"
    report += "- Escalate anything blocked more than 48 hours.\n"

    return report