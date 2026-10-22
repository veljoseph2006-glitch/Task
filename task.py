from datetime import datetime

class Task:
    def __init__(self, task_id, title, description="", due_date=None, priority="Medium"):
        # Encapsulated attributes
        self.__task_id = task_id
        self.__title = title
        self.__description = description
        self.__due_date = due_date
        self.__priority = priority  # High / Medium / Low
        self.__is_completed = False
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Getters (read-only access)
    @property
    def task_id(self): return self.__task_id
    @property
    def title(self): return self.__title
    @property
    def description(self): return self.__description
    @property
    def due_date(self): return self.__due_date
    @property
    def priority(self): return self.__priority
    @property
    def is_completed(self): return self.__is_completed
    @property
    def created_at(self): return self.__created_at

    # Setters with validation
    def update(self, title=None, description=None, due_date=None, priority=None):
        if title: self.__title = title
        if description: self.__description = description
        if due_date: self.__due_date = due_date
        if priority:
            if priority in ["High", "Medium", "Low"]:
                self.__priority = priority
            else:
                raise ValueError("Priority must be: High, Medium, or Low")

    def mark_complete(self):
        if self.__is_completed:
            return False  # Already completed
        self.__is_completed = True
        return True

    def to_dict(self):
        """Convert task to dictionary for file saving"""
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
        """Create Task object from dictionary"""
        task = cls(
            data["task_id"],
            data["title"],
            data["description"],
            data["due_date"],
            data["priority"]
        )
        if data.get("is_completed"):
            task.mark_complete()
        return task