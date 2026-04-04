import os
from PIL import Image
from pillow_heif import register_heif_opener
import rawpy
import numpy as np

register_heif_opener()

def convert_image(input_path: str, output_format: str, quality: int = 95):

    try:
        if not os.path.isfile(input_path):
            return {"success": False, "error": "Файл не найден"}

        file_ext = os.path.splitext(input_path)[1].lower()

        if file_ext in ['.cr2', '.cr3', '.nef', '.arw', '.dng', '.raf', '.orf', '.rw2']:
            with rawpy.imread(input_path) as raw:
                rgb = raw.postprocess()
            img = Image.fromarray(rgb)
        else:
            img = Image.open(input_path)


        file_dir = os.path.dirname(input_path)
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)

        format_to_ext = {
            "JPEG": "jpg",
            "PNG": "png",
            "WEBP": "webp",
            "HEIC": "heic",
            "GIF": "gif",
        }

        output_ext = format_to_ext.get(output_format.upper(), "jpg")
        output_path = os.path.join(file_dir, f"{name}.{output_ext}")

        save_kwargs = {"format": output_format.upper()}

        if output_format.upper() in ["JPEG", "JPG"]:
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask = img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True

        elif output_format.upper() == "PNG":
            if img.mode not in ("RGB", "RGBA", "P", "L"):
                img = img.convert("RGBA")

            save_kwargs["optimize"] = True

        elif output_format.upper() == "WEBP":
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            save_kwargs["quality"] = quality
            save_kwargs["method"] = 6
            save_kwargs["save_all"] = True

        elif output_format.upper() == "HEIC":
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

        elif output_format.upper() == "GIF":
            if img.mode not in ("P", "L"):
                img = img.convert("P", palette = Image.ADAPTIVE)

            save_kwargs["optimize"] = True

        img.save(output_path, **save_kwargs)

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