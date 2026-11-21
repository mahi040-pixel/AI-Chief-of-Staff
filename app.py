import streamlit as st
import asyncio
import json
import memory.memory as memory_store
import importlib
importlib.reload(memory_store)


from styles import apply_styles
from dotenv import load_dotenv
from agents import Runner

from my_agents.planner import planner_agent
from my_agents.email import email_agent
from my_agents.calendar import calendar_agent

from tools.meeting_tool import prepare_meeting
from tools.report_tool import generate_executive_report
from tools.strategy_tool import add_goal, list_goals

from tools.gmail_tool import send_email
from tools.calendar_tool import create_event

st.set_page_config(
    page_title="AI Chief of Staff",
    page_icon="🤖",
    layout="wide"
)
load_dotenv()
apply_styles()


# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "edit_email" not in st.session_state:
    st.session_state.edit_email = False


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 AI Chief of Staff")

    st.markdown("---")

    st.subheader("📌 Example Commands")

    commands = [
    ("🔍 Research", "Research latest OpenAI news"),
    ("📧 Email", "Prepare an email draft"),
    ("📅 Calendar", "Schedule a meeting tomorrow"),
    ("📋 Meeting Brief", "Prepare a brief on Q3 budget"),
    ("🎯 Strategy", "Add or review strategic goals")
]

    for title, command in commands:

      st.markdown(f"**{title}**")

      st.code(command, language="text")
    st.subheader("🧠 Recent Memory")
    history = memory_store.load_memory()

    if history:

        for item in history[-5:]:
            st.write("👤", item["user"])

    else:
        st.write("No memory yet.")

    st.markdown("---")

    if st.button("🗑 Clear Chat", key="sidebar_clear_chat"):

        st.session_state.messages = []
        st.session_state.pending_action = None
        st.session_state.edit_email = False
        memory_store.clear_memory()
        st.rerun()


# ---------------- ROUTING ---------------- #

def route(user_input):

    lower = user_input.lower()

    meeting_keywords = [
        "meeting brief",
        "prepare meeting",
        "prepare a meeting",
        "executive brief",
        "agenda",
        "discussion points",
        "briefing"
    ]

    report_keywords = [
        "executive summary",
        "daily report",
        "weekly report",
        "status report",
        "summarize everything"
    ]

    add_goal_keywords = [
        "add strategic goal",
        "track goal",
        "set objective",
        "set an okr"
    ]

    list_goal_keywords = [
        "show our strategic goals",
        "show strategic goals",
        "list strategic goals",
        "our strategic goals",
        "our priorities"
    ]

    email_keywords = [
        "send email",
        "send an email",
        "draft email",
        "write email",
        "compose email"
    ]

    calendar_keywords = [
    "schedule",
    "scheduled",
    "book a meeting",
    "book meeting",
    "set up a meeting",
    "arrange a meeting",
    "create a meeting",
    "create meeting",
    "create calendar event",
    "add calendar event"
    ]

    if any(k in lower for k in meeting_keywords):
        return "meeting"

    if any(k in lower for k in report_keywords):
        return "report"

    if any(k in lower for k in add_goal_keywords):
        return "add_goal"

    if any(k in lower for k in list_goal_keywords):
        return "list_goals"

    if any(k in lower for k in email_keywords):
        return "email"

    if any(k in lower for k in calendar_keywords):
        return "calendar"

    return "planner"


# ---------------- GOAL HELPERS ---------------- #

def extract_goal_text(user_input):

    if ":" in user_input:
        return user_input.split(":", 1)[1].strip()

    for keyword in [
        "add strategic goal",
        "track goal",
        "set objective",
        "set an okr"
    ]:

        idx = user_input.lower().find(keyword)

        if idx != -1:
            return user_input[idx + len(keyword):].strip(" :-")

    return user_input.strip()


def format_goals(goals):

    if not goals:
        return "No strategic goals tracked yet."

    output = ""

    for g in goals:

        output += (
            f"- {g['goal']} | "
            f"Owner: {g['owner']} | "
            f"Deadline: {g['deadline']} | "
            f"Status: {g['status']}\n"
        )

    return output


# ---------------- EXTRACT PENDING ACTION ---------------- #

