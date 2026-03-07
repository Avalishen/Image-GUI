import os
from PIL import Image
import customtkinter as ctk

def load_icons():
    icon_configs = {
        "duplicate":     ("images/album-dark.png", "images/album-light.png", (40, 40)),
        "rename":        ("images/rename-dark.png", "images/rename-light.png", (40, 40)),
        "metadata":      ("images/metadata-dark.png", "images/metadata-light.png", (40, 40)),
        "convert":       ("images/convert-dark.png", "images/convert-light.png", (40, 40)),
        "undo":          ("images/undo-dark.png", "images/undo-light.png", (40, 40)),
        "folder":        ("images/folder-dark.png", "images/folder-light.png", (20, 20)),
        "moon":          ("images/moon-dark.png", "images/sun-light.png", (40, 40)),
        "sun":           ("images/sun-dark.png", "images/moon-light.png", (40, 40)),
    }

    icons = {}
    for name, (light_path, dark_path, size) in icon_configs.items():
        try:
            light_img = Image.open(light_path) if os.path.isfile(light_path) else None
            dark_img = Image.open(dark_path) if os.path.isfile(dark_path) else None

            if light_img is None:
                light_img = dark_img
            if dark_img is None:
                dark_img = light_img

            if light_img is None:
                print(f"⚠️ Иконка не найдена: {light_path} или {dark_path}")
                icons[name] = None
            else:
                icons[name] = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=size)

        except Exception as e:
            print(f"❌ Ошибка загрузки иконки {name}: {e}")
            icons[name] = None

    return icons

def open_link(url):
    import webbrowser
    webbrowser.open(url)