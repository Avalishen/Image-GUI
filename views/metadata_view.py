import customtkinter as ctk
import os

from PIL import Image
from placeholders import placeholder_text_3
from utils import resource_path
from tkinter import filedialog
from core.metadata_finder import get_all_metadata, remove_metadata

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
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 450, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 65)
        self.result_textbox.insert("0.0", "Результат поиска появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала поиска и извлечения метаданных"""
        self.search_btn = ctk.CTkButton(self, text = "Извлечь Метаданные", corner_radius = 10,
                                       command = self.extract_all_metadata)
        self.search_btn.place(x = 20, y = 530)

        self.remove_metadata_btn = ctk.CTkButton(self, text = "Удалить Метаданные", corner_radius = 10,
                                       command = self.remove_all_metadata)
        self.remove_metadata_btn.place(x = 190, y = 530)


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

    def extract_all_metadata(self):
        """Извлекает геоданные из выбранного файла"""
        file_path = self.source_entry.get()

        if not file_path:
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "❌ Выберите файл!")
            self.result_textbox.configure(state="disabled")
            return

        result = get_all_metadata(file_path)

        if result.get("success"):
            text = "Метаданные изображения:\n\n"

            if "latitude" in result and "longitude" in result:
                text += f"Координаты:\n"
                text += f"  • Широта: {result['latitude']:.6f}° ({result['latitude_dms']})\n"
                text += f"  • Долгота: {result['longitude']:.6f}° ({result['longitude_dms']})\n\n"

            if "altitude" in result:
                text += f"  • Высота: {result['altitude']:.2f} м над уровнем моря\n"

            if "date" in result or "time" in result:
                text += f"\nДата и время съёмки:\n"
                if "date" in result:
                    text += f"  • Дата: {result['date']}\n"
                if "time" in result:
                    text += f"  • Время: {result['time']}\n"

            if "camera" in result:
                text += f"\nКамера:\n"
                text += f"  • Производитель: {result['camera'].get('make', 'Неизвестно')}\n"
                text += f"  • Модель: {result['camera'].get('model', 'Неизвестно')}\n"
                text += f"  • Программное обеспечение: {result['camera'].get('software', 'Неизвестно')}\n"

            if "shooting" in result:
                text += f"\nНастройки съёмки:\n"
                text += f"  • Диафрагма: {result['shooting'].get('aperture', 'Неизвестно')}\n"
                text += f"  • Выдержка: {result['shooting'].get('exposure', 'Неизвестно')}\n"
                text += f"  • ISO: {result['shooting'].get('iso', 'Неизвестно')}\n"
                text += f"  • Фокусное расстояние: {result['shooting'].get('focal_length', 'Неизвестно')}\n"
                text += f"  • Вспышка: {result['shooting'].get('flash', 'Неизвестно')}\n"

            if "datetime" in result:
                text += f"\nДата и время:\n"
                text += f"  • {result['datetime']}\n"

            if "other" in result:
                text += f"\nДополнительная информация:\n"
                text += f"  • Ориентация: {result['other'].get('orientation', 'Неизвестно')}\n"
                text += f"  • Цветовой профиль: {result['other'].get('color_space', 'Неизвестно')}\n"
                text += f"  • Авторское право: {result['other'].get('copyright', 'Неизвестно')}\n"
                text += f"  • Автор: {result['other'].get('artist', 'Неизвестно')}\n"
        else:
            text = f"❌ {result.get('message', result.get('error', 'Неизвестная ошибка'))}"

        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state="disabled")

    def remove_all_metadata(self):
        file_path = self.source_entry.get()

        if not file_path:
            text = "Выберите файл!"
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", text)
            self.result_textbox.configure(state="disabled")
            return

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)

        output_path = os.path.join(file_dir, f"{name}_cleaned{ext}")

        result = remove_metadata(file_path, output_path)

        if result.get("success"):
            text = f"Метаданные успешно удалены!\nСохранено в: {output_path}"
        else:
            text = f"Ошибка: {result.get('error', 'Неизвестная ошибка')}"

        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state="disabled")

