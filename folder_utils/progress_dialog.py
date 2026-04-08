import customtkinter as ctk


def show_progress_dialog(parent, progress, status):

    if not hasattr(parent, "_progress_window"):
        create_progress_window(parent)

    parent._progress_window.progress_bar.set(progress / 100)
    parent._progress_window.status_label.configure(text = status)
    parent._progress_window.update()

def create_progress_window(parent):
    """Окно прогресс-бара"""
    window = ctk.CTkToplevel(parent)
    window.title("Выполнение операции")
    window.geometry("400x150")
    window.resizable(False, False)
    window.transient(parent)

    status_label = ctk.CTkLabel(window, text = "Подготовка...", font = ("Roboto", 12))
    status_label.place(x = 10, y = 10)

    progress_bar = ctk.CTkProgressBar(window, width = 380, height = 20)
    progress_bar.place(x = 10, y = 50)
    progress_bar.set(0)

    parent._progress_window = window
    parent._progress_window.status_label = status_label
    parent._progress_window.progress_bar = progress_bar

def hide_progress_dialog(parent):
    if hasattr(parent, "_progress_window"):
        parent._progress_window.destroy()
        delattr(parent, "_progress_window")