def extract_pending_action(result):

    candidates = []

    for item in getattr(result, "new_items", []):

        item_output = getattr(item, "output", None)

        if item_output is not None:
            candidates.append(item_output)

    candidates.append(result.final_output)

    for candidate in candidates:

        if isinstance(candidate, dict):
            data = candidate

        elif isinstance(candidate, str):

            try:
                data = json.loads(candidate)

            except (ValueError, TypeError):
                continue

        else:
            continue

        if not isinstance(data, dict):
            continue

        if data.get("status") == "pending_confirmation":
            return data

    return None


# ---------------- EXECUTE AGENT ---------------- #

async def execute(agent, user_prompt):

    result = await Runner.run(
        agent,
        user_prompt
    )

    return result
# ---------------- CONVERSATION HISTORY ---------------- #

def get_conversation_input():
    return [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages
        if msg["role"] in ["user", "assistant"]
    ]

# ---------------- EXECUTIVE DASHBOARD ---------------- #

st.markdown("""
# 🤖 AI Chief of Staff

Your intelligent executive workspace for managing
research, meetings, emails and strategic goals.
""")

st.markdown("### Overview")

goals = list_goals()
memory_history = memory_store.load_memory()

total_requests = len([
    m for m in st.session_state.messages
    if m["role"] == "user"
])

active_goals = len([
    g for g in goals
    if str(g.get("status", "")).lower()
    not in ["completed", "complete"]
])

