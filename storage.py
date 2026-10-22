import json
from task import Task

FILE_NAME = "tasks_data.json"

def save_tasks(tasks):
    """Save all tasks to JSON file"""
    try:
        data = [task.to_dict() for task in tasks]
        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return False

def load_tasks():
    """Load tasks from JSON file"""
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]
    except FileNotFoundError:
        return []  # No file yet — return empty list
    except Exception as e:
        print(f"❌ Error loading: {e}")
        return []