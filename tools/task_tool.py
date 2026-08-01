import json
import os

FILE = "tasks.json"

def add_task(task):

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

    tasks.append(task)

    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

    return "Task added successfully."


def show_tasks():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)