import customtkinter as ctk
import os

from PIL import Image
from placeholders import placeholder_text_1
from utils import resource_path
from folder_utils.info_dialog import show_info_dialog
from core.quality_core import advanced_enhance_image
from tkinter import filedialog

quality_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/folder-dark.png")),
    dark_image = Image.open(resource_path("images/folder-light.png")),
    size = (24, 20)
)

info_image = ctk.CTkImage(
    light_image = Image.open(resource_path("images/info-dark.png")),
    dark_image = Image.open(resource_path("images/info-light.png")),
    size = (20, 20)
)

class QualityView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width = 780, height = 588, border_width = 1, corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для ввода пути к папке с фото"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_1, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        """Кнопка Обзор открывает меню для выбора папки"""
        self.review_btn = ctk.CTkButton(self, text = "Обзор...", image = quality_image, corner_radius = 10,
                                               fg_color = "transparent", hover_color = "gray", width = 80, command = self.choose_files)
        self.review_btn.place(x = 270, y = 20)

        """Поле CLAHE Clip Limit"""
        self.label_clahe_clip = ctk.CTkLabel(self, text = "CLAHE Clip Limit:")
        self.label_clahe_clip.place(x = 20, y = 60)

        """Слайдер (CLAHE Clip Limit)"""
        self.slider_clahe_clip = ctk.CTkSlider(self, from_ = 0.1, to = 5.0, width = 200, command = self.update_clahe_clip)
        self.slider_clahe_clip.set(1.5)
        self.slider_clahe_clip.place(x = 130, y = 65)

        """Поле с значением для слайдера (CLAHE Clip Limit)"""
        self.label_percent_clahe_clip = ctk.CTkLabel(self, text = "Clip Limit: 1.5")
        self.label_percent_clahe_clip.place(x = 350, y = 60)

        """Поле CLAHE Tile Size"""
        self.label_clahe_tile_size = ctk.CTkLabel(self, text = "CLAHE Tile Size:")
        self.label_clahe_tile_size.place(x = 20, y = 90)

        """Слайдер (CLAHE Tile Size)"""
        self.slider_clahe_tile_size = ctk.CTkSlider(self, from_ = 4, to = 64, width = 200, command = self.update_clahe_tile_size)
        self.slider_clahe_tile_size.set(16)
        self.slider_clahe_tile_size.place(x = 130, y = 95)

        """Поле с значением для слайдера (CLAHE Tile Size)"""
        self.label_percent_clahe_tile_size = ctk.CTkLabel(self, text = "Tile Size: 16")
        self.label_percent_clahe_tile_size.place(x = 350, y = 90)

        """Поле Шумоподавление"""
        self.label_brightness = ctk.CTkLabel(self, text="Шумоподавление:")
        self.label_brightness.place(x=20, y=120)

        """Слайдер (Шумоподавление)"""
        self.slider_brightness = ctk.CTkSlider(self, from_ = 0, to = 20, width = 200, command = self.update_brightness)
        self.slider_brightness.set(5)
        self.slider_brightness.place(x = 130, y = 125)

        """Поле с значением для слайдера (Шумоподавление)"""
        self.label_percent_brightness = ctk.CTkLabel(self, text = "Шумоподавление: 5")
        self.label_percent_brightness.place(x = 350, y = 120)

        """Поле в котором показывается результат"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 320, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 190)
        self.result_textbox.insert("0.0", "Результат улучшения появится здесь...")
        self.result_textbox.configure(state = "disabled")

        """Кнопка для начала изменения качества"""
        self.quality_btn = ctk.CTkButton(self, text = "Изменить качество", corner_radius = 10, command = self.on_quality_enhance)
        self.quality_btn.place(x = 20, y = 530)

        """Кнопка Информации"""
        self.info_btn = ctk.CTkButton(self, text = "INFO", image = info_image, corner_radius = 10,
                                      fg_color = "transparent", hover_color = "gray", width = 80, command = self.show_info)
        self.info_btn.place(x = 675, y = 530)

    def update_clahe_clip(self, value):
        """Обновляет значение CLAHE Clip Limit"""
        clip_value = float(value)
        self.label_percent_clahe_clip.configure(text = f"Clip Limit: {clip_value:.1f}")

    def update_clahe_tile_size(self, value):
        """Обновляет значение CLAHE Tile Size"""
        tile_value = int(float(value))
        self.label_percent_clahe_tile_size.configure(text = f"Tile Size: {tile_value}")

    def update_brightness(self, value):
        """Обновляет значение Шумоподавления"""
        brightness_value = int(float(value))
        self.label_percent_brightness.configure(text = f"Шумоподавление: {brightness_value}")

    def show_info(self):
        """Показывает окно информации"""
        show_info_dialog(self, "quality")

    def choose_files(self):
        file_path = filedialog.askopenfilename(
            title = "Выберите изображение",
            filetypes = [
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.jfif *.heic"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, file_path)

    def on_quality_enhance(self):
        """Улучшение качества с OpenCV (основная функция)"""
        input_path = self.source_entry.get()

        if not input_path or not os.path.isfile(input_path):
            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "Ошибка: Выберите файл для улучшения!")
            self.result_textbox.configure(state = "disabled")
            return

        file_dir = os.path.dirname(input_path)
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)
        output_path = os.path.join(file_dir, f"{name}_enhanced{ext}")

        result = advanced_enhance_image(
            input_path,
            output_path,
            clahe_clip_limit = float(self.slider_clahe_clip.get()),
            clahe_tile_size = int(self.slider_clahe_tile_size.get()),
            denoise_strength = int(self.slider_brightness.get())
        )

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")

        if result["success"]:
            self.result_textbox.insert("0.0",
                                       f"Успешно!\nИсходный размер: {result['original_size']} байт\nНовый размер: {result['new_size']} байт\nФайл сохранён: {result['output_path']}")
        else:
            self.result_textbox.insert("0.0", f"Ошибка: {result['error']}")

        self.result_textbox.configure(state = "disabled")