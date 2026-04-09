import os

from PIL import Image, ImageEnhance
from Tools.scripts.fixnotice import process


def enhance_image_quality(
        input_path: str,
        output_path: str,
        sharpness: float = 1.0,
        contrast: float = 1.0,
        brightness: float = 1.0,
        saturation: float = 1.0
) -> dict:
    try:
        if not os.path.exists(input_path):
            return{
                "success": False,
                "error": "Исходный файл не найден"
            }

        with Image.open(input_path) as img:
            processed_img = img.copy()

            """Резкость"""
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(processed_img)
                processed_img = enhancer.enhance(sharpness)

            """Контраст"""
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(processed_img)
                processed_img = enhancer.enhance(contrast)

            """Яркость"""
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(processed_img)
                processed_img = enhancer.enhance(brightness)

            """Насыщенность"""
            if saturation != 1.0:
                enhancer = ImageEnhance.Sharpness(processed_img)
                processed_img = enhancer.enhance(saturation)

            final_img = processed_img

            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if processed_img.mode == "RGBA":
                    background = Image.new("RGB", processed_img.size, (255, 255, 255))
                    background.paste(processed_img, mask=processed_img.split()[-1])
                    final_img = background
                elif processed_img.mode == "LA":
                    background = Image.new("L", processed_img.size, 255)
                    background.paste(processed_img, mask=processed_img.split()[-1])
                    final_img = background
                elif processed_img.mode == "P":
                    rgba_img = processed_img.convert("RGBA")
                    background = Image.new("RGB", rgba_img.size, (255, 255, 255))
                    background.paste(rgba_img, mask=rgba_img.split()[-1])
                    final_img = background
                elif processed_img.mode not in ("RGB", "L"):
                    final_img = processed_img.convert("RGB")

            save_kwargs = {}
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                save_kwargs["quality"] = 95
                save_kwargs["optimize"] = True
            elif output_path.lower().endswith('.webp'):
                save_kwargs["quality"] = 95
                save_kwargs["method"] = 6

            final_img.save(output_path, **save_kwargs)

        return {
            "success": True,
            "message": "Качество изображения успешно улучшено",
            "output_path": output_path,
            "original_size": os.path.getsize(input_path),
            "new_size": os.path.getsize(output_path)
        }

    except FileNotFoundError:
        return {"success": False, "error": "Файл не найде"}

    except PermissionError:
        return {"success": False, "error": "Нет прав на запись файла"}

    except Exception as e:
        return {"success": False, "error": f"Ошибка обработки: {str(e)}"}