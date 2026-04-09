import customtkinter as ctk
import os

from PIL import Image
from placeholders import placeholder_text_1
from utils import resource_path
from folder_utils.info_dialog import show_info_dialog
from core.quality_core import enhance_image_quality
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

        """Поле Резкость"""
        self.label_sharpness = ctk.CTkLabel(self, text = "Резкость:")
        self.label_sharpness.place(x = 20, y = 60)

        """Слайдер (Резкость)"""
        self.slider_sharpness = ctk.CTkSlider(self, from_ = 0, to = 200,
                                              width = 200, command = self.update_sharpness)
        self.slider_sharpness.set(100)
        self.slider_sharpness.place(x = 130, y = 65)

        """Поле с процентами для слайдера (Резкость)"""
        self.label_percent_sharpness = ctk.CTkLabel(self, text = "Резкость в %")
        self.label_percent_sharpness.place(x = 350, y = 60)

        """Поле Контраст"""
        self.label_contrast = ctk.CTkLabel(self, text = "Контраст:")
        self.label_contrast.place(x = 20, y = 90)

        """Слайдер (Контраст)"""
        self.slider_contrast = ctk.CTkSlider(self, from_ = 0, to = 200,
                                             width = 200, command = self.update_contrast)
        self.slider_contrast.set(100)
        self.slider_contrast.place(x = 130, y = 95)

        """Поле с процентами для слайдера (Контраст)"""
        self.label_percent_contrast = ctk.CTkLabel(self, text = "Контраст в %")
        self.label_percent_contrast.place(x = 350, y = 90)

        """Поле Яркость"""
        self.label_brightness = ctk.CTkLabel(self, text = "Яркость:")
        self.label_brightness.place(x = 20, y = 120)

        """Слайдер (Яркость)"""
        self.slider_brightness = ctk.CTkSlider(self, from_ = 0, to = 200,
                                               width = 200, command = self.update_brightness)
        self.slider_brightness.set(100)
        self.slider_brightness.place(x = 130, y = 125)

        """Поле с процентами для слайдера (Яркость)"""
        self.label_percent_brightness = ctk.CTkLabel(self, text = "Яркость в %")
        self.label_percent_brightness.place(x = 350, y = 120)

        """Поле Насыщенность"""
        self.label_saturation = ctk.CTkLabel(self, text = "Насыщенность:")
        self.label_saturation.place(x = 20, y = 150)

        """Слайдер (Насыщенность)"""
        self.slider_saturation = ctk.CTkSlider(self, from_ = 0, to = 200,
                                               width = 200, command = self.update_saturation)
        self.slider_saturation.set(100)
        self.slider_saturation.place(x = 130, y = 155)

        """Поле с процентами для слайдера (Насыщенность)"""
        self.label_percent_saturation = ctk.CTkLabel(self, text = "Насыщенность в %")
        self.label_percent_saturation.place(x = 350, y = 150)

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

    def update_sharpness(self, value):
        """Обновляет значение Резкости"""
        percent = int(float(value))
        self.label_percent_sharpness.configure(text = f"Резкость: {percent}%")

    def update_contrast(self, value):
        """Обновляет значение Контраста"""
        percent = int(float(value))
        self.label_percent_contrast.configure(text = f"Контраст: {percent}%")

    def update_brightness(self, value):
        """Обновляет значение Яркости"""
        percent = int(float(value))
        self.label_percent_brightness.configure(text = f"Яркость: {percent}%")

    def update_saturation(self, value):
        """Обновляет значение Насыщенности"""
        percent = int(float(value))
        self.label_percent_saturation.configure(text = f"Насыщенность: {percent}%")

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
        sharpness = self.slider_sharpness.get() / 100
        contrast = self.slider_contrast.get() / 100
        brightness = self.slider_brightness.get() / 100
        saturation = self.slider_saturation.get() / 100

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

        result = enhance_image_quality(
            input_path,
            output_path,
            sharpness = sharpness,
            contrast = contrast,
            brightness = brightness,
            saturation = saturation,
        )

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")

        if result["success"]:
            self.result_textbox.insert("0.0", f"Успешно!\nИсходный размер: {result['original_size']} байт\nНовый размер: {result['new_size']} байт\nФайл сохранён: {result['output_path']}")
        else:
            self.result_textbox.insert("0.0", f"Ошибка: {result['error']}")

        self.result_textbox.configure(state = "disabled")