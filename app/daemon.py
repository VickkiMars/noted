import json
import time
from pathlib import Path
from plyer import notification
from datetime import datetime, timedelta
import subprocess
import platform
from main import notify

TASKS_FILE = Path("tasks.json")
DEFAULT_SOUND = "assets/cheerful-527.wav"

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
        
def main():
    print("Noted Daemon started. Monitoring tasks...")
    while True:
        tasks = load_tasks()
        now = datetime.now()
        changed = False
        new_tasks = []
        for task in tasks:
            start_time = datetime.fromisoformat(task["start_time"])
            duration = task.get("duration_min", 30)
            end_time = start_time + timedelta(minutes=duration)
            expected_termination_time = datetime.fromisoformat(task.get("expected_termination_time"))

            # Send "Task Started" notification if it's time and not already notified
            if start_time <= now < end_time and not task.get("notified_start"):
                if task.get("title"):
                    notify(task["title"], task["message"])
                else:
                    notify("Task Started", task["message"])
                task["notified_start"] = True
                changed = True

            # Send "Task Completed" notification if duration is up, but only once
            if end_time <= now < expected_termination_time and not task.get("notified_completed"):
                if task.get("title"):
                    notify(task["title"], "Break is over")
                else:
                    notify("Task Completed", f"{task['message']} - Time's up!")
                task["notified_completed"] = True
                changed = True

            # Delete task if expected_termination_time is up
            if expected_termination_time > now:
                new_tasks.append(task)
            else:
                changed = True  # Task is expired and will be deleted

        if changed:
            save_tasks(new_tasks)
        time.sleep(5)

if __name__ == "__main__":
    main()