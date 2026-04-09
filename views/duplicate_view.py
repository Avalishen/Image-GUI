import time

import customtkinter as ctk
import os

from tkinter import filedialog
from PIL import Image
from placeholders import placeholder_text_1, placeholder_text_2
from core.duplicate_core import find_image_duplicates, move_duplicates_to_folder
from folder_utils.info_dialog import show_info_dialog
from utils import resource_path
from folder_utils.progress_dialog import show_progress_dialog, create_progress_window, hide_progress_dialog

duplicate_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

info_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/info-dark.png")),
    dark_image = Image.open(resource_path("images/info-light.png")),
    size = (20, 20)
)

class DuplicateView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 588, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        self.duplicate_results = None

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_1, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Поле для ввода пути к папке с дубликатами фото (Создается автоматически)"""
        self.dest_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_2, corner_radius = 10)
        self.dest_entry.place(x = 20, y = 60)

        """Кнопка Обзор открывает меню для выбора папки"""
        self.review_btn = ctk.CTkButton(self, text = "Обзор...", image = duplicate_image, corner_radius = 10,
                                               fg_color="transparent", hover_color="gray", command = self.choose_source, width = 80)
        self.review_btn.place(x = 270, y = 20)

        """Кнопка Обзор открывает меню для выбора папки для дубликатов (Если такая папка уже есть)"""
        self.review_duplicate_btn = ctk.CTkButton(self, text = "Обзор...", image = duplicate_image, corner_radius = 10,
                                             fg_color="transparent", hover_color="gray", command = self.choose_dest, width = 80)
        self.review_duplicate_btn.place(x = 270, y = 60)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 415, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 100)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled") # только для чтения

        """Кнопка для начала поиска дубликатов"""
        self.search_btn = ctk.CTkButton(self, text = "Найти дубликаты", corner_radius = 10, command = self.on_duplicate_search)
        self.search_btn.place(x = 20, y = 530)

        """Кнопка для перемещения дубликатов"""
        self.move_btn = ctk.CTkButton(self, text = "Переместить дубликаты", corner_radius = 10, command = self.on_duplicate_move, state = "disabled")
        self.move_btn.place(x = 180, y = 530)

        """Кнопка Информации"""
        self.info_btn = ctk.CTkButton(self, text = "INFO", image = info_image, corner_radius = 10,
                                      fg_color = "transparent", hover_color = "gray", width = 80, command = self.show_info)
        self.info_btn.place(x = 675, y = 530)

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
            self.show_progress(0, "Начинаю поиск дубликатов...")
            self.duplicate_results = find_image_duplicates(source_folder, progress_callback = self.update_progress)
            self.show_progress(100, "Готово!")
            time.sleep(0.5)
            self.hide_progress()

            text = self.format_duplicates(self.duplicate_results)

            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", text)
            self.result_textbox.configure(state = "disabled")

            self.move_btn.configure(state = "normal")

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

        try:
            os.makedirs(dest_folder, exist_ok = True)
            moved = move_duplicates_to_folder(self.duplicate_results, dest_folder)

            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"Перемещено {moved} файлов в:\n{dest_folder}")
            self.result_textbox.configure(state = "disabled")

            self.duplicate_results = None
            self.move_btn.configure(state = "disabled")

        except Exception as e:
            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"Ошибка: {e}")
            self.result_textbox.configure(state = "disabled")

    def show_info(self):
        show_info_dialog(self, "duplicate")

    def update_progress(self, progress, status):
        """Обновляет прогресс-бар"""
        self.show_progress(progress, status)

    def show_progress(self, progress, status):
        show_progress_dialog(self, progress, status)

    def show_result(self, result):
        """Показывает результат"""

        message = result.get("message", str(result))

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", message)
        self.result_textbox.configure(state="disabled")

    def show_error(self, result):
        """Показывает ошибку"""
        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", f"Ошибка: {result['message']}")
        self.result_textbox.configure(state = "disabled")

    def hide_progress(self):
        """Скрывает прогресс-бар"""
        if hasattr(self, "_progress_window"):
            self._progress_window.destroy()
            delattr(self, "_progress_window")