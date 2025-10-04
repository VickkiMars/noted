import typer
import threading
import json
from pathlib import Path
from plyer import notification
from datetime import datetime, timedelta
import subprocess
import platform

app = typer.Typer(help="NOTED CLI - Task notifier")

TASKS_FILE = Path("tasks.json")
DEFAULT_SOUND = "/home/kami/Desktop/codebase/noted/assets/cheerful-527.wav"

# ----------------------
# Helper functions
# ----------------------

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

def notify(title: str, message: str):
    notification.notify(title=title,
                        message=message,
                        timeout=5,
                        app_name="Noted",
                        app_icon="/home/kami/Desktop/codebase/noted/noted.png"
                        )
    if platform.system() == "Linux":
        subprocess.Popen(['aplay', DEFAULT_SOUND], stderr=subprocess.DEVNULL)

def remove_expired_tasks():
    """Remove tasks whose expected_termination_time is in the past."""
    tasks = load_tasks()
    now = datetime.now()
    new_tasks = []
    for task in tasks:
        expected_termination_time = datetime.fromisoformat(task.get("expected_termination_time"))
        if expected_termination_time > now:
            new_tasks.append(task)
    if len(new_tasks) != len(tasks):
        save_tasks(new_tasks)

# def schedule_task_notifications(task):
#     start_time = datetime.fromisoformat(task["start_time"])
#     duration = task.get("duration_min", 30)

#     now = datetime.now()
#     delay_start = max((start_time - now).total_seconds(), 0)
#     delay_reminder = delay_start + 2*60
#     delay_stop = delay_start + duration*60

#     def on_task_completed():
#         notify("Time's Up!", f"{task['message']}")
#         # Do not remove the task here; the daemon will handle deletion after 10s

#     # Schedule notifications
#     t1 = threading.Timer(delay_start, notify, args=("Task Started", task["message"]))
#     t2 = threading.Timer(delay_reminder, notify, args=("Reminder", task["message"]))
#     t3 = threading.Timer(delay_stop, on_task_completed)
#     for t in [t1, t2, t3]:
#         t.daemon = True  # Keep process alive for timers
#         t.start()

# ----------------------
# CLI Commands
# ----------------------

@app.command()
def noted(
    task_message: str = typer.Argument(..., help="Task description"),
    duration: int = typer.Option(30, "--duration", "-d", help="Duration in minutes"),
    start_in: int = typer.Option(0, "--start-in", "-s", help="Delay start in minutes")
):
    """Add a new task and schedule notifications."""
    start_time = datetime.now() + timedelta(minutes=start_in)
    expected_termination_time = start_time + timedelta(minutes=duration, seconds=10)
    task = {
        "message": task_message,
        "start_time": start_time.isoformat(),
        "duration_min": duration,
        "expected_termination_time": expected_termination_time.isoformat()
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    notify(title="Task Started", message=task_message)
    typer.echo(f"Task noted: '{task_message}' for {duration} min(s), starting in {start_in} min(s).")

@app.command("list")
def list_tasks():
    """
    List all scheduled (not yet expired) tasks.
    """
    remove_expired_tasks()
    tasks = load_tasks()
    now = datetime.now()
    upcoming_tasks = []
    for task in tasks:
        start = datetime.fromisoformat(task["start_time"])
        duration = task.get("duration_min", 30)
        end = start + timedelta(minutes=duration)
        expected_termination_time = datetime.fromisoformat(task.get("expected_termination_time"))
        if expected_termination_time > now:
            upcoming_tasks.append((task, start, end, expected_termination_time))
    if not upcoming_tasks:
        typer.echo("No upcoming tasks scheduled.")
        return

    for i, (task, start, end, expected_termination_time) in enumerate(upcoming_tasks, start=1):
        typer.echo(
            f"{i}. {task['message']} (Start: {start}, End: {end}, Duration: {task.get('duration_min', 30)} min, "
            f"Delete After: {expected_termination_time})"
        )

# ----------------------
# Entry point
# ----------------------

if __name__ == "__main__":
    # Remove expired tasks on startup
    remove_expired_tasks()
    app()