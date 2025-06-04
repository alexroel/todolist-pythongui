import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from database.crud_task import get_tasks_by_category, create_task, update_task_completed, delete_task
from models.task import Task

class TaskPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_category = None
        self.task_checkboxes = []

        # Entrada para nueva tarea
        self.new_task_entry = ctk.CTkEntry(self, placeholder_text="Nueva tarea...")
        self.new_task_entry.pack(fill="x", pady=(10, 0), padx=10)
        self.add_task_btn = ctk.CTkButton(self, text="Agregar tarea", command=self.add_task)
        self.add_task_btn.pack(fill="x", pady=(3, 10), padx=10)

        # Frame para la lista de tareas
        self.task_list_frame = ctk.CTkFrame(self)
        self.task_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def load_tasks(self, category, btn_index=None):
        self.selected_category = category

        # Limpiar checkboxes anteriores
        for cb in self.task_checkboxes:
            cb.destroy()
        self.task_checkboxes.clear()

        tasks = get_tasks_by_category(category.id)
        for task in tasks:
            var = ctk.BooleanVar(value=task.completed)
            cb = ctk.CTkCheckBox(
                self.task_list_frame,
                text=task.title,
                variable=var,
                command=lambda t=task, v=var: self.toggle_task_completed(t, v)
            )
            cb.pack(anchor="w", pady=(10, 0), padx=10)
            cb.bind("<Button-3>", lambda event, t=task: self.show_task_menu(event, t))
            # Tachado si está completada
            if task.completed:
                cb.configure(font=("Arial", 14, "overstrike"))
                cb.select()
            else:
                cb.configure(font=("Arial", 14, "normal"))
            self.task_checkboxes.append(cb)

    def toggle_task_completed(self, task: Task, var):
        completed = var.get()
        update_task_completed(task.id, completed)
        # Refrescar la lista de tareas
        if self.selected_category:
            self.load_tasks(self.selected_category)

    def add_task(self):
        title = self.new_task_entry.get().strip()
        if self.selected_category and title:
            create_task(title, self.selected_category.id)
            self.new_task_entry.delete(0, "end")
            self.load_tasks(self.selected_category)

    def show_task_menu(self, event, task: Task):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Eliminar", command=lambda: self.delete_task_confirm(task))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def delete_task_confirm(self, task: Task):
        if messagebox.askyesno("Eliminar", f"¿Eliminar la tarea '{task.title}'?"):
            if delete_task(task.id):
                if self.selected_category:
                    self.load_tasks(self.selected_category)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea.")