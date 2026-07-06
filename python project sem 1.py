# Python Project Sem 1
# Ankita Tiwari
# F127

print("Ankita Tiwari F127")

from datetime import datetime
import os#for file deletion

tasks = []# List to store all task tuples
task_titles = set()# Set to store titles for duplicate checking
FILENAME = "my_tasks.txt"


# ~~~~~~~~~~~~~~~ Load Tasks from File~~~~~~~~~~~~~~~~


def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    title, status, date = parts
                    tasks.append((title, status, date))# Using tuple
                    task_titles.add(title)
        print("Tasks loaded successfully!\n")
    except FileNotFoundError:
        print("No saved tasks found.\n")
    except Exception as e:
        print(f"Error loading tasks: {e}\n")


#~~~~~~~~~~~~~~~ Save Tasks to File ~~~~~~~~~~~~~~~~~~~~


def save_tasks():
    try:
        with open(FILENAME, "w") as file:
            for task in tasks:
                file.write(f"{task[0]}|{task[1]}|{task[2]}\n")
    except Exception as e:
        print(f"Error saving tasks: {e}\n")


# ~~~~~~~~~~~~~~~ Add New Task ~~~~~~~~~~~~~~~~~~~~~~~~~~


def add_task():
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty!\n")
        return
    if title in task_titles:
        print("This task already exists!\n")
        return

    date_input = input("Enter due date (YYYY-MM-DD): ").strip()
    if not date_input:
        print("Date cannot be empty!\n")
        return
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError as e:
        print(f"Invalid date! Use format YYYY-MM-DD. Error: {e}\n")
        return

    task = (title, "pending", date_input)
    tasks.append(task)
    task_titles.add(title)
    save_tasks()
    print("Task added and saved!\n")




# ~~~~~~~~~~~~~~~~~~~~ View Tasks ~~~~~~~~~~~~~~~~~~~~


def view_tasks():
    if not tasks:
        print("No tasks to show.\n")
        return
    print("\n--- Task List ---")
    for i, task in enumerate(tasks, 1):
        status_text = "Done" if task[1] == "done" else "Pending"
        print(f"{i}. {task[0]} (Due: {task[2]}) - Status: {status_text}")
    print()


# ~~~~~~~~~~~~~~~~~~ Mark Task Completed ~~~~~~~~~~~~~


def mark_completed():
    view_tasks()
    if not tasks:
        return
    choice = input("Enter task number to mark as completed: ").strip()
    if not choice:
        print("You must enter a task number!\n")
        return
    try:
        num = int(choice)
        if 1 <= num <= len(tasks):
            title, _, date = tasks[num - 1]
            tasks[num - 1] = (title, "done", date)
            save_tasks()
            print("Task marked as done and saved!\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")


# ~~~~~~~~~~~~~~~~~~ Delete Task ~~~~~~~~~~~~~~~~~~~


def delete_task():
    view_tasks()
    if not tasks:
        return
    choice = input("Enter task number to delete: ").strip()
    if not choice:
        print("You must enter a task number!\n")
        return
    try:
        num = int(choice)
        if 1 <= num <= len(tasks):
            removed_task = tasks.pop(num - 1)
            task_titles.remove(removed_task[0])
            save_tasks()
            print(f"Deleted task: {removed_task[0]} and saved!\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")


# ~~~~~~~~~~~~~~~~~ Edit Task ~~~~~~~~~~~~~~~~~~~


def edit_task():
    view_tasks()
    if not tasks:
        return
    choice = input("Enter task number to edit: ").strip()
    if not choice:
        print("You must enter a task number!\n")
        return
    try:
        num = int(choice)
        if 1 <= num <= len(tasks):
            old_title, status, old_date = tasks[num - 1]

            new_title = input(f"Enter new title (leave blank to keep '{old_title}'): ").strip()
            if new_title and new_title != old_title:
                if new_title in task_titles:
                    print("This title already exists!\n")
                    return
                task_titles.remove(old_title)
                task_titles.add(new_title)
            else:
                new_title = old_title

            new_date = input(f"Enter new due date (YYYY-MM-DD) (leave blank to keep '{old_date}'): ").strip()
            if new_date:
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format! Use YYYY-MM-DD.\n")
                    return
            else:
                new_date = old_date

            tasks[num - 1] = (new_title, status, new_date)
            save_tasks()
            print("Task updated and saved!\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")


# ~~~~~~~~~~~~~~~~~ Reset/Delete File ~~~~~~~~~~~~~~~~~


def reset_tasks_file():
    confirm = input("Are you sure you want to delete all saved tasks and create a new file? (yes/no): ").strip().lower()
    if confirm == "yes":
        try:
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
                print("Task file deleted.")

            tasks.clear()
            task_titles.clear()

            with open(FILENAME, "w") as file:
                file.write("# New task file created\n")  

            print("New task file created and task list reset!\n")
        except Exception as e:
            print(f"Error resetting task file: {e}\n")
    else:
        print("Operation cancelled.\n")


# ~~~~~~~~~~~~~~~~~~~~ Main Menu ~~~~~~~~~~~~~~~~~~~~


def menu():
    while True:
        print("===== My To-Do List =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Reset Task File")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()

        if not choice:
            print("You must choose a number between 1 and 7!\n")
        elif choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            reset_tasks_file()
        elif choice == "7":
            print("Tasks saved! See you next time!")
            break
        else:
            print("Invalid choice. Please try again.\n")


# ~~~~~~~~~~~~~~~~~~~ Run the Program ~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    load_tasks()
    menu()
