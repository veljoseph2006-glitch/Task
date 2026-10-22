import json
from datetime import datetime

FILE_NAME = "tasks_data.json"


class Task:
    def __init__(self, task_id, title, description="", due_date=None, priority="Medium"):
        self.__task_id = task_id
        self.__title = title
        self.__description = description
        self.__due_date = due_date
        self.__priority = priority
        self.__is_completed = False
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def task_id(self):
        return self.__task_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def due_date(self):
        return self.__due_date

    @property
    def priority(self):
        return self.__priority

    @property
    def is_completed(self):
        return self.__is_completed

    @property
    def created_at(self):
        return self.__created_at

    def update(self, title=None, description=None, due_date=None, priority=None):
        if title: self.__title = title
        if description: self.__description = description
        if due_date: self.__due_date = due_date
        if priority and priority in ["High", "Medium", "Low"]:
            self.__priority = priority

    def mark_complete(self):
        if self.__is_completed:
            return False
        self.__is_completed = True
        return True

    def to_dict(self):
        return {
            "task_id": self.__task_id,
            "title": self.__title,
            "description": self.__description,
            "due_date": self.__due_date,
            "priority": self.__priority,
            "is_completed": self.__is_completed,
            "created_at": self.__created_at
        }

    @classmethod
    def from_dict(cls, data):
        t = cls(
            data["task_id"],
            data["title"],
            data["description"],
            data["due_date"],
            data["priority"]
        )
        if data.get("is_completed"):
            t.mark_complete()
        return t


def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)
        return True
    except Exception as e:
        print(f"❌ Save error: {e}")
        return False


def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            return [Task.from_dict(d) for d in json.load(f)]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"⚠️ Load warning: Starting fresh. ({e})")
        return []


def display_header(title):
    print("\n" + "=" * 50)
    print(f"   {title}")
    print("=" * 50)


def display_summary(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t.is_completed)
    pending = total - done
    print(f"\n📊 Total: {total}  |  ✅ Done: {done}  |  ⏳ Pending: {pending}")


def display_task(task):
    status = "✅ COMPLETED" if task.is_completed else "⏳ PENDING"
    print(f"\n  ID: {task.task_id}")
    print(f"  Title: {task.title}")
    if task.description:
        print(f"  Note: {task.description}")
    if task.due_date:
        print(f"  Due: {task.due_date}")
    print(f"  Priority: {task.priority}  |  Status: {status}")


tasks = load_tasks()
next_id = max((t.task_id for t in tasks), default=0) + 1


def add_task():
    global next_id
    display_header("ADD NEW TASK")
    title = input("  Task title: ").strip()
    if not title:
        print("  ❌ Title cannot be empty")
        return
    desc = input("  Description: ").strip()
    due = input("  Due date: ").strip() or None
    priority = input("  Priority (High/Medium/Low): ").strip().capitalize() or "Medium"

    tasks.append(Task(next_id, title, desc, due, priority))
    save_tasks(tasks)
    print(f"  ✅ Task added! ID: {next_id}")
    next_id += 1


def edit_task():
    display_header("EDIT TASK")
    if not tasks:
        print("  📭 No tasks yet")
        return
    try:
        tid = int(input("  Task ID to edit: "))
    except ValueError:
        print("  ❌ Please enter a number")
        return
    task = next((t for t in tasks if t.task_id == tid), None)
    if not task:
        print("  ❌ Task not found")
        return
    display_task(task)
    title = input(f"  New title [{task.title}]: ").strip() or task.title
    desc = input(f"  New description: ").strip() or task.description
    due = input(f"  New due date: ").strip() or task.due_date
    priority = input(f"  New priority [{task.priority}]: ").strip().capitalize() or task.priority
    task.update(title, desc, due, priority)
    save_tasks(tasks)
    print("  ✅ Task updated!")


def delete_task():
    display_header("DELETE TASK")
    if not tasks:
        print("  📭 No tasks yet")
        return
    try:
        tid = int(input("  Task ID to delete: "))
    except ValueError:
        print("  ❌ Please enter a number")
        return
    task = next((t for t in tasks if t.task_id == tid), None)
    if not task:
        print("  ❌ Task not found")
        return
    display_task(task)
    confirm = input("  ⚠️ Delete this task? (Y/N): ").strip().upper()
    if confirm == "Y":
        tasks.remove(task)
        save_tasks(tasks)
        print("  ✅ Task deleted")
    else:
        print("  Deletion cancelled")


def view_all():
    display_header("ALL TASKS")
    if not tasks:
        print("  📭 No tasks found. Add your first task!")
        return
    print(f"\n  {'ID':<5}{'Title':<25}{'Priority':<10}{'Status':<12}")
    print("  " + "-" * 52)
    for t in tasks:
        status = "✅ Done" if t.is_completed else "⏳ Pending"
        print(f"  {t.task_id:<5}{t.title[:23]:<25}{t.priority:<10}{status:<12}")
    display_summary(tasks)


def search_filter():
    display_header("SEARCH & FILTER")
    print("  1 = All Tasks")
    print("  2 = Pending Only")
    print("  3 = Completed Only")
    print("  4 = Priority: High")
    print("  5 = Priority: Medium")
    print("  6 = Priority: Low")
    print("  7 = Search by Keyword")
    opt = input("\n  Choose option: ").strip()
    result = []
    if opt == "1":
        result = tasks
    elif opt == "2":
        result = [t for t in tasks if not t.is_completed]
    elif opt == "3":
        result = [t for t in tasks if t.is_completed]
    elif opt == "4":
        result = [t for t in tasks if t.priority == "High"]
    elif opt == "5":
        result = [t for t in tasks if t.priority == "Medium"]
    elif opt == "6":
        result = [t for t in tasks if t.priority == "Low"]
    elif opt == "7":
        kw = input("  Enter search word: ").lower()
        result = [t for t in tasks if kw in t.title.lower() or kw in t.description.lower()]
    else:
        print("  ❌ Invalid option")
        return

    if not result:
        print("  🔍 No matching tasks found")
    else:
        print(f"\n  📋 {len(result)} result(s):")
        for t in result:
            display_task(t)


def mark_complete():
    display_header("MARK TASK COMPLETE")
    if not tasks:
        print("  📭 No tasks yet")
        return
    try:
        tid = int(input("  Enter Task ID: "))
    except ValueError:
        print("  ❌ Please enter a number")
        return
    task = next((t for t in tasks if t.task_id == tid), None)
    if not task:
        print("  ❌ Task not found")
        return
    if task.mark_complete():
        save_tasks(tasks)
        print("  ✅ Task marked as complete! 🎉")
    else:
        print("  ⚠️ This task is already completed")


if __name__ == "_main_":
    display_header("📋 DAILY TASK TO-DO LIST")
    print("   Welcome! Your tasks save automatically. ✅")
    display_summary(tasks)

    while True:
        print("\n" + "-" * 50)
        print("  MAIN MENU")
        print("  1. Add New Task")
        print("  2. Edit Task")
        print("  3. Delete Task")
        print("  4. View All Tasks")
        print("  5. Search / Filter")
        print("  6. Mark Task Complete")
        print("  0. Exit")
        print("-" * 50)

        choice = input("  Enter your choice (0-6): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            edit_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            view_all()
        elif choice == "5":
            search_filter()
        elif choice == "6":
            mark_complete()
        elif choice == "0":
            print("\n👋 Thank you for using Daily Task To-Do List!")
            print("   💾 Your tasks have been saved. Goodbye!\n")
            break
        else:
            print("  ❌ Invalid choice — please enter 0 to 6")