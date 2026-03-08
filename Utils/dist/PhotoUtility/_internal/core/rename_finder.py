import os
import datetime
import hashlib

def rename_files_in_folder(folder_path: str, template: str) -> dict:
    """Переименование файлов своим именем"""
    files = os.listdir(folder_path)
    search_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    result = {}

    for i, file in enumerate(search_files, start = 1):
        ext = file.split(".")[-1]
        new_name = f"{template}_{i}.{ext}"
        new_path = os.path.join(folder_path, new_name)

        if os.path.exists(new_path):
            print(f"Файл {new_name} уже существует")
            continue

        old_path = os.path.join(folder_path, file)
        os.rename(old_path, new_path)
        result[file] = new_name

    return result

def generate_timestamp_hash(length: int = 15) -> str:
    """Генерация хеш от текущей даты и времени"""
    timestamp = str(datetime.datetime.now())

    hash_object = hashlib.md5(timestamp.encode())
    hash_hex = hash_object.hexdigest()

    return f"{hash_hex[:length]}"

def rename_files_with_hash(folder_path: str, prefix: str = "") -> dict:
    """Переименовывает файлы с использованием хеш-названий"""
    files = os.listdir(folder_path)
    search_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    result = {}
    for i, file in enumerate(search_files, start = 1):
        ext = file.split(".")[-1]

        timestamp_hash = generate_timestamp_hash(15)
        if prefix:
            new_name = f"{prefix}_{timestamp_hash}_{i}.{ext}"
        else:
            new_name = f"{timestamp_hash}_{i}.{ext}"

        new_path = os.path.join(folder_path, new_name)

        old_path = os.path.join(folder_path, file)
        os.rename(old_path, new_path)
        result[file] = new_name

    return result

