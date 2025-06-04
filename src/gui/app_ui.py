import customtkinter as ctk
from gui.category_panel import CategoryPanel
from gui.task_panel import TaskPanel

class TodoListApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ToDo List - Python GUI")
        self.geometry("750x450")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")

        # Layout principal
        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Panel de categorías (izquierda)
        self.category_panel = CategoryPanel(self, on_category_selected=self.on_category_selected)
        self.category_panel.grid(row=0, column=0, sticky="nswe", padx=5, pady=10)

        # Panel de tareas (derecha)
        self.task_panel = TaskPanel(self)
        self.task_panel.grid(row=0, column=1, sticky="nswe", padx=5, pady=10)

    def on_category_selected(self, category, btn_index=None):
        self.task_panel.load_tasks(category)





