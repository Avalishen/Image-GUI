import customtkinter as ctk

from PIL import Image
from placeholders import placeholder_text_3, placeholder_text_4
from utils import resource_path
from tkinter import filedialog

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
                                               fg_color = "transparent", hover_color = "gray", command = self.choose_files ,width = 80)
        self.browse_source_btn.place(x = 270, y = 20)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 300)
        self.result_textbox.place(x = 20, y = 100)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала поиска дубликатов"""
        self.search_btn = ctk.CTkButton(self, text = "Извлеч Метаданные", corner_radius = 10,
                                       )
        self.search_btn.place(x = 20, y = 420)


    def choose_files(self):
        file_path = filedialog.askopenfilename(
            title = "Выберите изображение",
            filetypes = [
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.jfif"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, file_path)

