import customtkinter as ctk
import os
import threading
from tkinter import filedialog
from PIL import Image
from utils import resource_path
from core.quality_core import ai_enhancer
from placeholders import placeholder_text_1
from folder_utils.info_dialog import show_info_dialog

"""Иконки"""
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
        super().__init__(parent, width = 780, height = 588, border_width = 1,
                         corner_radius = 10, border_color = "gray", fg_color = "transparent")

        """Поле для пути к файлу"""
        self.source_entry = ctk.CTkEntry(self, width = 240, placeholder_text = placeholder_text_1, corner_radius = 10)
        self.source_entry.place(x = 20, y = 20)

        self.review_btn = ctk.CTkButton(self, text="Обзор...", image=quality_image, corner_radius=10,
                                        fg_color="transparent", hover_color="gray", command=self.choose_files, width=80)
        self.review_btn.place(x=270, y=20)

        """Масштаб"""
        self.scale_label = ctk.CTkLabel(self, text="Масштаб увеличения:")
        self.scale_label.place(x = 20, y = 70)

        self.scale_slider = ctk.CTkSlider(self, from_ = 1, to = 4, number_of_steps = 3,
                                          width = 200, command = self.update_scale)
        self.scale_slider.set(2)
        self.scale_slider.place(x = 200, y = 75)

        self.scale_value = ctk.CTkLabel(self, text="Масштаб: 2x")
        self.scale_value.place(x = 420, y = 70)

        """Размер тайла"""
        self.tile_label = ctk.CTkLabel(self, text="Размер тайла (память):")
        self.tile_label.place(x = 20, y = 110)

        self.tile_slider = ctk.CTkSlider(self, from_ = 64, to = 512, number_of_steps = 7,
                                         width = 200, command = self.update_tile)
        self.tile_slider.set(256)
        self.tile_slider.place(x = 200, y = 115)

        self.tile_value = ctk.CTkLabel(self, text = "Тайл: 256")
        self.tile_value.place(x = 420, y = 110)

        """Шумоподавление"""
        self.denoise_label = ctk.CTkLabel(self, text="Шумоподавление:")
        self.denoise_label.place(x = 20, y = 150)

        self.denoise_slider = ctk.CTkSlider(self, from_ = 0, to = 20, number_of_steps = 20,
                                            width = 200, command = self.update_denoise)
        self.denoise_slider.set(5)
        self.denoise_slider.place(x = 200, y = 155)

        self.denoise_value = ctk.CTkLabel(self, text="Шум: 5")
        self.denoise_value.place(x = 420, y = 150)

        """Прогресс-бар"""
        self.progress_bar = ctk.CTkProgressBar(self, width = 740, height = 20)
        self.progress_bar.place(x = 20, y = 210)
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(self, text = "Готов к обработке")
        self.progress_label.place(x = 20, y = 240)

        """Textbox результата"""
        self.result_textbox = ctk.CTkTextbox(self, width = 740, height = 230, corner_radius = 10)
        self.result_textbox.place(x = 20, y = 280)
        self.result_textbox.insert("0.0", "Результат появится здесь...")
        self.result_textbox.configure(state = "disabled")

        self.quality_btn = ctk.CTkButton(self, text = "Улучшить", width = 200,
                                         command = self.start_enhancement,
                                         fg_color = "green", hover_color = "darkgreen",
                                         corner_radius = 10)
        self.quality_btn.place(x = 20, y = 530)

        self.cancel_btn = ctk.CTkButton(self, text = "Отмена", width = 150,
                                        command = self.cancel_enhancement,
                                        fg_color = "red", hover_color = "darkred",
                                        corner_radius = 10, state = "disabled")
        self.cancel_btn.place(x = 240, y = 530)

        self.info_btn = ctk.CTkButton(self, text = "INFO", image = info_image, corner_radius = 10,
                                      fg_color = "transparent", hover_color = "gray", width = 80, command = self.show_info)
        self.info_btn.place(x = 675, y = 530)

        self.model_loaded = False

    def show_info(self):
        show_info_dialog(self, "quality")

    """Обновление ползунков"""
    def update_scale(self, value):
        scale = int(float(value))
        self.scale_value.configure(text = f"Масштаб: {scale}x")

    def update_tile(self, value):
        tile = int(float(value))
        self.tile_value.configure(text = f"Тайл: {tile}")
        ai_enhancer.input_size = tile

    def update_denoise(self, value):
        strength = int(float(value))
        self.denoise_value.configure(text = f"Шум: {strength}")
        ai_enhancer.denoise_strength = strength

    """Выбор файла"""
    def choose_files(self):
        file_path = filedialog.askopenfilename(
            title = "Выберите изображение",
            filetypes = [
                ("Изображения", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, file_path)

    """Запуск улучшения"""
    def start_enhancement(self):
        input_path = self.source_entry.get()

        if not input_path or not os.path.isfile(input_path):
            self.result_textbox.configure(state = "normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "Выберите файл для улучшения!")
            self.result_textbox.configure(state = "disabled")
            return

        file_dir = os.path.dirname(input_path)
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)
        output_path = os.path.join(file_dir, f"{name}_ai_enhanced.png")

        """Загружаем модель если ещё не загружена"""
        if not self.model_loaded:
            self.progress_label.configure(text = "Загрузка модели...")
            ai_enhancer.load_model()
            self.model_loaded = True

        """Блокируем кнопки"""
        self.quality_btn.configure(state = "disabled")
        self.cancel_btn.configure(state = "normal")

        scale = int(self.scale_slider.get())
        thread = threading.Thread(
            target = self.enhance_worker,
            args = (input_path, output_path, scale)
        )
        thread.start()

    def enhance_worker(self, input_path, output_path, scale):
        def update_progress(percent, message):
            self.progress_bar.set(percent / 100)
            self.progress_label.configure(text=message)

        result = ai_enhancer.enhance_image(
            input_path,
            output_path,
            scale = scale,
            progress_callback = update_progress
        )

        self.after(0, self.update_ui_after_enhancement, result)

    def update_ui_after_enhancement(self, result):
        self.quality_btn.configure(state = "normal")
        self.cancel_btn.configure(state = "disabled")

        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0", "end")

        if result["success"]:
            orig_size = result["original_size"] / (1024 * 1024)
            new_size = result["new_size"] / (1024 * 1024)
            self.result_textbox.insert("0.0",
                                       f"✅ Успешно!\n"
                                       f"Исходный размер: {orig_size:.2f} МБ\n"
                                       f"Новый размер: {new_size:.2f} МБ\n"
                                       f"Сохранено: {result['output_path']}")
        else:
            self.result_textbox.insert("0.0", f"Ошибка: {result['error']}")

        self.result_textbox.configure(state = "disabled")

    def cancel_enhancement(self):
        ai_enhancer.cancel()
        self.progress_label.configure(text = "Отмена...")