pending_approvals = (
    1 if st.session_state.pending_action else 0
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💬 Total Requests", total_requests)

with c2:
    st.metric("🎯 Active Goals", active_goals)

with c3:
    st.metric("🧠 Memory Records", len(memory_history))

with c4:
    st.metric("⏳ Pending Approvals", pending_approvals)

st.markdown("---")

# Workspace overview

st.markdown("### Your Workspace")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔍 Research")
    st.caption(
        "Explore topics, discover insights "
        "and generate research summaries."
    )

with col2:
    st.markdown("#### 📧 Communication")
    st.caption(
        "Prepare professional emails "
        "and review drafts before sending."
    )

with col3:
    st.markdown("#### 📅 Operations")
    st.caption(
        "Manage meetings, strategic goals "
        "and executive activities."
    )

st.markdown("---")

# ---------------- CHAT HISTORY ---------------- #
st.markdown("## 💬 AI Assistant")

st.caption(
    "Ask your AI Chief of Staff to research, "
    "manage emails, schedule meetings and more."
)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- USER INPUT ---------------- #

prompt = st.chat_input(
    "Type your request...",
    disabled=st.session_state.pending_action is not None
)


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    status = st.empty()

    route_type = route(prompt)

    try:

        # ---------------- MEETING ---------------- #

        if route_type == "meeting":

            status.info("📋 Meeting Preparation Agent")

            with st.spinner("Preparing meeting brief..."):

                output = prepare_meeting(prompt)


        # ---------------- REPORT ---------------- #

        elif route_type == "report":

            status.info("📊 Report Generator Agent")

            with st.spinner("Generating executive report..."):

                output = generate_executive_report()


        # ---------------- ADD GOAL ---------------- #

        elif route_type == "add_goal":

            status.info("🎯 Strategy Tracker Agent")

            with st.spinner("Saving strategic goal..."):

                output = add_goal(extract_goal_text(prompt))


        # ---------------- LIST GOALS ---------------- #

        elif route_type == "list_goals":

            status.info("🎯 Strategy Tracker Agent")

            with st.spinner("Loading strategic goals..."):

                output = format_goals(list_goals())


        # ---------------- EMAIL ---------------- #

        elif route_type == "email":

            status.info("📧 Email Agent")

            with st.spinner("Preparing email draft..."):

                result = asyncio.run(
                    execute(email_agent, prompt)
                )

                pending = extract_pending_action(result)

                if not pending:
                    raise ValueError(
                        "Email draft could not be extracted. "
                        "No email was sent."
                    )

                st.session_state.pending_action = {
                    "type": "email",
                    "data": pending
                }

                st.session_state.edit_email = False

                output = (
                    "📧 Email draft prepared successfully. "
                    "Review it below before sending."
                )


        # ---------------- CALENDAR ---------------- #

        elif route_type == "calendar":

            status.info("📅 Calendar Agent")

            with st.spinner("Preparing calendar event..."):

                result = asyncio.run(
                    execute(calendar_agent, prompt)
                )

                pending = extract_pending_action(result)

                if not pending:
                    raise ValueError(
                        "Calendar event details could not be extracted. "
                        "No event was created."
                    )

                st.session_state.pending_action = {
                    "type": "calendar",
                    "data": pending
                }

                output = (
                    "📅 Calendar event prepared successfully. "
                    "Review it below before creating."
                )


        # ---------------- PLANNER ---------------- #

        else:

            status.info("🧠 Planner Agent")

            with st.spinner("Working..."):

               conversation_input = get_conversation_input()

               result = asyncio.run(
                            execute(planner_agent, conversation_input)
                           )

               output = result.final_output

        status.success("✅ Completed")

        st.session_state.messages.append({
            "role": "assistant",
            "content": str(output)
        })

        memory_store.save_memory(prompt, str(output))

        with st.chat_message("assistant"):
            st.markdown(output)

    except Exception as e:

        status.error(f"Something went wrong: {str(e)}")


# ---------------- CONFIRMATION SECTION ---------------- #

pending = st.session_state.pending_action

if pending:

    st.markdown("---")

    # ---------------- EMAIL PREVIEW ---------------- #

    if pending["type"] == "email":

        data = pending["data"]

        st.subheader("📧 Email Preview")

        if st.session_state.edit_email:

            st.subheader("✏️ Edit Your Email")

            edited_to = st.text_input(
                "Recipient Email",
                value=data["to"],
                key="edited_email_to"
            )

            edited_subject = st.text_input(
                "Subject",
                value=data["subject"],
                key="edited_email_subject"
            )

            edited_body = st.text_area(
                "Email Body",
                value=data["body"],
                height=250,
                key="edited_email_body"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("💾 Save Changes"):

                    if (
                        not edited_to.strip()
                        or "@" not in edited_to
                    ):
                        st.error("Enter a valid recipient email.")

                    elif not edited_subject.strip():
                        st.error("Subject cannot be empty.")

                    elif not edited_body.strip():
                        st.error("Email body cannot be empty.")

                    else:

                        data["to"] = edited_to.strip()
                        data["subject"] = edited_subject.strip()
                        data["body"] = edited_body.strip()

                        st.session_state.pending_action["data"] = data

                        st.session_state.edit_email = False

                        st.success("Email updated successfully!")

                        st.rerun()

            with col2:

                if st.button("↩️ Back to Preview"):

                    st.session_state.edit_email = False
                    st.rerun()

        else:

            st.write("**To:**", data["to"])

            st.write("**Subject:**", data["subject"])

            st.markdown("**Email Body:**")

            st.text(data["body"])

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button("✏️ Edit Email"):

                    st.session_state.edit_email = True
                    st.rerun()

            with col2:

                if st.button("✅ Confirm & Send"):

                    try:

                        with st.spinner("Sending email..."):

                            result = send_email(
                                data["to"],
                                data["subject"],
                                data["body"]
                            )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "✅ " + result
                        })

                        st.session_state.pending_action = None
                        st.session_state.edit_email = False

                        st.success(result)

                        st.rerun()

                    except Exception as e:

                        st.error(f"Email sending failed: {str(e)}")

            with col3:

                if st.button("❌ Cancel Email"):

                    st.session_state.pending_action = None
                    st.session_state.edit_email = False

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Email cancelled. No email was sent."
                    })

                    st.rerun()


    # ---------------- CALENDAR PREVIEW ---------------- #

    elif pending["type"] == "calendar":

        data = pending["data"]

        st.subheader("📅 Calendar Event Preview")

        st.write("**Event Title:**", data["title"])

        st.write("**Start:**", data["start"])

        st.write("**End:**", data["end"])

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✅ Confirm & Create Event"):

                try:

                    with st.spinner("Creating calendar event..."):

                        result = create_event(
                            data["title"],
                            data["start"],
                            data["end"]
                        )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "✅ " + result
                    })

                    st.session_state.pending_action = None

                    st.success(result)

                    st.rerun()

                except Exception as e:

                    st.error(f"Calendar creation failed: {str(e)}")

        with col2:

            if st.button("❌ Cancel Event"):

                st.session_state.pending_action = None

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Calendar event cancelled. No event was created."
                })

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