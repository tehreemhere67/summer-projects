import json #storing each task as a dictionary. the list of dictionaries/tasks stored in the json file.

def add_task():
    name = input("Enter task name: ")
    priority = input("Enter priority (high/medium/low): ")
    due_date = input("Enter due date: ")
    task = {"name": name, "priority": priority, "due_date": due_date, "done": False}
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
        tasks.append(task)
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)
    except FileNotFoundError:
        with open("tasks.json", "w") as f:
            json.dump([task], f)

def view_tasks():
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task['name']} | {task['priority']} | due: {task['due_date']} | done: {task['done']}")

def mark_task_done():
    view_tasks()
    task_number= int(input("Enter the task number to mark done: "))
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    tasks[task_number - 1]["done"] = True
    with open("tasks.json", "w") as f:
            json.dump(tasks, f)
    
def delete_task():
    view_tasks()
    task_number= int(input("Enter the task number to delete: "))
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    tasks.pop(task_number-1)
    with open("tasks.json", "w") as f:
            json.dump(tasks, f)
    
def main():
    while True:
        print("\n1. Add task")
        print("2. View all tasks")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Quit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            add_task()
        elif choice == 2:
            view_tasks()
        elif choice == 3:
            mark_task_done()
        elif choice == 4:
            delete_task()
        elif choice ==5:
            break
main()