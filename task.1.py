# Напишіть програму на Python, яка рекурсивно копіює файли у вихідній директорії, 
# переміщає їх до нової директорії та сортує в піддиректорії, назви яких базуються на розширенні файлів.
# Також візьміть до уваги наступні умови:
# 1. Парсинг аргументів. Скрипт має приймати два аргументи командного рядка: шлях до вихідної директорії та шлях до 
# директорії призначення (за замовчуванням, якщо тека призначення не була передана, вона повинна бути з назвою dist).
# 2. Рекурсивне читання директорій:
# Має бути написана функція, яка приймає шлях до директорії як аргумент.
# Функція має перебирати всі елементи у директорії.
# Якщо елемент є директорією, функція повинна викликати саму себе рекурсивно для цієї директорії.
# Якщо елемент є файлом, він має бути доступним для копіювання.
# 3. Копіювання файлів:
# Для кожного типу файлів має бути створений новий шлях у вихідній директорії, використовуючи розширення файлу для назви піддиректорії.
# Файл з відповідним типом має бути скопійований у відповідну піддиректорію.
# 4. Обробка винятків. Код має правильно обробляти винятки, наприклад, помилки доступу до файлів або директорій.

import os
import shutil
import argparse

def create_dir_if_not_exists(dir_path: str) -> None:
  if not os.path.exists(dir_path):
    print(f'Destination_dir {dir_path} does not exist, creating it...')
    os.makedirs(dir_path)

def copy_files(source_dir: str, destination_dir: str) -> dict[str, int]:
  result = {
    'error_count': 0
  }

  for item in os.listdir(source_dir):
    item_path = os.path.join(source_dir, item)
    
    if os.path.isdir(item_path):
      dir_path = os.path.join(destination_dir, item)
      create_dir_if_not_exists(dir_path)
      
      res = copy_files(item_path, dir_path)
      result['error_count'] += res['error_count']
    elif os.path.isfile(item_path):
      # Get extension without dot
      file_extension = os.path.splitext(item)[1][1:]
      if not file_extension:
        file_extension = 'no_extension'
          
      extension_dir = os.path.join(destination_dir, file_extension)
      create_dir_if_not_exists(extension_dir)
          
      destination_path = os.path.join(extension_dir, item)
      
      try:
          shutil.copy2(item_path, destination_path)
      except PermissionError:
          print(f'Permission denied when copying {item_path}')
          result['error_count'] += 1
      except OSError as e:
          print(f'Error copying {item_path}: {e}')
          result['error_count'] += 1

  return result


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  parser.add_argument("--source_dir", required=True, help="Source directory")
  parser.add_argument("--destination_dir", help="Destination directory", default=os.path.join(os.getcwd(), 'dist'))
  
  args = parser.parse_args()

  print('source_dir', args.source_dir)
  print('destination_dir', args.destination_dir)

  create_dir_if_not_exists(args.destination_dir)

  result = copy_files(args.source_dir, args.destination_dir)

  if result['error_count'] > 0:
    print(f'File was copied successfully. Total errors: {result["error_count"]}')
  else:
    print('File was copied successfully.')


