def display_header(title):
    print("\n" + "=" * 50)
    print(f"   {title}")
    print("=" * 50)

def display_summary(tasks):
    """Show Total / Done / Pending — matches your UI!"""
    total = len(tasks)
    done = sum(1 for t in tasks if t.is_completed)
    pending = total - done

    print("\n📊 SUMMARY")
    print(f"   Total:     {total}")
    print(f"   ✅ Done:   {done}")
    print(f"   ⏳ Pending: {pending}")
    print("-" * 50)

def display_task(task):
    """Format a single task for display"""
    status = "✅ COMPLETED" if task.is_completed else "⏳ PENDING"
    print(f"  ID: {task.task_id}")
    print(f"  Title: {task.title}")
    if task.description:
        print(f"  Description: {task.description}")
    if task.due_date:
        print(f"  Due Date: {task.due_date}")
    print(f"  Priority: {task.priority}")
    print(f"  Status: {status}")
    print(f"  Created: {task.created_at}")
    print("  " + "-" * 40)

def get_valid_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  ⚠️ Please enter something or press Enter to skip.")

def get_priority():
    while True:
        p = input("  Priority (High/Medium/Low) [Medium]: ").strip().capitalize()
        if p == "":
            return "Medium"
        if p in ["High", "Medium", "Low"]:
            return p
        print("  ❌ Please enter: High, Medium, or Low")