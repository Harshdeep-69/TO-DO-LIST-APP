import tkinter as tk
from tkinter import messagebox

# File to store tasks
FILE_NAME = "tasks.txt"

# Load tasks from file
def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                task_listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass
 
# Save tasks to file
def save_tasks():
    with open(FILE_NAME, "w") as f:
        tasks = task_listbox.get(0, tk.END)
        for task in tasks:
            f.write(task + "\n")

# Add task
def add_task():
    task = entry.get()
    if task != "":
        task_listbox.insert(tk.END, task)
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

# Mark as done
def mark_done():
    try:
        selected = task_listbox.curselection()[0]
        task = task_listbox.get(selected)
        task_listbox.delete(selected)
        task_listbox.insert(selected, "✔ " + task)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task!")

# Main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x450")

# Entry box
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=10)

# Buttons
btn_add = tk.Button(root, text="Add Task", width=20, command=add_task)
btn_add.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Task", width=20, command=delete_task)
btn_delete.pack(pady=5)

btn_done = tk.Button(root, text="Mark as Done", width=20, command=mark_done)
btn_done.pack(pady=5)

# Task list
task_listbox = tk.Listbox(root, width=40, height=15)
task_listbox.pack(pady=10)

# Load saved tasks
load_tasks()

# Run app
root.mainloop()