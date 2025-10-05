# Noted - Task Notifier CLI

**Noted** is a command-line tool for scheduling tasks and break notifications, with a background daemon to ensure you never miss a notification—even if you close the CLI.

---

## Features

- Add tasks with durations and automatic breaks between them.
- Specify break duration in your task file.
- Get notifications when tasks start, when breaks start, and when tasks are completed.
- Background daemon ensures notifications and cleanup even if CLI is closed.
- Tasks are automatically deleted after completion.

---

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/noted.git
    cd noted/app
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

---

## Usage

### Add a Single Task

```sh
python3 main.py noted "Write report" --duration 30 --start-in 5
```
- Adds a task "Write report" for 30 minutes, starting in 5 minutes.

### Load Tasks from a File

Prepare a file (e.g., `test.txt`):

```
1. Work on RL for 1 minutes
2. Read TLOHN for 1 minutes
3. Visit tradingview and explore the markets for 2 minutes
4. Learn Chinese for 2 minutes
break=20
```
- The last line (`break=20`) sets the break duration (in minutes) between tasks.

Run:
```sh
python3 main.py noted --load "/path/to/test.txt"
```

### List Scheduled Tasks

```sh
python3 main.py list
```

---

## How Breaks Work

- After each task, a break is automatically scheduled.
- The break duration is set by the `break=XX` line in your task file (default is 20 minutes if not specified).
- Notifications are sent for task start, task completion, and break start.

---

## Daemon

- The daemon runs in the background and checks for tasks to notify and delete every 5 seconds.
- It is started automatically if not already running when you use the CLI.
- To stop the daemon, kill the process manually (e.g., `pkill -f daemon.py`).

---

## File Structure

- `main.py` — CLI for adding/listing tasks.
- `daemon.py` — Background process for notifications and cleanup.
- `load_tasks.py` — Parses task files.
- `utils.py` — Handles task ordering and break scheduling.
- `tasks.json` — Stores scheduled tasks.

---

## Requirements

- Python 3.8+
- [plyer](https://github.com/kivy/plyer) (for notifications)
- Linux (for best notification and sound support)

---

## License

MIT License

---

## Author

[Victor Martin]