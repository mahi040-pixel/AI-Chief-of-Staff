import json
import os

FILE = "strategy.json"


def _load():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        content = f.read().strip()

    if not content:
        return []

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return []


def _save(goals):
    with open(FILE, "w") as f:
        json.dump(goals, f, indent=4)


def add_goal(goal, owner="CEO", deadline="Not set"):
    goals = _load()

    for g in goals:
        if g["goal"].lower() == goal.lower():
            return f"Goal '{goal}' is already tracked (status: {g['status']}). Use update to change it, not add."

    goals.append({
        "goal": goal,
        "owner": owner,
        "deadline": deadline,
        "status": "Not Started",
        "progress_notes": []
    })

    _save(goals)

    return f"Strategic goal added: {goal}"


def list_goals():
    return _load()


def update_goal_status(goal, status, note=None):
    goals = _load()

    updated = False

    for g in goals:
        if g["goal"].lower() == goal.lower():
            g["status"] = status

            if note:
                g["progress_notes"].append(note)

            updated = True

    _save(goals)

    if updated:
        return f"Updated '{goal}' to status: {status}"

    return f"Goal '{goal}' not found. Use the exact goal text, or add it first."