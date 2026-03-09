import customtkinter as ctk

from PIL import Image
from placeholders import placeholder_text_3, placeholder_text_4
from utils import resource_path
from tkinter import filedialog
from core.metadata_finder import get_gps_data

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

        """Кнопка Обзор открывает меню для выбора папки"""
        self.browse_source_btn = ctk.CTkButton(self, text = "Обзор...", image = metadata_image, corner_radius = 10,
                                               fg_color = "transparent", hover_color = "gray", command = self.choose_files ,width = 80)
        self.browse_source_btn.place(x = 270, y = 20)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 300)
        self.result_textbox.place(x = 20, y = 100)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала поиска дубликатов"""
        self.search_btn = ctk.CTkButton(self, text = "Извлечь Метаданные", corner_radius = 10,
                                       command = self.extract_gps)
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

    def display_result(self, result):
        """Отображает результат в текстовом поле"""
        text = "Результат переименования:\n\n"
        for old_name, new_name in result.items():
            text += f"• {old_name} → {new_name}\n"

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state = "disabled")

    def extract_gps(self):
        """Извлекает геоданные из выбранного файла"""
        file_path = self.source_entry.get()

        if not file_path:
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "❌ Выберите файл!")
            self.result_textbox.configure(state="disabled")
            return

        result = get_gps_data(file_path)

        if result.get("success"):
            text = "Геоданные изображения:\n\n"
            if "latitude" in result and "longitude" in result:
                text += f"Координаты:\n"
                text += f"  Широта: {result['latitude']:.6f}° ({result['latitude_dms']})\n"
                text += f"  Долгота: {result['longitude']:.6f}° ({result['longitude_dms']})\n\n"

                if "altitude" in result:
                    text += f"Высота: {result['altitude']:.2f} м над уровнем моря\n\n"

                if "date" in result or "time" in result:
                    text += f"Дата и время съёмки:\n"
                    if "date" in result:
                        text += f"  Дата: {result['date']}\n"
                    if "time" in result:
                        text += f"  Время: {result['time']}\n"
            else:
                text = f"❌ {result.get('message', result.get('error', 'Неизвестная ошибка'))}"


        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state="disabled")
