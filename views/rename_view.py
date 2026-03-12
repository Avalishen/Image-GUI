import customtkinter as ctk

from tkinter import filedialog
from PIL import Image
from placeholders import placeholder_text_3, placeholder_text_4
from core.rename_finder import rename_files_in_folder, rename_files_with_hash
from utils import resource_path

rename_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

class RenameView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 575, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_3, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Поле для ввода названия"""
        self.rename_entry_name = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_4, corner_radius = 10)
        self.rename_entry_name.place(x = 20, y = 60)
        self.rename_entry_name.configure(state = "disabled")

        """Кнопка Обзор открывает меню для выбра папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = rename_image, corner_radius = 10,
                                               fg_color="transparent", hover_color="gray", command = self.choose_source, width = 80)
        self.browse_source_btn.place(x = 270, y = 20)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 375, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 140)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для переименования файлов"""
        self.search_btn = ctk.CTkButton(self, text = "Переименовать", command = self.on_rename_click, corner_radius = 10)
        self.search_btn.place(x = 20, y = 530)

        """Чекбокс для отметок выбора"""
        self.custom_var = ctk.BooleanVar(value = False)
        self.custom_rename = ctk.CTkCheckBox(self, text = "Своё Название", variable = self.custom_var, command = self.on_custom_checkbox, width = 240)
        self.custom_rename.place(x = 20, y = 100)

        self.hash_var = ctk.BooleanVar(value = False)
        self.hash_rename = ctk.CTkCheckBox(self, text = "Хэш Название", variable = self.hash_var, command = self.on_hash_rename, width = 240)
        self.hash_rename.place(x = 160, y = 100)

    def choose_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, folder)

    def on_custom_checkbox(self):
        """Обработчик чекбокса 'Своё Название' """
        if self.custom_var.get():
            self.hash_var.set(False)
            self.rename_entry_name.configure(state = "normal")
            self.rename_entry_name.focus()
        else:
            self.rename_entry_name.configure(state = "disabled")

    def on_hash_rename(self):
        """Обработчик чекбокса 'Хэш Название' """
        if self.hash_var.get():
            self.custom_var.set(False)
            self.rename_entry_name.configure(state = "disabled")

    def display_result(self, result):
        """Отображает результат в текстовом поле"""
        text = "Результат переименования:\n\n"
        for old_name, new_name in result.items():
            text += f"• {old_name} → {new_name}\n"

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state = "disabled")

    def show_error(self, message):
        """Показывает ошибку в текстовом поле"""
        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", f"Ошибка: {message}")
        self.result_textbox.configure(state = "disabled")

    def on_rename_click(self):
        """Обрабатывает нажатие кнопки переименования"""
        folder = self.source_entry.get()

        if not folder:
            self.show_error("Выберите папку!")
            return

        if self.custom_var.get():
            template = self.rename_entry_name.get()
            if not template:
                self.show_error("Введите название!")
                return

            try:
                result = rename_files_in_folder(folder, template)
                self.display_result(result)
            except Exception as e:
                self.show_error(str(e))

        elif self.hash_var.get():
            prefix = self.rename_entry_name.get()
            try:
                result = rename_files_with_hash(folder, prefix)
                self.display_result(result)
            except Exception as e:
                self.show_error(str(e))

        else:
            self.show_error("Выберите режим переименования!")