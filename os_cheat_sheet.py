"""
Cheat Sheet: Модуль os в Python
================================

os — модуль для взаимодействия с операционной системой:
- работа с файлами и директориями
- выполнение системных команд
- переменные окружения
"""

"""
# ИМПОРТ
import os

# ПУТИ И ДИРЕКТОРИИ
os.getcwd()                    # текущая рабочая директория
os.chdir(path)                 # изменить рабочую директорию
os.listdir(path = '.')           # список файлов/папок в директории
os.mkdir(path)                 # создать папку
os.makedirs(path)              # создать папку рекурсивно (все промежуточные)
os.rmdir(path)                 # удалить пустую папку
os.removedirs(path)            # удалить папку рекурсивно (если пустые)

# ПРОВЕРКИ
os.path.exists(path)           # существует ли путь
os.path.isfile(path)           # является ли файлом
os.path.isdir(path)            # является ли директорией
os.path.isabs(path)            # абсолютный ли путь
os.access(path, mode)          # проверка прав доступа (F_OK, R_OK, W_OK, X_OK)

# ИНФОРМАЦИЯ О ФАЙЛАХ
os.path.getsize(path)          # размер файла
os.path.getmtime(path)         # время последнего изменения (timestamp)
os.path.getctime(path)         # время создания (на Windows)
os.path.getatime(path)         # время последнего доступа

# РАБОТА С ПУТЯМИ
os.path.join('path', 'to', 'file')  # объединение частей пути
os.path.split(path)            # разделить на (директория, файл)
os.path.dirname(path)          # директория из пути
os.path.basename(path)         # имя файла из пути
os.path.splitext(filename)     # разделить на (имя, расширение)

# УДАЛЕНИЕ / ПЕРЕИМЕНОВАНИЕ
os.remove(path)                # удалить файл
os.rename(src, dst)            # переименовать файл/папку
os.renames(old, new)           # переименовать с созданием промежуточных директорий

# СИСТЕМНЫЕ КОМАНДЫ
os.system(command)             # выполнить команду в терминале
os.popen(command)              # выполнить команду и вернуть объект (не рекомендуется)
os.walk(top)                   # обход дерева директорий (итератор по (dirpath, dirnames, filenames))

# ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
os.environ                     # словарь переменных окружения
os.environ['VAR'] = 'value'    # установить переменную
os.getenv('VAR', default)      # получить переменную с дефолтом
"""