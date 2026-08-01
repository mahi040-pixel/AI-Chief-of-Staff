from tools.calendar_tool import get_tomorrows_meetings
from tools.search_tool import search_web
from tools.task_tool import show_tasks
from memory.memory import load_memory


def prepare_meeting(topic):

    meetings = get_tomorrows_meetings()
    research = search_web(topic)
    tasks = show_tasks()
    memory = load_memory()

    brief = "# Executive Meeting Brief\n\n"

    brief += f"## Topic\n{topic}\n\n"

    brief += "## Tomorrow's Meetings\n"

    if meetings:
        for meeting in meetings:

            title = meeting.get("summary", "No Title")

            start = meeting["start"].get(
                "dateTime",
                meeting["start"].get("date", "")
            )

            brief += f"- {title}\n"
            brief += f"  Start: {start}\n\n"

    else:
        brief += "No meetings scheduled.\n\n"

    brief += "## Latest Research\n"

    if research:

        for item in research[:3]:

            brief += f"- {item['title']}\n"
            brief += f"{item['content']}\n\n"

    else:

        brief += "No research found.\n\n"

    brief += "## Pending Tasks\n"

    if tasks:

        for task in tasks:

            brief += f"- {task}\n"

    else:

        brief += "No pending tasks.\n"

    brief += "\n## Previous Context\n"

    if memory:

        topic_words = [w.lower() for w in topic.split() if len(w) > 3]

        relevant = [
            item for item in memory[-10:]
            if any(word in item["user"].lower() for word in topic_words)
        ]

        if not relevant:
            relevant = memory[-2:]

        for item in relevant[-2:]:

            short_answer = item["assistant"][:300].replace("\n", " ").strip()

            brief += f"- You asked: \"{item['user']}\"\n"
            brief += f"  Summary: {short_answer}...\n\n"

    else:

        brief += "No previous memory.\n\n"

    brief += """## Recommended Agenda

1. Opening
2. Current Status
3. Discussion
4. Risks
5. Action Items

## Suggested Questions

- What are today's priorities?
- What decisions need approval?
- What are the blockers?

## Expected Outcome

Clear decisions, owners assigned, and follow-up actions documented.
"""

    return brief