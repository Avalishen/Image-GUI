import os
import cv2
import numpy as np
from PIL import Image


def advanced_enhance_image(
        input_path: str,
        output_path: str,
        clahe_clip_limit: float = 1.5,
        clahe_tile_size: int = 16,
        denoise_strength: int = 5
) -> dict:
    try:
        if not os.path.exists(input_path):
            return {"success": False, "error": "Исходный файл не найден"}

        pil_img = Image.open(input_path)
        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')

        opencv_img = np.array(pil_img)
        img = cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR)

        if denoise_strength > 0:
            d = min(15, max(3, denoise_strength))

            sigma_color = 20 + (denoise_strength * 2)
            sigma_space = 20 + (denoise_strength * 2)

            denoised = cv2.bilateralFilter(
                img,
                d=d,
                sigmaColor=sigma_color,
                sigmaSpace=sigma_space
            )
        else:
            denoised = img

        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        tile_size = max(2, min(64, clahe_tile_size))
        clahe = cv2.createCLAHE(clipLimit=clahe_clip_limit, tileGridSize=(tile_size, tile_size))
        l_clahe = clahe.apply(l_channel)

        lab_clahe = cv2.merge([l_clahe, a_channel, b_channel])
        enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

        if denoise_strength > 0:
            blurred = cv2.GaussianBlur(enhanced, (0, 0), 3)
            enhanced = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)

        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        pil_result = Image.fromarray(enhanced_rgb)

        pil_result.save(output_path, quality=95, optimize=True)

        return {
            "success": True,
            "message": "Продвинутое улучшение успешно",
            "output_path": output_path,
            "original_size": os.path.getsize(input_path),
            "new_size": os.path.getsize(output_path)
        }

    except ImportError:
        return {"success": False, "error": "Требуется установка opencv-python и numpy"}
    except Exception as e:
        return {"success": False, "error": f"Ошибка обработки: {str(e)}"}