import customtkinter as ctk
from utils import open_link

def create_welcome_frame(parent):
    frame = ctk.CTkFrame(
        parent, width = 780, height = 588,
        corner_radius = 10, border_width = 1,
        border_color = "gray", fg_color = "transparent"
    )

    title_label = ctk.CTkLabel(frame, text = "Добро пожаловать в PhotoUtility!", font = ("Roboto", 20))
    title_label.place(x = 10, y = 10)

    welcome_text = (
        "PhotoUtility — это локальная утилита для работы с фотографиями.\n\n"
        "Она поможет вам:\n"
        " ✔ Найти и удалить дубликаты изображений\n"
        " ✔ Переименовать файлы по шаблону\n"
        " ✔ Удалить скрытые метаданные (EXIF, GPS и др.)\n"
        " ✔ Конвертировать RAW, HEIC и другие форматы в JPG/PNG\n\n"
        "Все операции выполняются на вашем компьютере —\n"
        "Ваши файлы не попадут в интернет.\n\n"
        " ✔ Это open-source утилита: бесплатная, прозрачная\n"
        "Без скрытых функций. Вы можете изучить код,\n"
        "Улучшить его или собрать свою версию —\n"
        "Всё доступно на GitHub.\n\n"
        "Для начала работы нажмите на нужную кнопку в верхнем меню"
    )

    description_label = ctk.CTkLabel(frame, text  = welcome_text, font = ("Roboto", 18), justify = "left")
    description_label.place(x = 10, y = 50)

    repository_label = ctk.CTkLabel(frame, text = "→ Репозиторий проекта", text_color = "#999999",
                                    font = ("Roboto", 10, "underline"), cursor = "hand2")
    repository_label.bind("<Button-1>", lambda e: open_link("https://github.com/Avalishen/PhotoUtility"))
    repository_label.place(x = 480, y = 559)

    github_label = ctk.CTkLabel(frame, text = "→ Мой GitHub", text_color = "#999999",
                                font = ("Roboto", 10, "underline"), cursor = "hand2")
    github_label.bind("<Button-1>", lambda e: open_link("https://github.com/Avalishen"))
    github_label.place(x = 610, y = 559)

    telegram_label = ctk.CTkLabel(frame, text = "→ Мой Telegram", text_color = "#999999",
                                  font = ("Roboto", 10, "underline"), cursor = "hand2")
    telegram_label.bind("<Button-1>", lambda e: open_link("https://t.me/AvalishenSG"))
    telegram_label.place(x = 690, y = 559)

    author_label = ctk.CTkLabel(
        frame, text = "Создано для фотографов и коллекционеров файлов",
        font = ("Roboto", 10), text_color = "#999999"
    )
    author_label.place(x = 10, y = 559)

    return frame