import os
from PIL import Image


def convert_png_to_jpg(input_path: str, output_path: str, quality: int = 95):

    try:
        if not os.path.isfile(input_path):
            return {"success": False, "error": "Файл не найден"}

        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))

                if img.mode == "P":
                    img = img.convert("RGBA")

                background.paste(img, mask=img.split()[-1])
                img = background

            elif img.mode != "RGB":
                img = img.convert("RGB")

            img.save(output_path, "JPEG", quality=quality, optimize=True)

        return {
            "success": True,
            "message": "Изображение успешно конвертировано",
            "output_path": output_path,
            "original_size": os.path.getsize(input_path),
            "new_size": os.path.getsize(output_path)
        }

    except FileNotFoundError:
        return {"success": False, "error": "Файл не найден"}

    except PermissionError:
        return {"success": False, "error": "Нет прав на запись"}

    except Exception as e:
        return {"success": False, "error": str(e)}