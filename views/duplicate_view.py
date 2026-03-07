import customtkinter as ctk
import os

from tkinter import filedialog
from PIL import Image
from placeholders import placeholder_text_1, placeholder_text_2
from core.duplicate_finder import find_image_duplicates

duplicate_image = ctk.CTkImage(
    light_image = Image.open("images/folder-dark.png"),
    dark_image = Image.open("images/folder-light.png"),
    size = (24, 20)
)

class DuplicateView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 575, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        self.duplicate_results = None

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_1, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Поле для ввода пути к папке с дубликатами фото (Создается автоматически)"""
        self.dest_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_2, corner_radius = 10)
        self.dest_entry.place(x = 20, y = 60)

        """Кнопка Обзор открывает меню для выбра папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = duplicate_image, corner_radius = 10,
                                               fg_color="transparent", hover_color="gray", command = self.choose_source, width = 80)
        self.browse_source_btn.place(x = 270, y = 20)

        """Кнопка Обзор открывает меню для выбра папки для дубликатво (Если такая папка уже есть)"""
        self.browse_dest_btn = ctk.CTkButton(self, text = "Обзор...", image = duplicate_image, corner_radius = 10,
                                             fg_color="transparent", hover_color="gray", command = self.choose_dest, width = 80)
        self.browse_dest_btn.place(x = 270, y = 60)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 300)
        self.result_textbox.place(x = 20, y = 100)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled") # только для чтения

        """Кнопка для начала поиска дубликатов"""
        self.search_btn = ctk.CTkButton(self, text = "Найти дубликаты", corner_radius = 10, command = self.on_duplicate_search)
        self.search_btn.place(x=20, y=420)

        """Кнопка для перемещения дубликатов"""
        self.move_btn = ctk.CTkButton(self, text = "Переместить дубликаты", corner_radius = 10, command = self.on_duplicate_move, state="disabled")
        self.move_btn.place(x=180, y=420)

    def choose_source(self):
        folder = filedialog.askdirectory(title = "Папка с фото")
        if folder:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, folder)
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, os.path.join(folder, "Дубликаты"))


    def choose_dest(self):
        folder = filedialog.askdirectory(title = "Папка для дубликатов")
        if folder:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, folder)

    def on_duplicate_search(self):
        """Вызывается при нажатии 'Найти дубликаты'"""
        source_folder = self.source_entry.get()
        if not source_folder:
            return

        try:
            self.duplicate_results = find_image_duplicates(source_folder)
            text = self.format_duplicates(self.duplicate_results)

            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", text)
            self.result_textbox.configure(state = "disabled")

            self.move_btn.configure(state="normal")

        except Exception as e:
            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"Ошибка: {e}")
            self.result_textbox.configure(state = "disabled")

    def format_duplicates(self, duplicate_groups: dict) -> str:
        """Превращает {хеш: [файлы]} в читаемый текст"""
        if not duplicate_groups:
            return "Дубликаты не найдены."

        lines = [f"Найдено {len(duplicate_groups)} групп(а) дубликатов:\n"]
        for i, (hash_val, files) in enumerate(duplicate_groups.items(), 1):
            lines.append(f"Группа {i}:")
            for f in files:
                lines.append(f"  • {os.path.basename(f)}")
            lines.append("")
        return "\n".join(lines)

    def on_duplicate_move(self):
        """Вызывается при нажатии 'Переместить'"""
        if not self.duplicate_results:
            return

        dest_folder = self.dest_entry.get()
        if not dest_folder:
            return

        from core.duplicate_finder import move_duplicates_to_folder
        try:
            os.makedirs(dest_folder, exist_ok=True)
            moved = move_duplicates_to_folder(self.duplicate_results, dest_folder)

            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"Перемещено {moved} файлов в:\n{dest_folder}")
            self.result_textbox.configure(state="disabled")

            self.duplicate_results = None
            self.move_btn.configure(state="disabled")

        except Exception as e:
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"Ошибка: {e}")
            self.result_textbox.configure(state="disabled")