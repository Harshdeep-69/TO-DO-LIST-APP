import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FILE_NAME = "tasks.txt"

tasks = []
search_query = ""

# Save
def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for t in tasks:
            pin_flag = "1" if t["pinned"] else "0"
            f.write(f"{pin_flag}|{t['text']}\n")

# Load
def load_tasks():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            for line in f:
                pin, text = line.strip().split("|", 1)
                tasks.append({"text": text, "pinned": pin == "1"})
    except:
        pass
    render_tasks()

# Add task
def add_task():
    text = entry.get()
    if text:
        time = datetime.now().strftime("%H:%M")
        tasks.append({"text": f"[{time}] {text}", "pinned": False})
        entry.delete(0, "end")
        save_tasks()
        render_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task!")

# Delete
def delete_task(i):
    tasks.pop(i)
    save_tasks()
    render_tasks()

# Mark done
def mark_done(i):
    if not tasks[i]["text"].startswith("✔"):
        tasks[i]["text"] = "✔ " + tasks[i]["text"]
        save_tasks()
        render_tasks()

# Pin / Unpin
def toggle_pin(i):
    tasks[i]["pinned"] = not tasks[i]["pinned"]
    save_tasks()
    render_tasks()

# Edit
def edit_task(i):
    entry.delete(0, "end")
    entry.insert(0, tasks[i]["text"])
    tasks.pop(i)
    save_tasks()
    render_tasks()

# 🔍 SEARCH FUNCTION
def search_tasks():
    global search_query
    search_query = search_entry.get().lower()
    render_tasks()

# Render cards
def render_tasks():
    for w in task_frame.winfo_children():
        w.destroy()

    # Apply search filter
    if search_query:
        display_tasks = [
            t for t in tasks
            if search_query in t["text"].lower()
        ]
    else:
        display_tasks = tasks

    # pinned first
    sorted_tasks = sorted(display_tasks, key=lambda x: not x["pinned"])

    for i, task in enumerate(sorted_tasks):
        card = ctk.CTkFrame(
            task_frame,
            corner_radius=15,
            fg_color=("#fff3b0" if task["pinned"] else "#2b2b2b")
        )
        card.grid(row=i//2, column=i%2, padx=10, pady=10)

        label = ctk.CTkLabel(card, text=task["text"], wraplength=150, justify="left")
        label.pack(padx=10, pady=10)

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=5)

        pin_btn = ctk.CTkButton(btn_frame, text="📌", width=35,
                                command=lambda i=i: toggle_pin(i))
        pin_btn.grid(row=0, column=0, padx=3)

        done_btn = ctk.CTkButton(btn_frame, text="✔", width=35,
                                 command=lambda i=i: mark_done(i))
        done_btn.grid(row=0, column=1, padx=3)

        edit_btn = ctk.CTkButton(btn_frame, text="✏️", width=35,
                                command=lambda i=i: edit_task(i))
        edit_btn.grid(row=0, column=2, padx=3)

        del_btn = ctk.CTkButton(btn_frame, text="🗑", width=35,
                               command=lambda i=i: delete_task(i))
        del_btn.grid(row=0, column=3, padx=3)

# ================= UI =================
app = ctk.CTk()
app.geometry("420x700")
app.title("TO DO NOTES")

title = ctk.CTkLabel(app, text="📝 My Notes", font=("Arial", 26, "bold"))
title.pack(pady=10)

# ===== INPUT BAR =====
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=10)

entry = ctk.CTkEntry(input_frame, placeholder_text="Take a note...", width=260, height=40)
entry.grid(row=0, column=0, padx=5)

add_btn = ctk.CTkButton(input_frame, text="+", width=50, height=40, corner_radius=12, command=add_task)
add_btn.grid(row=0, column=1)

# ===== SEARCH BAR (NEW ADDED FEATURE) =====
search_frame = ctk.CTkFrame(app, fg_color="transparent")
search_frame.pack(pady=5)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search notes...", width=200, height=35)
search_entry.grid(row=0, column=0, padx=5)

search_btn = ctk.CTkButton(search_frame, text="🔍", width=50, height=35, command=search_tasks)
search_btn.grid(row=0, column=1)

# ===== TASK AREA =====
task_frame = ctk.CTkScrollableFrame(app, width=380, height=500)
task_frame.pack(pady=10)

load_tasks()

app.mainloop()
