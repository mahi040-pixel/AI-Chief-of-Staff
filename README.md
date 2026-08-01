# 🤖 AI Chief of Staff

An intelligent **Multi-Agent Executive Assistant** built using the **OpenAI Agents SDK**, **Python**, **Streamlit**, and various productivity APIs. This project acts as a virtual Chief of Staff for a CEO by assisting with research, email management, meeting scheduling, task management, and executive decision support while incorporating human approval for critical actions.

---

# 🚀 Features

### 🧠 Executive Planner
- Acts as the central decision-making agent.
- Routes user requests to the appropriate specialized agent.
- Coordinates workflows between multiple agents.

### 🔍 Research Analyst
- Performs real-time web research using the Tavily Search API.
- Summarizes research into concise executive-friendly bullet points.
- Retrieves the latest information from trusted web sources.

### 📧 Email Manager
- Drafts professional emails.
- Sends emails through the Gmail API.
- Uses OAuth authentication for secure access.
- Requires human approval before sending.

### 📅 Meeting Manager
- Schedules meetings directly in Google Calendar.
- Integrates with Google Calendar API.
- Creates calendar events with title, date, and time.
- Uses OAuth authentication.

### ✅ Task Manager
- Creates task lists.
- Stores tasks locally.
- Displays pending tasks.
- Helps manage executive priorities.

### 📝 Review Agent
- Reviews written content.
- Improves grammar and clarity.
- Summarizes text.
- Produces professional executive communication.

### 💾 Memory System
- Stores approved conversations.
- Maintains conversation history.
- Provides lightweight context for future interactions.

### 👤 Human Approval
- Critical actions require user confirmation.
- Prevents accidental execution.
- Ensures executive oversight.

---

# 🏗️ Project Architecture

```
                        User
                          │
                          ▼
                Executive Planner Agent
                          │
     ┌──────────┬──────────┼──────────┬──────────┐
     ▼          ▼          ▼          ▼          ▼
 Research    Email      Calendar     Task      Review
  Agent      Agent        Agent      Agent      Agent
     │          │           │           │
     └──────────┴───────────┴───────────┘
                    │
                Memory System
                    │
             Human Approval Layer
```

---

# 🛠️ Tech Stack

- Python 3.13
- OpenAI Agents SDK
- Streamlit
- Tavily Search API
- Gmail API
- Google Calendar API
- Google OAuth 2.0
- JSON
- dotenv

---

# 📁 Project Structure

```
AI-Chief-of-Staff/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
├── credentials.json
├── token.json
│
├── my_agents/
│   ├── planner.py
│   ├── research.py
│   ├── email.py
│   ├── calendar.py
│   ├── task.py
│   ├── review.py
│   └── meeting.py
│
├── tools/
│   ├── search_tool.py
│   ├── gmail_tool.py
│   ├── calendar_tool.py
│   ├── task_tool.py
│   └── meeting_tool.py
│
├── memory/
│   ├── memory.py
│   └── data.json
│
├── prompts/
│
└── tasks.json
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Chief-of-Staff.git
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

# ▶️ Run Terminal Version

```bash
python main.py
```

---

# 🌐 Run Streamlit Interface

```bash
streamlit run app.py
```

---

# 📌 Example Commands

### Research

```
Research latest OpenAI news
```

### Email

```
Send an email to example@gmail.com
```

### Calendar

```
Schedule a meeting tomorrow at 5 PM
```

### Tasks

```
Create a task list for project submission
```

### Review

```
Review this executive summary
```

---

# 🔄 Workflow

1. User submits a request.
2. Executive Planner analyzes the request.
3. Appropriate specialized agent is selected.
4. Agent performs the required task.
5. Human approval is requested for critical actions.
6. Approved interactions are stored in memory.
7. Final response is returned to the user.

---

# 🔒 Security

- OAuth 2.0 Authentication
- Gmail API Authorization
- Google Calendar Authorization
- Environment Variable Protection
- Human Approval Before Critical Actions

---

# 🎯 Future Enhancements

- Strategy Tracking Agent
- Executive Report Generator
- Slack Integration
- Microsoft Outlook Integration
- Microsoft Teams Integration
- PDF Report Generation
- Meeting Minutes Generation
- Voice Assistant Support
- Dashboard Analytics

---

# 👨‍💻 Author

**Mahi Varshney**

Indira Gandhi Delhi Technical University for Women

---

# 📜 License

This project is developed for academic and educational purposes.
