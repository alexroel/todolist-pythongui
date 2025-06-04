import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from database.crud_category import get_all_categories, create_category, delete_category, update_category
from models.category import Category

class CategoryPanel(ctk.CTkFrame):
    def __init__(self, master, on_category_selected=None):
        super().__init__(master)
        self.on_category_selected = on_category_selected
        self.selected_category = None
        self.active_category_btn = None
        self.category_buttons = []

        # Switch de modo claro/oscuro (opcional, puedes quitar si lo tienes en app_ui)
        self.mode_var = ctk.StringVar(value="light")
        self.mode_switch = ctk.CTkSwitch(
            self,
            text="Modo oscuro",
            variable=self.mode_var,
            onvalue="dark",
            offvalue="light",
            command=self.toggle_mode
        )
        self.mode_switch.pack(fill="x", padx=10, pady=10)

        # Frame para agregar nueva categoría
        self.add_category_frame = ctk.CTkFrame(self)
        self.add_category_frame.pack(fill="x", padx=5, pady=5)
        self.add_category_entry = ctk.CTkEntry(self.add_category_frame, placeholder_text="Nueva Lista...")
        self.add_category_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.add_category_btn = ctk.CTkButton(self.add_category_frame, text="Agregar", command=self.add_category)
        self.add_category_btn.pack(side="left", padx=5, pady=5)

        # Frame para la lista de categorías
        self.category_list_frame = ctk.CTkFrame(self)
        self.category_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_categories()

    def toggle_mode(self):
        ctk.set_appearance_mode(self.mode_var.get())

    def load_categories(self):
        # Limpiar botones anteriores
        for btn in self.category_buttons:
            btn.destroy()
        self.category_buttons.clear()

        categories = get_all_categories()
        for idx, category in enumerate(categories):
            btn = ctk.CTkButton(
                self.category_list_frame,
                text=category.name,
                font=("Arial", 14),
                anchor="w",
                command=lambda c=category, b=idx: self.select_category(c, b)
                             
            )
            btn.pack(fill="x", pady=(10, 0), padx=10)
            btn.bind("<Button-3>", lambda event, c=category, b=idx: self.show_category_menu(event, c, b))
            self.category_buttons.append(btn)

    def select_category(self, category: Category, btn_index: int):
        self.selected_category = category

        # Resaltar el botón activo
        if self.active_category_btn is not None:
            self.category_buttons[self.active_category_btn].configure(fg_color="#3498db")
        self.category_buttons[btn_index].configure(fg_color="#05578e")
        self.active_category_btn = btn_index

        # Llamar callback si existe
        if self.on_category_selected:
            self.on_category_selected(category, btn_index)

    def show_category_menu(self, event, category: Category, btn_index: int):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar", command=lambda: self.edit_category_dialog(category, btn_index))
        menu.add_command(label="Eliminar", command=lambda: self.delete_category_confirm(category, btn_index))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def edit_category_dialog(self, category: Category, btn_index: int):
        dialog = ctk.CTkInputDialog(text="Nuevo nombre:", title="Editar categoría")
        new_name = dialog.get_input()
        if new_name and new_name.strip():
            if update_category(Category(category.id, new_name.strip())):
                self.load_categories()
                # Mantener resaltado el botón editado si era el activo
                if self.active_category_btn == btn_index:
                    self.select_category(Category(category.id, new_name.strip()), btn_index)
            else:
                messagebox.showerror("Error", "No se pudo actualizar la categoría.")

    def delete_category_confirm(self, category: Category, btn_index: int):
        if messagebox.askyesno("Eliminar", f"¿Eliminar la categoría '{category.name}'?"):
            if delete_category(category.id):
                self.load_categories()
                # Si la categoría eliminada era la activa, limpiar selección
                if self.active_category_btn == btn_index:
                    self.selected_category = None
                    self.active_category_btn = None
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría.")

    def add_category(self):
        name = self.add_category_entry.get().strip()
        if name:
            create_category(Category(id=None, name=name))
            self.add_category_entry.delete(0, "end")
            self.load_categories()