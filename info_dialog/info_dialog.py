import customtkinter as ctk
from .instructions import INSTRUCTIONS


def show_info_dialog(parent, section_key):
    """
    Показывает информационное окно с инструкцией

    Параметры:
        parent: родительское окно
        section_key: ключ раздела ("convert", "enhance", "rename" и т.д.)
    """

    # Получаем текст инструкции по ключу
    text = INSTRUCTIONS.get(section_key, "Инструкция не найдена")

    # Создаём заголовок окна
    titles = {
        "convert": "Инструкция: Конвертация",
        "enhance": "Инструкция: Улучшение качества",
        "rename": "Инструкция: Переименование",
        "duplicates": "Инструкция: Поиск дубликатов",
        "metadata": "Инструкция: Метаданные"
    }

    title = titles.get(section_key, "Инструкция")

    # Создаём окно (ОДНО окно для ВСЕХ инструкций!)
    info_window = ctk.CTkToplevel(parent)
    info_window.title(title)
    info_window.geometry("600x450")

    # Центрируем окно
    info_window.transient(parent)
    info_window.grab_set()

    # Создаём текстовое поле
    text_box = ctk.CTkTextbox(
        info_window,
        width = 560,
        height = 410,
        font = ("Arial", 12),
        wrap = "word"
    )
    text_box.insert("0.0", text)
    text_box.configure(state = "disabled")
    text_box.place(x = 20, y = 20)