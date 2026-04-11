import tkinter as tk
from tkinter import messagebox
from datetime import datetime

FILE_NAME = "tasks.txt"

# Load tasks
def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                task_listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass
    update_counter()

# Save tasks
def save_tasks():
    with open(FILE_NAME, "w") as f:
        for task in task_listbox.get(0, tk.END):
            f.write(task + "\n")
    update_counter()

# Add task with timestamp
def add_task():
    task = entry.get()
    if task:
        time = datetime.now().strftime("%H:%M")
        task_listbox.insert(tk.END, f"[{time}] {task}")
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task!")

# Delete task
def delete_task():
    try:
        selected = task_listbox.curselection()[0]
        task_listbox.delete(selected)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task!")

# Mark done
def mark_done():
    try:
        selected = task_listbox.curselection()[0]
        task = task_listbox.get(selected)
        if not task.startswith("✔"):
            task_listbox.delete(selected)
            task_listbox.insert(selected, "✔ " + task)
            save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task!")

# Edit task
def edit_task():
    try:
        selected = task_listbox.curselection()[0]
        old_task = task_listbox.get(selected)
        new_task = entry.get()
        if new_task:
            task_listbox.delete(selected)
            task_listbox.insert(selected, new_task)
            entry.delete(0, tk.END)
            save_tasks()
        else:
            messagebox.showwarning("Warning", "Enter new task!")
    except:
        messagebox.showwarning("Warning", "Select a task!")

# Clear all
def clear_all():
    if messagebox.askyesno("Confirm", "Delete all tasks?"):
        task_listbox.delete(0, tk.END)
        save_tasks()

# Search task
def search_task():
    query = search_entry.get().lower()
    task_listbox.delete(0, tk.END)
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                if query in line.lower():
                    task_listbox.insert(tk.END, line.strip())
    except:
        pass

# Counter
def update_counter():
    count_label.config(text=f"Total Tasks: {task_listbox.size()}")

# Theme toggle
dark_mode = False
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2c2c2c" if dark_mode else "white"
    fg = "white" if dark_mode else "black"

    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass

# Main window
root = tk.Tk()
root.title("Advanced To-Do App")
root.geometry("420x550")

# Entry
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=10)

# Buttons
tk.Button(root, text="Add Task", width=20, command=add_task).pack(pady=3)
tk.Button(root, text="Delete Task", width=20, command=delete_task).pack(pady=3)
tk.Button(root, text="Mark Done", width=20, command=mark_done).pack(pady=3)
tk.Button(root, text="Edit Task", width=20, command=edit_task).pack(pady=3)
tk.Button(root, text="Clear All", width=20, command=clear_all).pack(pady=3)
tk.Button(root, text="Toggle Theme", width=20, command=toggle_theme).pack(pady=3)

# Search bar
search_entry = tk.Entry(root, width=25)
search_entry.pack(pady=5)
tk.Button(root, text="Search", command=search_task).pack()

# Listbox + Scrollbar
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox = tk.Listbox(frame, width=40, height=15, yscrollcommand=scrollbar.set)
task_listbox.pack()

scrollbar.config(command=task_listbox.yview)

# Counter
count_label = tk.Label(root, text="Total Tasks: 0")
count_label.pack()

# Load tasks
load_tasks()

root.mainloop()