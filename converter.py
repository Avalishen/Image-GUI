import os
from PIL import Image

def convert_png_to_jpg(input_path: str, output_path: str, quality: int = 95) -> bool:
    try:
        if not os.path.isfile(input_path):
            print(f"Ошибка: файл не найден — {input_path}")
            return False

        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask = img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(output_path, "JPEG", quality = quality, optimize = True)
        return True
    except Exception as e:
        print(f"Ошибка конвертации {input_path} → {output_path}: {e}")
        return False


if __name__ == "__main__":
    input_file = input("Введите путь к PNG-файлу: ").strip('"')
    output_file = input("Куда сохранить JPG: ").strip('"')

    success = convert_png_to_jpg(input_file, output_file, quality=90)
    if success:
        print("✅ Готово!")
    else:
        print("❌ Ошибка")