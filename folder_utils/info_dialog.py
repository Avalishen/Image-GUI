import customtkinter as ctk
from .instructions import INSTRUCTIONS


def show_info_dialog(parent, section_key):

    text = INSTRUCTIONS.get(section_key, "Инструкция не найдена")

    titles = {
        "duplicates": "Инструкция: Поиск дубликатов",
        "rename": "Инструкция: Переименование",
        "metadata": "Инструкция: Метаданные",
        "convert": "Инструкция: Конвертация",
        "enhance": "Инструкция: Улучшение качества",
    }

    title = titles.get(section_key, "Инструкция")

    info_window = ctk.CTkToplevel(parent)
    info_window.title(title)
    info_window.geometry("600x450")
    info_window.resizable(False, False)

    info_window.transient(parent)
    info_window.grab_set()

    text_box = ctk.CTkTextbox(info_window, width = 560, height = 410, font = ("Roboto", 14), wrap = "word")
    text_box.insert("0.0", text)
    text_box.configure(state = "disabled")
    text_box.place(x = 20, y = 20)