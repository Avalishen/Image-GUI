import customtkinter as ctk
import os

from PIL import Image
from placeholders import placeholder_text_3
from utils import resource_path
from tkinter import filedialog
from core.metadata_finder import get_all_metadata, remove_metadata

quality_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

class QualityView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 575, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_3, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Кнопка Обзор открывает меню для выбора папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = quality_image, corner_radius = 10,
                                               fg_color = "transparent", hover_color = "gray", width = 80)
        self.browse_source_btn.place(x = 270, y = 20)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 250, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 165)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала конвертации"""
        self.search_btn = ctk.CTkButton(self, text = "Конвертировать файл", corner_radius = 10)
        self.search_btn.place(x = 20, y = 530)