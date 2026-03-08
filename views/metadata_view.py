from tkinter import filedialog

import customtkinter as ctk

from PIL import Image
from placeholders import placeholder_text_3, placeholder_text_4
from utils import resource_path

metadata_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

class MetadataView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 575, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_3, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Кнопка Обзор открывает меню для выбра папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = metadata_image, corner_radius = 10,
                                               fg_color = "transparent", hover_color = "gray", command = self.choose_source ,width = 80)



    def choose_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, folder)