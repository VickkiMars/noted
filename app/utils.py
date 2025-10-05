from datetime import datetime, timedelta

now = datetime.now()
BREAK = [1, 1] # [Minutes, Seconds]
def handle_order(tasks, break_minutes):
    ordered_tasks = []
    for task in tasks:
        stop_time = now + timedelta(minutes=task[-1])
        if ordered_tasks != []:
            start_time = datetime.fromisoformat(ordered_tasks[-1][-1]) + timedelta(minutes=break_minutes, seconds=4)
            stop_time = start_time + timedelta(minutes=task[-1])
            ordered_tasks.append(
                (task[0], start_time.isoformat(), stop_time.isoformat())
            )
        else:
            start_time = now + timedelta(seconds=10) # 10 Seconds for the user to set things up
            ordered_tasks.append(
                (task[0], start_time.isoformat(), stop_time.isoformat())
            )
    return ordered_tasks

if __name__ == "__main__":
    from app.load_tasks import load_file

    file = load_file("/home/kami/Desktop/codebase/noted/test.txt")
    all_tasks = handle_order(tasks=file)

    for task in all_tasks:
        start = datetime.fromisoformat(task[1])
        stop = datetime.fromisoformat(task[-1])
        print(f"Task: {task[0]} will begin by {start.hour}:{start.minute}")
