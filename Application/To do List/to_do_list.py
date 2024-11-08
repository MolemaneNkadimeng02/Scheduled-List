import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Application")
        self.master.geometry("400x400")

        self.tasks = []

        # Initialize the Listbox first
        self.task_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        # Then load tasks
        self.load_tasks()

        # Initialize the buttons
        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.update_button = tk.Button(master, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.complete_button = tk.Button(master, text="Mark as Complete", command=self.mark_completed)
        self.complete_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.populate_task_list()

    def populate_task_list(self):
        """Populate the Listbox with tasks, sorted by urgency."""
        self.task_listbox.delete(0, tk.END)
        # Sort tasks: urgent first, then non-urgent
        sorted_tasks = sorted(self.tasks, key=lambda x: (not x['urgent'], x['title']))
        for task in sorted_tasks:
            status = ' (Completed)' if task['completed'] else ''
            urgency = ' [Urgent]' if task['urgent'] else ''
            self.task_listbox.insert(tk.END, task['title'] + urgency + status)

    def add_task(self):
        """Add a new task with urgency option."""
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if title:
            urgent = messagebox.askyesno("Task Urgency", "Is this task urgent?")
            self.tasks.append({"title": title, "completed": False, "urgent": urgent})
            self.populate_task_list()

    def update_task(self):
        """Update the selected task."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            new_title = simpledialog.askstring("Update Task", "Enter new task title:", initialvalue=selected_task['title'])
            if new_title:
                urgent = messagebox.askyesno("Task Urgency", "Is this task urgent?", default=selected_task['urgent'])
                selected_task['title'] = new_title
                selected_task['urgent'] = urgent
                self.populate_task_list()
        else:
            messagebox.showwarning("Update Task", "Please select a task to update.")

    def delete_task(self):
        """Delete the selected task."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.populate_task_list()
        else:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")

    def mark_completed(self):
        """Mark the selected task as completed."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]['completed'] = True
            self.populate_task_list()
        else:
            messagebox.showwarning("Complete Task", "Please select a task to mark as complete.")

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Save Tasks", "Tasks saved successfully.")

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Load Tasks", "The task file is corrupted or empty. Starting with an empty task list.")
                self.tasks = []
        else:
            self.tasks = []
        self.populate_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()