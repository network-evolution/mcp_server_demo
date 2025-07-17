# server.py
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import json,os
from dateparser.search import search_dates

load_dotenv()

# Create an MCP server
mcp = FastMCP("ToDoListWithDate")

TASK_FILE = "/Users/dev/gitdir/mcp_demo_new/todo_list_apps/todo_tasks_with_date.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            json.dump([], f)
    with open(TASK_FILE, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

tasks = load_tasks()
next_id = max([t["id"] for t in tasks], default=0) + 1 if tasks else 1

@mcp.tool()
def add_task(task: str) -> str:
    """Add a new task to the to-do list"""
    global next_id

    parsed_date = search_dates(task)
    if parsed_date:
        _, dt = parsed_date[-1]
        due_date = dt.strftime("%Y-%m-%d")
        task = task.replace(parsed_date[-1][0], "").strip()

    # print(due_date)
    # print(task)

    new_task = {"id": next_id, "task": task, "completed": False, "due":due_date}
    tasks.append(new_task)
    save_tasks(tasks)
    next_id += 1
    return f"Task added: {new_task['id']}. {task}"

# add_task("Client Meeting on 22 June 2025")
@mcp.tool()
def complete_task(task_id: int) -> str:
    """Mark a task as completed"""
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                return f"Task {task_id} is already completed."
            task["completed"] = True
            save_tasks(tasks)
            return f"Task {task_id} marked as completed."
    return f"Task {task_id} not found."

@mcp.tool()
def list_tasks() -> str:
    """List all tasks"""
    if not tasks:
        return "Your to-do list is empty."
    result = []
    for t in tasks:
        status = "✅" if t["completed"] else "🕗"
        due = f" (Due: {t['due']})" if t.get("due") else ""
        result.append(f"{t['id']}. {t['task']} {due} {status}")
    return "\n".join(result)