import os
from PIL import Image


def convert_image(input_path: str, output_format: str, quality: int = 95):

    try:
        if not os.path.isfile(input_path):
            return {"success": False, "error": "Файл не найден"}

        with Image.open(input_path) as img:
            file_dir = os.path.dirname(input_path)
            file_name = os.path.basename(input_path)
            name, ext = os.path.splitext(file_name)

            format_to_ext = {
                "JPEG": "jpg",
                "PNG": "png",
                "WEBP": "webp",
                "HEIC": "heic",
            }

            output_ext = format_to_ext.get(output_format.upper(), "jpg")
            output_path = os.path.join(file_dir, f"{name}.{output_ext}")

            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))

                if img.mode == "P":
                    img = img.convert("RGBA")

                background.paste(img, mask = img.split()[-1])
                img = background

            elif img.mode != "RGB":
                img = img.convert("RGB")

            img.save(output_path, output_format.upper(), quality = quality, optimize=True)

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