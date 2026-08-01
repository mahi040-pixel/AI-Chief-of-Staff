import streamlit as st
import asyncio

from dotenv import load_dotenv
from agents import Runner

from my_agents.planner import planner_agent
from memory.memory import save_memory, load_memory
from tools.meeting_tool import prepare_meeting
from tools.report_tool import generate_executive_report
from tools.strategy_tool import add_goal, list_goals, update_goal_status

load_dotenv()

st.set_page_config(
    page_title="AI Chief of Staff",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 AI Chief of Staff")

    st.markdown("---")

    st.subheader("Example Commands")

    st.code("Research latest OpenAI news")
    st.code("Send an email to abc@gmail.com")
    st.code("Schedule a meeting tomorrow at 5 PM")
    st.code("Prepare meeting brief on Q3 budget")
    st.code("Create a task called Finish Project")
    st.code("Show all my tasks")
    st.code("Add strategic goal: Expand to EU market")
    st.code("Show our strategic goals")
    st.code("Generate executive summary report")

    st.markdown("---")

    st.subheader("🧠 Recent Memory")

    history = load_memory()

    if history:

        for item in history[-5:]:

            st.write("👤", item["user"])

    else:

        st.write("No memory yet.")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ---------------- CHAT HISTORY ---------------- #

if "messages" not in st.session_state:

    st.session_state.messages = []

if "pending" not in st.session_state:

    st.session_state.pending = None

st.title("🤖 AI Chief of Staff")

st.caption("Your AI Executive Assistant")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- ROUTING (failsafe, mirrors main.py) ---------------- #

def route(user_input: str):
    """
    Deterministic keyword routing for actions that must not depend on the
    LLM choosing to hand off correctly. Falls back to the Planner Agent
    (which can still hand off to any agent, including ones not listed
    here) for everything else.
    """

    lower = user_input.lower()

    meeting_keywords = [
        "meeting brief", "prepare meeting", "prepare a meeting",
        "executive brief", "agenda", "discussion points", "briefing",
    ]

    report_keywords = [
        "executive summary", "daily report", "weekly report",
        "status report", "summarize everything",
    ]

    add_goal_keywords = ["add strategic goal", "track goal", "set objective", "set an okr"]

    list_goal_keywords = [
        "show our strategic goals", "show strategic goals",
        "list strategic goals", "our strategic goals", "our priorities",
    ]

    if any(k in lower for k in meeting_keywords):
        return "meeting"

    if any(k in lower for k in report_keywords):
        return "report"

    if any(k in lower for k in add_goal_keywords):
        return "add_goal"

    if any(k in lower for k in list_goal_keywords):
        return "list_goals"

    return "planner"


def extract_goal_text(user_input: str) -> str:
    """Pulls the goal text out of a phrase like 'Add strategic goal: X'."""

    if ":" in user_input:
        return user_input.split(":", 1)[1].strip()

    for keyword in ["add strategic goal", "track goal", "set objective", "set an okr"]:
        idx = user_input.lower().find(keyword)
        if idx != -1:
            return user_input[idx + len(keyword):].strip(" :-")

    return user_input.strip()


def format_goals(goals) -> str:

    if not goals:
        return "No strategic goals tracked yet."

    output = ""

    for g in goals:
        output += f"- {g['goal']} | Owner: {g['owner']} | Deadline: {g['deadline']} | Status: {g['status']}\n"

    return output


CRITICAL_ACTION_HINTS = [
    "send email", "schedule meeting", "create meeting",
    "add meeting", "delete", "update goal",
]


def is_critical_action(user_input: str) -> bool:
    lower = user_input.lower()
    return any(k in lower for k in CRITICAL_ACTION_HINTS)


# ---------------- USER INPUT ---------------- #

prompt = st.chat_input("Type your request...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    status = st.empty()

    route_type = route(prompt)

    async def execute():

        result = await Runner.run(
            planner_agent,
            prompt
        )

        return result.final_output

    if route_type == "meeting":

        status.info("📋 Meeting Preparation Agent")

        with st.spinner("Pulling calendar, research, tasks and memory..."):
            output = prepare_meeting(prompt)

    elif route_type == "report":

        status.info("📊 Report Generator Agent")

        with st.spinner("Compiling executive summary..."):
            output = generate_executive_report()

    elif route_type == "add_goal":

        status.info("🎯 Strategy Tracker Agent")

        with st.spinner("Saving strategic goal..."):
            goal_text = extract_goal_text(prompt)
            output = add_goal(goal_text)

    elif route_type == "list_goals":

        status.info("🎯 Strategy Tracker Agent")

        with st.spinner("Loading strategic goals..."):
            output = format_goals(list_goals())

    else:

        status.info("🧠 Planner Agent")

        with st.spinner("Working..."):
            output = asyncio.run(execute())

    status.success("✅ Completed")

    st.session_state.pending = {
        "user": prompt,
        "assistant": output,
        "critical": is_critical_action(prompt),
    }

    with st.chat_message("assistant"):

        st.markdown(output)

# ---------------- HUMAN APPROVAL ---------------- #
# Every response — critical actions especially (email / calendar / goal
# updates) — waits for explicit human approval before being committed to
# memory, matching the "human approval for critical actions" requirement.

if st.session_state.pending:

    pending = st.session_state.pending

    st.markdown("---")

    if pending["critical"]:
        st.warning("⚠️ This looks like a critical action (email, calendar, or goal update). Please review before approving.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve"):

            save_memory(pending["user"], pending["assistant"])

            st.session_state.messages.append(
                {"role": "assistant", "content": pending["assistant"]}
            )

            st.session_state.pending = None
            st.success("Approved and saved.")
            st.rerun()

    with col2:
        if st.button("❌ Reject"):

            st.session_state.pending = None
            st.info("Rejected — not saved to memory.")
            st.rerun()

# ---------------- DOWNLOAD CHAT ---------------- #

if st.session_state.messages:

    conversation = ""

    for msg in st.session_state.messages:

        conversation += (
            f"{msg['role']}:\n"
            f"{msg['content']}\n\n"
        )

    st.download_button(
        label="📥 Download Conversation",
        data=conversation,
        file_name="conversation.txt",
        mime="text/plain"
    )