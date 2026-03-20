import customtkinter as ctk
import os

from PIL import Image
from placeholders import placeholder_text_3
from utils import resource_path
from tkinter import filedialog
from core.convert_finder import convert_png_to_jpg

convert_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

formats_in = ["jpg", "png", "gif", "bmp",]

class ConvertView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 575, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_3, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Кнопка Обзор открывает меню для выбора папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = convert_image, corner_radius = 10,
                                               fg_color = "transparent", hover_color = "gray", width = 80, command = self.choose_files)
        self.browse_source_btn.place(x = 270, y = 20)

        self.combobox_from_format = ctk.CTkComboBox(self, values = formats_in, width = 240, corner_radius = 10, state = "readonly")
        self.combobox_from_format.set("Выберите исходный формат")
        self.combobox_from_format.place(x = 20, y = 60)

        self.combobox_to_format = ctk.CTkComboBox(self, values = formats_in, width = 240, corner_radius = 10, state = "readonly")
        self.combobox_to_format.set("Выберите целевой формат")
        self.combobox_to_format.place(x = 20, y = 100)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 250, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 165)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала конвертации"""
        self.search_btn = ctk.CTkButton(self, text = "Конвертировать файл", corner_radius = 10, command = self.convert)
        self.search_btn.place(x = 20, y = 530)


    def choose_files(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.jfif"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, file_path)

    def display_result(self, result):
        """Отображает результат в текстовом поле"""
        text = "Результат переименования:\n\n"
        for old_name, new_name in result.items():
            text += f"• {old_name} → {new_name}\n"

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state = "disabled")

    def convert(self):

        file_path = self.source_entry.get()
        if not file_path:
            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "Выберите файл!")
            self.result_textbox.configure(state = "disabled")
            return

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)

        output_path = os.path.join(file_dir, f"{name}.jpg")
        result = convert_png_to_jpg(file_path, output_path, quality = 90)
        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")

        if result.get("success"):
            output_text = "Конвертация Успешна!\n"
            output_text += f"Файл сохранен: {result['output_path']}\n"
            output_text += f"Размер: {result['new_size'] / 1024:.2f} КБ\n"
            self.result_textbox.insert("0.0", output_text)
        else:
            self.result_textbox.insert("0.0", f"Ошибка: {result.get('error', 'Неизвестная ошибка')}")

        self.result_textbox.configure(state = "disabled")

