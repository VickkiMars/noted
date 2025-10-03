import typer
import threading
import json
from pathlib import Path
from plyer import notification
from datetime import datetime, timedelta
import subprocess
import platform
import time

app = typer.Typer(help="NOTED CLI - Task notifier")

TASKS_FILE = Path("tasks.json")
DEFAULT_SOUND = "/home/kami/Desktop/codebase/noted/assets/cheerful-527.wav"

# ----------------------
# Helper functions
# ----------------------

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

def notify(title: str, message: str):
    notification.notify(title=title, message=message, timeout=5)
    if platform.system() == "Linux":
        subprocess.Popen(['aplay', DEFAULT_SOUND], stderr=subprocess.DEVNULL)

def schedule_task_notifications(task):
    start_time = datetime.fromisoformat(task["start_time"])
    duration = task.get("duration_min", 30)

    now = datetime.now()
    delay_start = max((start_time - now).total_seconds(), 0)
    delay_reminder = delay_start + 2*60
    delay_stop = delay_start + duration*60

    for delay, title in [
        (delay_start, "Task Started"),
        (delay_reminder, "Reminder"),
        (delay_stop, "Task Completed")
    ]:
        msg = task["message"] if title != "Task Completed" else f"{task['message']} - Time's up!"
        t = threading.Timer(delay, notify, args=(title, msg))
        t.daemon = True
        t.start()

# ----------------------
# CLI Commands
# ----------------------

@app.command()
def noted(
    task_message: str = typer.Argument(..., help="Task description"),
    duration: int = typer.Option(30, "--duration", "-d", help="Duration in minutes"),
    start_in: int = typer.Option(0, "--start-in", "-s", help="Delay start in minutes")
):
    start_time = datetime.now() + timedelta(minutes=start_in)
    task = {
        "message": task_message,
        "start_time": start_time.isoformat(),
        "duration_min": duration
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    schedule_task_notifications(task)
    time.sleep(1)
    typer.echo(f"Task noted: '{task_message}' for {duration} min(s), starting in {start_in} min(s).")

@app.command("list")
def list_tasks():
    """
    List all scheduled tasks.
    """
    tasks = load_tasks()
    if not tasks:
        typer.echo("No tasks scheduled.")
        return

    for i, task in enumerate(tasks, start=1):
        start = datetime.fromisoformat(task["start_time"])
        typer.echo(f"{i}. {task['message']} (Start: {start}, Duration: {task.get('duration_min', 30)} min)")

# ----------------------
# Entry point
# ----------------------

if __name__ == "__main__":
    app()
