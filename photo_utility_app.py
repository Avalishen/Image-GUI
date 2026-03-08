import customtkinter as ctk

from views.welcome_view import create_welcome_frame
from views.duplicate_view import DuplicateView
from views.rename_view import RenameView
from views.metadata_view import MetadataView
from utils import load_icons
from utils import resource_path

class PhotoUtilityApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        """Иницилизация атрибутов класса (Frame)"""
        self.top_frame = None
        self.lower_frame = None
        self.welcome_frame = None
        self.duplicate_frame = None
        self.rename_frame = None
        self.metadata_frame = None
        """Иницилизация атрибутов класса (Button)"""
        self.duplicate_btn = None
        self.rename_btn = None
        self.metadata_btn = None
        self.convert_btn = None
        self.theme_btn = None
        self.return_btn = None
        """Настройка основного окна"""
        self.title("GUI v 0.3")
        self.geometry("800x700")
        self.resizable(False, False)
        self.iconbitmap(resource_path("images/icon.ico"))
        self.icons = load_icons()
        self.duplicate_results = None
        self.setup_ui()

    def setup_ui(self):

        self.top_frame = ctk.CTkFrame(self, width = 800, height = 93, corner_radius = 10, border_width = 1, border_color = "gray", fg_color = "transparent")
        self.top_frame.place(x = 0, y = 0)

        self.lower_frame = ctk.CTkFrame(self, width = 800, height = 608, corner_radius = 10, border_width = 1, border_color = "gray", fg_color = "transparent")
        self.lower_frame.place(x = 0, y = 92)

        self.welcome_frame = create_welcome_frame(self.lower_frame)

        self.duplicate_frame = DuplicateView(self.lower_frame)

        self.rename_frame = RenameView(self.lower_frame)

        self.metadata_frame = MetadataView(self.lower_frame)

        self.show_welcome()

        self.create_menu_buttons()

    def create_menu_buttons(self):
        self.duplicate_btn = ctk.CTkButton(
            self.top_frame, text = "Поиск\nДубликатов", cursor = "hand2",
            corner_radius = 10, image = self.icons["duplicate"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top",
            command = self.show_duplicates
        )
        self.duplicate_btn.place(x = 3, y = 3)

        self.rename_btn = ctk.CTkButton(
            self.top_frame, text = "Изменить\nНазвание", cursor = "hand2",
            corner_radius = 10, image = self.icons["rename"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top",
            command = self.show_rename
        )
        self.rename_btn.place(x = 99, y = 3)

        self.metadata_btn = ctk.CTkButton(
            self.top_frame, text = "Поиск\nМетаданных", cursor = "hand2",
            corner_radius = 10, image = self.icons["metadata"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top"
        )
        self.metadata_btn.place(x = 185, y = 3)

        self.convert_btn = ctk.CTkButton(
            self.top_frame, text = "Конвертация\nФайла", cursor = "hand2",
            corner_radius = 10, image = self.icons["convert"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top"
        )
        self.convert_btn.place(x = 287, y = 3)

        self.theme_btn = ctk.CTkButton(
            self.top_frame, text = "Сменить\nТему", cursor = "hand2",
            corner_radius = 10, image = self.icons["moon"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top", command = self.theme)
        self.theme_btn.place(x = 634, y = 3)

        self.return_btn = ctk.CTkButton(
            self.top_frame, text = "Вернуться\nНазад", cursor = "hand2",
            corner_radius = 10, image = self.icons["undo"],
            width = 50, height = 50, fg_color = "transparent",
            hover_color = "gray", compound = "top",
            command = self.show_welcome
        )
        self.return_btn.place(x = 712, y = 3)

    def theme(self):
        """Смена темы окна"""
        current = ctk.get_appearance_mode()
        new_theme = "dark" if current == "Light" else "light"
        ctk.set_appearance_mode(new_theme)

        if new_theme == "light":
            text_color = "black"
        else:
            text_color = "white"

        for btn in[
            getattr(self, "duplicate_btn", None),
            getattr(self, "rename_btn", None),
            getattr(self, "metadata_btn", None),
            getattr(self, "convert_btn", None),
            getattr(self, "theme_btn", None),
            getattr(self, "return_btn", None),

        ]:
            if btn is not None:
                btn.configure(text_color = text_color)

        if hasattr(self, "duplicate_frame"):
            self.duplicate_frame.browse_source_btn.configure(text_color = text_color)
            self.duplicate_frame.browse_dest_btn.configure(text_color = text_color)
            self.duplicate_frame.search_btn.configure(text_color = text_color)
            self.duplicate_frame.move_btn.configure(text_color = text_color)

    def reload_icons(self):
        """Смена иконок при смене темы экрана"""
        self.icons = load_icons()

        if hasattr(self, "duplicate_btn"):
            self.duplicate_btn.configure(image = self.icons["duplicate"])
        if hasattr(self, "rename_btn"):
            self.rename_btn.configure(image=self.icons["rename"])

    def hide_all_frames(self):
        """Скрывает все экраны"""
        self.welcome_frame.place_forget()
        self.duplicate_frame.place_forget()
        self.rename_frame.place_forget()
        self.metadata_frame.place_forget()
        #self.convert_frame.place_forget()

    def show_welcome(self):
        """Показывает приветственный экран"""
        self.hide_all_frames()
        self.welcome_frame.place(x = 10, y = 10)

    def show_duplicates(self):
        """Показывает экран поиска дубликатов"""
        self.hide_all_frames()
        self.duplicate_frame.place(x = 10, y = 10)

    def show_rename(self):
        """Показывает экран переименования файлов"""
        self.hide_all_frames()
        self.rename_frame.place(x = 10, y = 10)

    def show_metadata(self):
        self.hide_all_frames()
        self.metadata_frame.place(x = 10, y = 10)
