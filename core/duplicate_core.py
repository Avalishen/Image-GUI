import os
import imagehash

from PIL import Image
from collections import defaultdict

def find_image_duplicates(folder_path: str) -> dict:
    """Возвращает {хеш: [список_файлов]} — только дубликаты (группы из 2+ файлов)."""
    duplicates = defaultdict(list)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue
        try:
            with Image.open(file_path) as img:
                img_hash = str(imagehash.phash(img))
                duplicates[img_hash].append(file_path)
        except(IOError, SyntaxError, ValueError):
            continue
    duplicate_group = {h: files for h, files in duplicates.items() if len(files) > 1}
    return duplicate_group

def move_duplicates_to_folder(duplicate_groups: dict, target_folder: str) -> int:
    """Перемещает все файлы, кроме первого в каждой группе. Возвращает число перемещённых."""
    os.makedirs(target_folder, exist_ok=True)
    moved = 0
    for files in duplicate_groups.values():
        for file_path in files[1:]:  # пропускаем оригинал (первый файл)
            try:
                filename = os.path.basename(file_path)
                new_path = os.path.join(target_folder, filename)
                counter = 1
                while os.path.exists(new_path):
                    name, ext = os.path.splitext(filename)
                    new_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
                    counter += 1
                os.rename(file_path, new_path)
                moved += 1
            except OSError:
                continue
    return moved