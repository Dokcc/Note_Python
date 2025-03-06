# Заметки+.рyw Ver.:T-1.10
    # [версия для Windows]1111111 2222
    # Новая запись (очистка текста) +
    # Открыть файл (загрузка текста) +
    # Сохранить (сохранение текста) +
    # Сохранить как (Ctrl+Shift+S) +
    # Отмена действий (Ctrl+Z, Ctrl+Shift+S) +
    # Горячие клавиши +
    # Авто заглавные +
    # Распознавание ссылок +
    # Кликабельные ссылки +
    # Смена курсора на ссылке +
    # Стиль оформления ссылки +
    # Изменение фона заголовка +
    # Динамический заголовок окна +
    # Поле подсказок +
    # Подсказки для кнопки "menu_bt_new" +
    # Эффект наведения для кнопки "menu_bt_new" +
    # Создание меню ~
    # Функционал кнопки "menu_bt_new" +
    # Кнопки стиля перенесены из style_container в menu_bar с использованием .place() +
    # Логирование координат и отступов кнопок стиля в menu_bar +
    # Обновление координат кнопок стиля (x=34, 61, 88, 115) +
    # Добавление названия ОС в начало логов +
    # Добавление версии кода в начало логов +
    # Кнопка пм-жирный +
    # Проверка символов перед и после курсора для кнопки пм-жирный +
    # Исправление ошибки TclError при отсутствии символов в выделении +
    # Кнопки пм-курсив, пм-подчёркивание, пм-зачёркивание +
    # Исправление конфликта стилей пм-жирный и пм-курсив через динамическое управление тегами +
    # Добавление копирования и вставки форматирования текста +
    # Добавление поддержки сохранения в .rtf и .txt с учётом форматирования +
    # Добавление парсера RTF для извлечения форматирования при открытии .rtf файлов +
    # Перемещение всех изображений в подкаталог _img\ +


import customtkinter as ctk
import tkinter as tk
import logging
import re
import webbrowser
from tkinter import messagebox, filedialog
import sys
import platform
from PIL import Image  # Для работы с изображениями в customtkinter
import os  # Для работы с путями файлов

# Версия кода
CODE_VERSION = "T-1.10"

# Путь к папке с изображениями
IMG_DIR = "_img"

# Для изменения цвета заголовка на Windows
if platform.system() == "Windows":
    import ctypes
    from ctypes import wintypes

# Настройка логирования (записываем в файл error.log)
logging.basicConfig(filename='error.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
logging.getLogger("PIL").setLevel(logging.WARNING)  # Отключаем DEBUG-логи от PIL
logging.debug("Логирование инициализировано")
logging.debug(f"Операционная система: {platform.system()}")
logging.debug(f"Версия кода: {CODE_VERSION}")

# Минимальный тест для tkinter
try:
    root = tk.Tk()
    root.destroy()
except Exception as e:
    logging.error(f"Ошибка при создании tkinter окна: {e}")
    raise

# Регулярное выражение для поиска URL (с флагом re.IGNORECASE для нечувствительности к регистру)
URL_PATTERN = re.compile(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', re.IGNORECASE)

# === Блок: Параметры окна ===
WINDOW_WIDTH = 600  # Ширина окна в пикселях
WINDOW_HEIGHT = 400  # Высота окна в пикселях
WINDOW_VERSION = ""  # Убрали номер версии из заголовка
WINDOW_TITLE_DEFAULT = "Новая запись"  # Начальный текст заголовка окна без версии
WINDOW_BORDER_WIDTH = 1  # Внутренний отступ окна (1 пиксель)

# === Блок: Цветовая тема (dark) ===
WINDOW_BG = "#363A3F"  # Цвет фона окна
TITLE_TEXT_COLOR = "#D1D1D1"  # Цвет текста заголовка (оставлен для возможного использования)
TEXT_AREA_TEXT_COLOR = "#D1D1D1"  # Цвет текста в текстовом поле

# === Блок: Параметры меню ===
MENU_BAR_HEIGHT = 34  # Высота меню в пикселях
MENU_BAR_IPADDING_TOP = 2  # Внешний отступ сверху (для дочерних элементов)
MENU_BAR_IPADDING_BOTTOM = 3  # Внешний отступ снизу (для дочерних элементов)
MENU_BAR_IPADDING_LEFT = 10  # Внешний отступ слева (для дочерних элементов)
MENU_BAR_IPADDING_RIGHT = 7  # Внешний отступ справа (для дочерних элементов)
MENU_BAR_BG = WINDOW_BG  # Цвет фона меню (совпадает с фоном окна)

# === Блок: Параметры кнопки в меню ===
MENU_BUTTON_HEIGHT = 24  # Высота кнопки
MENU_BUTTON_WIDTH = 24  # Ширина кнопки
MENU_BUTTON_BG = WINDOW_BG  # Цвет фона кнопки (совпадает с фоном окна)
MENU_BUTTON_CORNER_RADIUS = 1  # Радиус скругления углов кнопки
MENU_BUTTON_IPADDING_X = 0  # Внутренний отступ кнопки по горизонтали (слева и справа)
MENU_BUTTON_IPADDING_Y = 0  # Внутренний отступ кнопки по вертикали (сверху и снизу)

# === Блок: Параметры кнопок стиля шрифта ===
STYLE_BUTTON_WIDTH = 30  # Ширина кнопок стиля шрифта
STYLE_BUTTON_HEIGHT = 24  # Высота кнопок стиля шрифта
STYLE_BUTTON_SPACING_HEND = 1  # Расстояние между кнопками
STYLE_BUTTON_BOLD_X = MENU_BUTTON_WIDTH + MENU_BAR_IPADDING_LEFT  # Координата X для первой кнопки (34)
STYLE_BUTTON_ITALIC_X = STYLE_BUTTON_BOLD_X + STYLE_BUTTON_WIDTH + STYLE_BUTTON_SPACING_HEND - 2  # Координата X для второй кнопки (61)
STYLE_BUTTON_UNDER_X = STYLE_BUTTON_ITALIC_X + STYLE_BUTTON_WIDTH + STYLE_BUTTON_SPACING_HEND - 2  # Координата X для третьей кнопки (88)
STYLE_BUTTON_STRIKET_X = STYLE_BUTTON_UNDER_X + STYLE_BUTTON_WIDTH + STYLE_BUTTON_SPACING_HEND - 2  # Координата X для четвёртой кнопки (115)

# === Блок: Параметры текстового поля ===
TEXT_AREA_PADX_LEFT = 10  # Внешний отступ текстового поля слева
TEXT_AREA_PADX_RIGHT = 12  # Внешний отступ текстового поля справа
TEXT_AREA_PADY_TOP = 5  # Внешний отступ текстового поля сверху
TEXT_AREA_PADY_BOTTOM = 10  # Внешний отступ текстового поля снизу
TEXT_AREA_BG = "#363A3F"  # Цвет фона текстового поля (по умолчанию совпадает с WINDOW_BG)
TEXT_AREA_FONT_FAMILY = "Roboto"  # Шрифт по умолчанию
TEXT_AREA_FONT_SIZE = 13  # Размер шрифта по умолчанию
TEXT_AREA_LINE_SPACING = 3  # Межстрочное расстояние (в пикселях)

# Определяем шрифты для всех комбинаций начертаний
FONT_NORMAL = (TEXT_AREA_FONT_FAMILY, TEXT_AREA_FONT_SIZE)  # Обычный шрифт
FONT_BOLD = (TEXT_AREA_FONT_FAMILY, TEXT_AREA_FONT_SIZE, "bold")  # Жирный
FONT_ITALIC = (TEXT_AREA_FONT_FAMILY, TEXT_AREA_FONT_SIZE, "italic")  # Курсивный
FONT_BOLD_ITALIC = (TEXT_AREA_FONT_FAMILY, TEXT_AREA_FONT_SIZE, "bold italic")  # Жирный и курсивный

# === Блок: Параметры поля подсказок ===
HINT_BAR_HEIGHT = 30  # Высота поля подсказок в пикселях
HINT_BAR_BG = WINDOW_BG  # Цвет фона поля подсказок (совпадает с фоном окна)
HINT_BAR_FONT_FAMILY = "Montserrat SemiBold"  # Семейство шрифта для поля подсказок
HINT_BAR_TEXT_FONT_SIZE = 10  # Размер шрифта для текста подсказок
HINT_BAR_ICON_FONT_SIZE = HINT_BAR_TEXT_FONT_SIZE + 2  # Размер шрифта для символов ◧ и ◨ (на 4 больше текста)
HINT_BAR_TEXT_COLOR = "#757575"  # Цвет текста в поле подсказок
HINT_BAR_IPADX = 5  # Внутренние горизонтальные отступы в столбцах
HINT_BAR_LEFT_WIDTH = 0.6  # Ширина левого столбца (50%)
HINT_BAR_CENTER_WIDTH = 0.2  # Ширина центрального столбца (25%)
HINT_BAR_RIGHT_WIDTH = 0.2  # Ширина правого столбца (25%)

# === Блок: Параметры оформления ссылок ===
LINK_FG_COLOR = "#92A1B5"  # Цвет текста ссылок
LINK_UNDERLINE = False  # Подчёркивание ссылок
LINK_FONT_FAMILY = TEXT_AREA_FONT_FAMILY  # Шрифт ссылок (берём из TEXT_AREA_FONT_FAMILY, т.е. "Roboto")
LINK_FONT_SIZE = 11  # Размер шрифта ссылок
LINK_FONT_WEIGHT = "bold"  # Вес шрифта ссылок (жирный)

# Глобальная переменная для хранения форматирования при копировании
copied_tags = []

def main():
    try:
        # Устанавливаем тёмную тему для приложения
        ctk.set_appearance_mode("dark")

        root = ctk.CTk()
        root.configure(border_width=WINDOW_BORDER_WIDTH)
        root.configure(fg_color=WINDOW_BG)
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        root.title(WINDOW_TITLE_DEFAULT)

        # Изменяем цвет заголовка на Windows
        if platform.system() == "Windows":
            try:
                hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
                color_hex = WINDOW_BG.lstrip('#')
                color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
                color_ref = (color_rgb[2] << 16) + (color_rgb[1] << 8) + color_rgb[0]
                DWMWA_CAPTION_COLOR = 35
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_CAPTION_COLOR,
                    ctypes.byref(ctypes.c_int(color_ref)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except Exception as e:
                logging.error(f"Не удалось изменить цвет заголовка на Windows: {e}")

        # Создаём поле меню
        menu_bar = ctk.CTkFrame(
            root,
            height=MENU_BAR_HEIGHT,
            width=WINDOW_WIDTH,
            fg_color=MENU_BAR_BG,
            corner_radius=0
        )
        menu_bar.pack_propagate(False)
        menu_bar.place(x=0, y=0)

        # Переменная для отслеживания текущего файла
        current_file_path = [None]

        # Функция для проверки, пуст ли документ
        def is_document_empty():
            content = text_area.get("1.0", "end-1c").strip()
            return not content

        # Функция для проверки наличия форматирования в документе
        def has_formatting():
            # Проверяем наличие тегов форматирования в документе
            for tag in ("bold", "italic", "underline", "strikethrough"):
                if text_area.tag_ranges(tag):
                    return True
            return False

        # Функция для преобразования текста в RTF-формат
        def text_to_rtf():
            # Начало RTF-документа
            rtf_content = r"{\rtf1\ansi\deff0" + "\n"
            
            # Определяем шрифт
            rtf_content += r"{\fonttbl{\f0\fswiss\fcharset0 " + TEXT_AREA_FONT_FAMILY + ";}}\n"
            rtf_content += r"\fs" + str(TEXT_AREA_FONT_SIZE * 2) + "\n"  # Размер шрифта в RTF (в полупунктах)
            
            # Получаем весь текст
            text = text_area.get("1.0", "end-1c")
            if not text:
                return r"{\rtf1\ansi\deff0}"

            current_pos = "1.0"
            while text_area.compare(current_pos, "<", "end-1c"):
                # Получаем теги в текущей позиции
                tags = text_area.tag_names(current_pos)
                
                # Открываем форматирование
                formatting = ""
                if "bold" in tags:
                    formatting += r"\b"
                if "italic" in tags:
                    formatting += r"\i"
                if "underline" in tags:
                    formatting += r"\ul"
                if "strikethrough" in tags:
                    formatting += r"\strike"
                
                # Добавляем пробел после управляющих кодов, если есть форматирование
                if formatting:
                    formatting += " "
                
                # Получаем следующий символ
                char = text_area.get(current_pos, f"{current_pos}+1c")
                
                # Экранируем специальные символы в RTF
                if char == "\\":
                    char = r"\\"
                elif char == "{":
                    char = r"\{"
                elif char == "}":
                    char = r"\}"
                elif char == "\n":
                    char = r"\par "  # Новая строка в RTF
                elif ord(char) > 127:  # Для символов Unicode
                    char = r"\u" + str(ord(char)) + "?"
                
                # Добавляем форматированный символ
                rtf_content += formatting + char
                
                # Закрываем форматирование
                closing = ""
                if "strikethrough" in tags:
                    closing += r"\strike0"
                if "underline" in tags:
                    closing += r"\ulnone"
                if "italic" in tags:
                    closing += r"\i0"
                if "bold" in tags:
                    closing += r"\b0"
                
                # Добавляем пробел после закрытия форматирования, если оно есть
                if closing:
                    closing += " "
                
                rtf_content += closing
                
                current_pos = f"{current_pos}+1c"

            # Завершаем RTF-документ
            rtf_content += "}"
            return rtf_content

        # Функция для парсинга RTF и извлечения текста с форматированием
        def rtf_to_text(rtf_content):
            # Очищаем текстовое поле перед загрузкой
            text_area.delete("1.0", "end")
            
            # Состояние форматирования
            bold = False
            italic = False
            underline = False
            strikethrough = False
            in_group = 0  # Уровень вложенности групп { }
            skip_until_group_level = -1  # Уровень группы, до которого нужно пропускать
            inside_fonttbl = False  # Флаг, указывающий, что мы внутри группы \fonttbl
            i = 0  # Индекс символа в RTF-файле
            
            plain_text = []  # Список для хранения текста
            formatting_positions = []  # Список для хранения форматирования каждого символа

            while i < len(rtf_content):
                char = rtf_content[i]
                logging.debug(f"Обрабатываем символ [{i}]: {char!r}, in_group={in_group}, skip_until_group_level={skip_until_group_level}, inside_fonttbl={inside_fonttbl}")

                # Пропускаем содержимое групп, если skip_until_group_level активный
                if skip_until_group_level >= 0:
                    if char == "{":
                        in_group += 1
                        logging.debug(f"Увеличиваем вложенность групп: in_group={in_group}")
                    elif char == "}":
                        in_group -= 1
                        logging.debug(f"Уменьшаем вложенность групп: in_group={in_group}")
                        if in_group <= skip_until_group_level:
                            skip_until_group_level = -1  # Прекращаем пропуск
                            inside_fonttbl = False  # Выходим из группы \fonttbl
                            logging.debug("Прекращаем пропуск группы (fonttbl/colortbl)")
                    i += 1
                    continue

                if char == "{":  # Начало группы
                    in_group += 1
                    logging.debug(f"Начало группы, in_group={in_group}")
                    i += 1
                    # Проверяем, начинается ли группа с управляющего кода
                    if i < len(rtf_content) and rtf_content[i] == "\\":
                        i += 1
                        control_word = ""
                        while i < len(rtf_content) and (rtf_content[i].isalnum() or rtf_content[i] == '-'):
                            control_word += rtf_content[i]
                            i += 1
                        logging.debug(f"Обнаружен управляющий код внутри группы: \\{control_word}")
                        # Пропускаем пробел после управляющего кода, если он есть
                        if i < len(rtf_content) and rtf_content[i] == " ":
                            i += 1
                            logging.debug(f"Пропущен пробел после управляющего кода: \\{control_word}")
                        # Обрабатываем известные группы
                        if control_word in ("fonttbl", "colortbl"):
                            skip_until_group_level = in_group - 1  # Пропускаем до конца текущей группы
                            inside_fonttbl = (control_word == "fonttbl")  # Отмечаем, что мы внутри \fonttbl
                            logging.debug(f"Начало группы {control_word}, пропускаем до уровня {skip_until_group_level}")
                            continue
                        elif control_word.startswith("rtf") or control_word in ("ansi", "deff0"):
                            # Игнорируем управляющие коды верхнего уровня (\rtf, \ansi, \deff0)
                            logging.debug(f"Игнорируем управляющий код верхнего уровня: \\{control_word}")
                            continue
                    continue  # Продолжаем парсинг, не возвращаясь назад

                if char == "}":  # Конец группы
                    in_group -= 1
                    logging.debug(f"Конец группы, in_group={in_group}")
                    i += 1
                    continue

                if char == "\\":  # Управляющий код
                    i += 1
                    # Извлекаем управляющий код
                    control_word = ""
                    while i < len(rtf_content) and (rtf_content[i].isalnum() or rtf_content[i] == '-'):
                        control_word += rtf_content[i]
                        i += 1
                    
                    # Пропускаем пробел после управляющего кода, если он есть
                    if i < len(rtf_content) and rtf_content[i] == " ":
                        i += 1
                        logging.debug(f"Пропущен пробел после управляющего кода: \\{control_word}")
                    
                    # Если мы внутри \fonttbl, пропускаем все управляющие коды
                    if inside_fonttbl:
                        logging.debug(f"Игнорируем управляющий код внутри fonttbl: \\{control_word}")
                        continue
                    
                    # Обрабатываем управляющие коды
                    logging.debug(f"Обрабатываем управляющий код: \\{control_word}")
                    if control_word == "b":
                        bold = True
                    elif control_word == "b0":
                        bold = False
                    elif control_word == "i":
                        italic = True
                    elif control_word == "i0":
                        italic = False
                    elif control_word == "ul":
                        underline = True
                    elif control_word == "ulnone":
                        underline = False
                    elif control_word == "strike":
                        strikethrough = True
                    elif control_word == "strike0":
                        strikethrough = False
                    elif control_word == "par":
                        plain_text.append("\n")
                        formatting_positions.append({"bold": bold, "italic": italic, "underline": underline, "strikethrough": strikethrough})
                        logging.debug("Добавлен перенос строки: \\par")
                    elif control_word.startswith("u"):  # Unicode символ
                        # Извлекаем числовое значение Unicode (например, \u9675)
                        unicode_value = int(control_word[1:])
                        char = chr(unicode_value)
                        plain_text.append(char)
                        formatting_positions.append({"bold": bold, "italic": italic, "underline": underline, "strikethrough": strikethrough})
                        logging.debug(f"Добавлен Unicode-символ: {char}")
                        # Пропускаем следующий символ (обычно ?)
                        if i < len(rtf_content) and rtf_content[i] in " ?":
                            i += 1
                    elif control_word.startswith("f") and not control_word.startswith("fs"):  # Игнорируем \f0, \f1 и т.д.
                        logging.debug(f"Игнорируем управляющий код (шрифт): \\{control_word}")
                        continue
                    elif control_word.startswith("fs"):  # Размер шрифта (игнорируем)
                        logging.debug(f"Игнорируем управляющий код (размер шрифта): \\{control_word}")
                        continue
                    else:
                        logging.debug(f"Необработанный управляющий код: \\{control_word}")
                    continue

                # Обрабатываем экранированные символы
                if char == "\\" and i + 1 < len(rtf_content):
                    next_char = rtf_content[i + 1]
                    if next_char in "\\{}":
                        plain_text.append(next_char)
                        formatting_positions.append({"bold": bold, "italic": italic, "underline": underline, "strikethrough": strikethrough})
                        logging.debug(f"Добавлен экранированный символ: {next_char}")
                        i += 2
                        continue

                # Добавляем обычный символ
                if char not in "\r\n":  # Игнорируем \r\n (лишние переносы строк)
                    plain_text.append(char)
                    formatting_positions.append({"bold": bold, "italic": italic, "underline": underline, "strikethrough": strikethrough})
                    logging.debug(f"Добавлен обычный символ: {char!r}")
                i += 1

            # Логируем итоговый текст перед вставкой
            final_text = "".join(plain_text)
            logging.debug(f"Итоговый текст перед вставкой: {final_text!r}")

            # Вставляем текст в tk.Text
            text_area.insert("1.0", final_text)

            # Применяем форматирование
            for pos, fmt in enumerate(formatting_positions):
                char_start = f"1.0 + {pos} chars"
                char_end = f"1.0 + {pos + 1} chars"
                if fmt["bold"]:
                    text_area.tag_add("bold", char_start, char_end)
                if fmt["italic"]:
                    text_area.tag_add("italic", char_start, char_end)
                if fmt["underline"]:
                    text_area.tag_add("underline", char_start, char_end)
                if fmt["strikethrough"]:
                    text_area.tag_add("strikethrough", char_start, char_end)
                # Применяем шрифт
                apply_font_style(char_start, char_end)

        # Функция для обновления заголовка окна
        def update_window_title():
            try:
                if current_file_path[0]:
                    file_name = os.path.basename(current_file_path[0])
                    file_name_without_ext = os.path.splitext(file_name)[0]
                    new_title = f"{file_name_without_ext}"
                else:
                    content = text_area.get("1.0", "end-1c").rstrip()
                    if content:
                        words = content.split()[:3]
                        first_three_words = " ".join(words)
                        if len(first_three_words) <= 30:
                            title_text = first_three_words
                        else:
                            title_text = content[:30]
                        new_title = f"{title_text}"
                    else:
                        new_title = WINDOW_TITLE_DEFAULT
                root.title(new_title)
            except Exception as e:
                logging.error(f"Ошибка при обновления заголовка окна: {e}")

        # Функция для создания новой записи (очистка текстового поля)
        def new_note(event=None):
            try:
                text_area.delete("1.0", "end")
                current_file_path[0] = None
                highlight_links()
                update_window_title()
                update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return True
            except Exception as e:
                logging.error(f"Ошибка при создании новой записи: {e}")
                return False

        # Функция для открытия файла и загрузки текста
        def open_file(event=None):
            try:
                file_path = filedialog.askopenfilename(
                    filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("RTF files", "*.rtf")]  # "All files" теперь первый
                )
                if file_path:
                    file_ext = os.path.splitext(file_path)[1].lower()
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    if file_ext == ".rtf":
                        # Парсим RTF и извлекаем форматирование
                        rtf_to_text(content)
                    else:
                        # Для .txt загружаем текст как есть
                        text_area.delete("1.0", "end")
                        text_area.insert("1.0", content)

                    current_file_path[0] = file_path
                    highlight_links()
                    update_window_title()
                    update_style_buttons()  # Обновляем иконки всех кнопок стиля
                    return True
                return False
            except Exception as e:
                logging.error(f"Ошибка при открытии файла: {e}")
                return False

        # Функция для сохранения текста в текущий файл
        def save_text(event=None):
            try:
                if not current_file_path[0]:
                    return save_as(event)
                
                # Определяем формат файла
                file_ext = os.path.splitext(current_file_path[0])[1].lower()
                
                if file_ext == ".rtf":
                    # Сохраняем в RTF-формате
                    rtf_content = text_to_rtf()
                    with open(current_file_path[0], "w", encoding="utf-8") as file:
                        file.write(rtf_content)
                else:
                    # Сохраняем в текстовом формате (без форматирования)
                    content = text_area.get("1.0", "end-1c")
                    with open(current_file_path[0], "w", encoding="utf-8") as file:
                        file.write(content)
                
                update_window_title()
                return True
            except Exception as e:
                logging.error(f"Ошибка при сохранении текста: {e}")
                return False

        # Функция "Сохранить как"
        def save_as(event=None):
            try:
                initial_file = None
                if not current_file_path[0]:
                    content = text_area.get("1.0", "end-1c").rstrip()
                    if content:
                        initial_file = content[:30].replace(" ", "_")
                    else:
                        initial_file = "заметка"
                else:
                    initial_file = os.path.basename(current_file_path[0])

                # Проверяем наличие форматирования
                if has_formatting():
                    filetypes = [("RTF files", "*.rtf")]
                    default_extension = ".rtf"
                else:
                    filetypes = [("RTF files", "*.rtf"), ("Text files", "*.txt")]
                    default_extension = ".rtf"  # По умолчанию предлагаем RTF

                file_path = filedialog.asksaveasfilename(
                    defaultextension=default_extension,
                    filetypes=filetypes,
                    initialfile=initial_file
                )
                if file_path:
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext == ".rtf":
                        # Сохраняем в RTF-формате
                        rtf_content = text_to_rtf()
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(rtf_content)
                    else:
                        # Сохраняем в текстовом формате (без форматирования)
                        content = text_area.get("1.0", "end-1c")
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(content)
                    
                    current_file_path[0] = file_path
                    update_window_title()
                    return True
                return False
            except Exception as e:
                logging.error(f"Ошибка при сохранении текста как: {e}")
                return False

        # Функции для копирования и вставки с сохранением форматирования
        def copy_text(event):
            global copied_tags
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    
                    # Копируем текст в буфер обмена
                    text_area.event_generate("<<Copy>>")
                    
                    # Сохраняем теги форматирования для каждого символа в выделенном диапазоне
                    copied_tags = []
                    current_pos = sel_start
                    while text_area.compare(current_pos, "<", sel_end):
                        tags = [tag for tag in text_area.tag_names(current_pos) 
                                if tag in ("bold", "italic", "underline", "strikethrough")]
                        copied_tags.append(tags)
                        current_pos = f"{current_pos}+1c"
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при копировании текста: {e}")
                return "break"

        def paste_text(event):
            global copied_tags
            try:
                # Получаем позицию курсора перед вставкой
                insert_pos = text_area.index(tk.INSERT)
                
                # Выполняем стандартную вставку текста
                text_area.event_generate("<<Paste>>")
                
                # Если есть сохранённые теги форматирования, применяем их к вставленному тексту
                if copied_tags:
                    # Определяем диапазон вставленного текста
                    pasted_text = root.clipboard_get()
                    pasted_length = len(pasted_text)
                    
                    # Применяем теги к каждому символу вставленного текста
                    for i, tags in enumerate(copied_tags):
                        if i < pasted_length:  # Убеждаемся, что не выходим за длину вставленного текста
                            char_start = f"{insert_pos}+{i}c"
                            char_end = f"{insert_pos}+{i+1}c"
                            for tag in tags:
                                text_area.tag_add(tag, char_start, char_end)
                            # Обновляем шрифт для текущего символа
                            apply_font_style(char_start, char_end)
                
                highlight_links()
                update_window_title()
                update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при вставке текста: {e}")
                return "break"

        def cut_text(event):
            global copied_tags
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    
                    # Сохраняем теги форматирования перед вырезанием
                    copied_tags = []
                    current_pos = sel_start
                    while text_area.compare(current_pos, "<", sel_end):
                        tags = [tag for tag in text_area.tag_names(current_pos) 
                                if tag in ("bold", "italic", "underline", "strikethrough")]
                        copied_tags.append(tags)
                        current_pos = f"{current_pos}+1c"
                    
                    # Выполняем стандартное вырезание
                    text_area.event_generate("<<Cut>>")
                    highlight_links()
                    update_window_title()
                    update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при вырезании текста: {e}")
                return "break"

        def select_all(event):
            try:
                text_area.tag_add("sel", "1.0", "end-1c")
                update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при выделении всего текста: {e}")
                return "break"

        def undo(event):
            try:
                text_area.event_generate("<<Undo>>")
                highlight_links()
                update_window_title()
                update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при отмене действия: {e}")
                return "break"

        def redo(event):
            try:
                text_area.event_generate("<<Redo>>")
                highlight_links()
                update_window_title()
                update_style_buttons()  # Обновляем иконки всех кнопок стиля
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при повторе действия: {e}")
                return "break"

        # Функция для обработки клика ЛКМ на кнопке "menu_bt_new"
        def handle_new_button_click(event=None):
            if is_document_empty():
                new_note()
            else:
                if current_file_path[0]:
                    if save_text():
                        new_note()
                else:
                    if not save_as():
                        new_note()
            update_style_buttons()  # Обновляем иконки всех кнопок стиля
            return "break"

        # Загружаем иконку btn_new.png
        try:
            btn_new_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_new.png"),
                size=(MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)  # Теперь 24x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_new.png: {e}")
            btn_new_icon = None

        # Загружаем иконку btn_new_hover.png
        try:
            btn_new_hover_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_new_hover.png"),
                size=(MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)  # Теперь 24x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_new_hover.png: {e}")
            btn_new_hover_icon = None

        # Функции для управления подсказками и эффектом наведения
        def show_new_button_hint(event=None):
            # hint_label_left.configure(text="ЛКМ → Новая заметка | ПКМ → Открыть заметку")
            hint_label_left.configure(state="normal")  # Разрешаем редактирование
            hint_label_left.delete("1.0", "end")
            hint_label_left.insert("1.0", "◨", ("icon",))
            hint_label_left.insert("end", " → Новая заметка ", ("text",))
            hint_label_left.insert("end", "| ", ("text",))
            hint_label_left.insert("end", "◧", ("icon",))
            hint_label_left.insert("end", " → Открыть заметку", ("text",))
            hint_label_left.configure(state="disabled")  # Запрещаем редактирование
            if btn_new_hover_icon:
                menu_bt_new.configure(image=btn_new_hover_icon)

        def hide_new_button_hint(event=None):
            hint_label_left.configure(state="normal")  # Разрешаем редактирование
            hint_label_left.delete("1.0", "end")
            hint_label_left.configure(state="disabled")  # Запрещаем редактирование
            if btn_new_icon:
                menu_bt_new.configure(image=btn_new_icon)

        # Добавляем первую кнопку в меню (menu_bt_new)
        menu_bt_new = ctk.CTkButton(
            menu_bar,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            text="",
            fg_color=MENU_BUTTON_BG,
            hover=True,
            hover_color=MENU_BUTTON_BG,
            corner_radius=MENU_BUTTON_CORNER_RADIUS,
            image=btn_new_icon,
            command=handle_new_button_click
        )
        menu_bt_new.bind("<Button-3>", open_file)
        menu_bt_new.bind("<Enter>", show_new_button_hint)
        menu_bt_new.bind("<Leave>", hide_new_button_hint)
        menu_bt_new.pack(
            side="left",
            padx=(MENU_BAR_IPADDING_LEFT, 0),
            pady=(MENU_BAR_IPADDING_TOP, MENU_BAR_IPADDING_BOTTOM),
            ipadx=MENU_BUTTON_IPADDING_X,
            ipady=MENU_BUTTON_IPADDING_Y
        )

        # Загружаем иконки для кнопок стиля шрифта
        try:
            btn_bold_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_Bold.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_Bold.png: {e}")
            btn_bold_icon = None

        try:
            btn_bold_hover_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_Bold_hover.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_Bold_hover.png: {e}")
            btn_bold_hover_icon = None

        try:
            btn_italic_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_italic.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_italic.png: {e}")
            btn_italic_icon = None

        try:
            btn_italic_hover_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_italic_hover.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_italic_hover.png: {e}")
            btn_italic_hover_icon = None

        try:
            btn_under_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_under.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_under.png: {e}")
            btn_under_icon = None

        try:
            btn_under_hover_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_under_hover.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_under_hover.png: {e}")
            btn_under_hover_icon = None

        try:
            btn_striket_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_striket.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_striket.png: {e}")
            btn_striket_icon = None

        try:
            btn_striket_hover_icon = ctk.CTkImage(
                light_image=Image.open(f"{IMG_DIR}/btn_striket_hover.png"),
                size=(STYLE_BUTTON_WIDTH, STYLE_BUTTON_HEIGHT)  # Теперь 30x24
            )
        except Exception as e:
            logging.error(f"Не удалось загрузить иконку btn_striket_hover.png: {e}")
            btn_striket_hover_icon = None

        # Функция для проверки наличия тега в заданном диапазоне
        def has_tag(tag, start, end):
            ranges = text_area.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                tag_start = ranges[i]
                tag_end = ranges[i + 1]
                if (text_area.compare(start, ">=", tag_start) and text_area.compare(start, "<", tag_end)) or \
                   (text_area.compare(end, ">", tag_start) and text_area.compare(end, "<=", tag_end)):
                    return True
            return False

        # Функция для определения текущих начертаний и применения правильного шрифта
        def apply_font_style(start, end):
            # Определяем, какие стили (bold, italic) применены к диапазону
            has_bold = has_tag("bold", start, end)
            has_italic = has_tag("italic", start, end)

            # Удаляем старые теги начертания
            text_area.tag_remove("font_normal", start, end)
            text_area.tag_remove("font_bold", start, end)
            text_area.tag_remove("font_italic", start, end)
            text_area.tag_remove("font_bold_italic", start, end)

            # Применяем правильный тег шрифта в зависимости от комбинации
            if has_bold and has_italic:
                text_area.tag_add("font_bold_italic", start, end)
            elif has_bold:
                text_area.tag_add("font_bold", start, end)
            elif has_italic:
                text_area.tag_add("font_italic", start, end)
            else:
                text_area.tag_add("font_normal", start, end)

        # Функции для переключения стилей
        def toggle_bold(event=None):
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    if has_tag("bold", sel_start, sel_end):
                        text_area.tag_remove("bold", sel_start, sel_end)
                    else:
                        text_area.tag_add("bold", sel_start, sel_end)
                    # Обновляем шрифт для всего выделенного диапазона
                    apply_font_style(sel_start, sel_end)
                    update_style_buttons()
            except tk.TclError:
                pass

        def toggle_italic(event=None):
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    if has_tag("italic", sel_start, sel_end):
                        text_area.tag_remove("italic", sel_start, sel_end)
                    else:
                        text_area.tag_add("italic", sel_start, sel_end)
                    # Обновляем шрифт для всего выделенного диапазона
                    apply_font_style(sel_start, sel_end)
                    update_style_buttons()
            except tk.TclError:
                pass

        def toggle_underline(event=None):
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    if has_tag("underline", sel_start, sel_end):
                        text_area.tag_remove("underline", sel_start, sel_end)
                        menu_bt_under.configure(image=btn_under_icon)
                    else:
                        text_area.tag_add("underline", sel_start, sel_end)
                        menu_bt_under.configure(image=btn_under_hover_icon)
            except tk.TclError:
                pass

        def toggle_strikethrough(event=None):
            try:
                if text_area.tag_ranges("sel"):
                    sel_start = text_area.index("sel.first")
                    sel_end = text_area.index("sel.last")
                    if has_tag("strikethrough", sel_start, sel_end):
                        text_area.tag_remove("strikethrough", sel_start, sel_end)
                        menu_bt_striket.configure(image=btn_striket_icon)
                    else:
                        text_area.tag_add("strikethrough", sel_start, sel_end)
                        menu_bt_striket.configure(image=btn_striket_hover_icon)
            except tk.TclError:
                pass

        # Функции для обновления иконок кнопок стиля
        def update_bold_button_icon():
            if text_area.tag_ranges("sel"):
                sel_start = text_area.index("sel.first")
                sel_end = text_area.index("sel.last")
                if has_tag("bold", sel_start, sel_end):
                    menu_bt_bold.configure(image=btn_bold_hover_icon)
                else:
                    menu_bt_bold.configure(image=btn_bold_icon)
            else:
                cursor_pos = text_area.index(tk.INSERT)
                if "bold" in text_area.tag_names(cursor_pos):
                    menu_bt_bold.configure(image=btn_bold_hover_icon)
                    return
                before_pos = f"{cursor_pos}-1c"
                after_pos = f"{cursor_pos}+1c"
                has_char_before = text_area.compare(before_pos, ">=", "1.0")
                has_char_after = text_area.compare(after_pos, "<", "end-1c")
                if has_char_before and has_char_after:
                    before_has_bold = has_tag("bold", before_pos, before_pos)
                    after_has_bold = has_tag("bold", after_pos, after_pos)
                    if before_has_bold and after_has_bold:
                        menu_bt_bold.configure(image=btn_bold_hover_icon)
                        return
                menu_bt_bold.configure(image=btn_bold_icon)

        def update_italic_button_icon():
            if text_area.tag_ranges("sel"):
                sel_start = text_area.index("sel.first")
                sel_end = text_area.index("sel.last")
                if has_tag("italic", sel_start, sel_end):
                    menu_bt_italic.configure(image=btn_italic_hover_icon)
                else:
                    menu_bt_italic.configure(image=btn_italic_icon)
            else:
                cursor_pos = text_area.index(tk.INSERT)
                if "italic" in text_area.tag_names(cursor_pos):
                    menu_bt_italic.configure(image=btn_italic_hover_icon)
                    return
                before_pos = f"{cursor_pos}-1c"
                after_pos = f"{cursor_pos}+1c"
                has_char_before = text_area.compare(before_pos, ">=", "1.0")
                has_char_after = text_area.compare(after_pos, "<", "end-1c")
                if has_char_before and has_char_after:
                    before_has_italic = has_tag("italic", before_pos, before_pos)
                    after_has_italic = has_tag("italic", after_pos, after_pos)
                    if before_has_italic and after_has_italic:
                        menu_bt_italic.configure(image=btn_italic_hover_icon)
                        return
                menu_bt_italic.configure(image=btn_italic_icon)

        def update_underline_button_icon():
            if text_area.tag_ranges("sel"):
                sel_start = text_area.index("sel.first")
                sel_end = text_area.index("sel.last")
                if has_tag("underline", sel_start, sel_end):
                    menu_bt_under.configure(image=btn_under_hover_icon)
                else:
                    menu_bt_under.configure(image=btn_under_icon)
            else:
                cursor_pos = text_area.index(tk.INSERT)
                if "underline" in text_area.tag_names(cursor_pos):
                    menu_bt_under.configure(image=btn_under_hover_icon)
                    return
                before_pos = f"{cursor_pos}-1c"
                after_pos = f"{cursor_pos}+1c"
                has_char_before = text_area.compare(before_pos, ">=", "1.0")
                has_char_after = text_area.compare(after_pos, "<", "end-1c")
                if has_char_before and has_char_after:
                    before_has_underline = has_tag("underline", before_pos, before_pos)
                    after_has_underline = has_tag("underline", after_pos, after_pos)
                    if before_has_underline and after_has_underline:
                        menu_bt_under.configure(image=btn_under_hover_icon)
                        return
                menu_bt_under.configure(image=btn_under_icon)

        def update_strikethrough_button_icon():
            if text_area.tag_ranges("sel"):
                sel_start = text_area.index("sel.first")
                sel_end = text_area.index("sel.last")
                if has_tag("strikethrough", sel_start, sel_end):
                    menu_bt_striket.configure(image=btn_striket_hover_icon)
                else:
                    menu_bt_striket.configure(image=btn_striket_icon)
            else:
                cursor_pos = text_area.index(tk.INSERT)
                if "strikethrough" in text_area.tag_names(cursor_pos):
                    menu_bt_striket.configure(image=btn_striket_hover_icon)
                    return
                before_pos = f"{cursor_pos}-1c"
                after_pos = f"{cursor_pos}+1c"
                has_char_before = text_area.compare(before_pos, ">=", "1.0")
                has_char_after = text_area.compare(after_pos, "<", "end-1c")
                if has_char_before and has_char_after:
                    before_has_strikethrough = has_tag("strikethrough", before_pos, before_pos)
                    after_has_strikethrough = has_tag("strikethrough", after_pos, after_pos)
                    if before_has_strikethrough and after_has_strikethrough:
                        menu_bt_striket.configure(image=btn_striket_hover_icon)
                        return
                menu_bt_striket.configure(image=btn_striket_icon)

        # Функция для обновления всех иконок кнопок стиля
        def update_style_buttons(event=None):
            update_bold_button_icon()
            update_italic_button_icon()
            update_underline_button_icon()
            update_strikethrough_button_icon()

        # Добавляем кнопки стиля шрифта в menu_bar с использованием .place()
        menu_bt_bold = ctk.CTkButton(
            menu_bar,
            width=STYLE_BUTTON_WIDTH,
            height=STYLE_BUTTON_HEIGHT,
            text="",
            fg_color=MENU_BUTTON_BG,
            hover=False,
            corner_radius=MENU_BUTTON_CORNER_RADIUS,
            image=btn_bold_icon,
            command=toggle_bold,
            border_spacing=0
        )
        menu_bt_bold.place(x=STYLE_BUTTON_BOLD_X, y=MENU_BAR_IPADDING_TOP)

        menu_bt_italic = ctk.CTkButton(
            menu_bar,
            width=STYLE_BUTTON_WIDTH,
            height=STYLE_BUTTON_HEIGHT,
            text="",
            fg_color=MENU_BUTTON_BG,
            hover=False,
            corner_radius=MENU_BUTTON_CORNER_RADIUS,
            image=btn_italic_icon,
            command=toggle_italic,
            border_spacing=0
        )
        menu_bt_italic.place(x=STYLE_BUTTON_ITALIC_X, y=MENU_BAR_IPADDING_TOP)

        menu_bt_under = ctk.CTkButton(
            menu_bar,
            width=STYLE_BUTTON_WIDTH,
            height=STYLE_BUTTON_HEIGHT,
            text="",
            fg_color=MENU_BUTTON_BG,
            hover=False,
            corner_radius=MENU_BUTTON_CORNER_RADIUS,
            image=btn_under_icon,
            command=toggle_underline,
            border_spacing=0
        )
        menu_bt_under.place(x=STYLE_BUTTON_UNDER_X, y=MENU_BAR_IPADDING_TOP)

        menu_bt_striket = ctk.CTkButton(
            menu_bar,
            width=STYLE_BUTTON_WIDTH,
            height=STYLE_BUTTON_HEIGHT,
            text="",
            fg_color=MENU_BUTTON_BG,
            hover=False,
            corner_radius=MENU_BUTTON_CORNER_RADIUS,
            image=btn_striket_icon,
            command=toggle_strikethrough,
            border_spacing=0
        )
        menu_bt_striket.place(x=STYLE_BUTTON_STRIKET_X, y=MENU_BAR_IPADDING_TOP)

        # Функция для обновления ширины меню при изменении размера окна
        def update_menu_bar_width(event):
            menu_bar.configure(width=root.winfo_width())
            hint_bar.configure(width=root.winfo_width())
            hint_y = root.winfo_height() - WINDOW_BORDER_WIDTH
            hint_bar.place(
                x=WINDOW_BORDER_WIDTH, 
                y=hint_y,
                relwidth=(root.winfo_width() - 2 * WINDOW_BORDER_WIDTH) / root.winfo_width(),
                anchor="sw"
            )

        root.bind("<Configure>", update_menu_bar_width)

        def on_closing():
            try:
                for after_id in root.tk.eval('after info').split():
                    root.after_cancel(after_id)
            except Exception as e:
                logging.error(f"Ошибка при отмене after-событий: {e}")
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Общий обработчик для событий <Control-Key>
        def handle_control_key(event):
            keycode = event.keycode
            if keycode == 90:  # Z
                if event.state & 0x0001:
                    return redo(event)
                else:
                    return undo(event)
            elif keycode == 83:  # S
                if event.state & 0x0001:
                    return save_as(event)
                else:
                    return save_text(event)
            elif keycode == 67:  # Ctrl+C
                return copy_text(event)
            elif keycode == 86:  # Ctrl+V
                return paste_text(event)
            elif keycode == 88:  # Ctrl+X
                return cut_text(event)
            elif keycode == 65:  # Ctrl+A
                return select_all(event)
            elif keycode == 78:  # Ctrl+N
                return new_note(event)
            elif keycode == 79:  # Ctrl+O
                return open_file(event)
            return "break"

        # Поле для ввода текста (используем tk.Text)
        text_area = tk.Text(
            root,
            bg=TEXT_AREA_BG,
            fg=TEXT_AREA_TEXT_COLOR,
            wrap="word",
            font=FONT_NORMAL,  # Устанавливаем обычный шрифт по умолчанию
            borderwidth=0,
            highlightthickness=0,
            spacing1=TEXT_AREA_LINE_SPACING,
            insertbackground=TEXT_AREA_TEXT_COLOR,
            cursor="xterm",
            undo=True
        )
        text_area.place(
            x=0, 
            y=MENU_BAR_HEIGHT,
            relwidth=1.0,
            relheight=1.0,
            anchor="nw"
        )
        text_area.configure(
            padx=TEXT_AREA_PADX_LEFT,
            pady=TEXT_AREA_PADY_TOP
        )
        text_area.place_configure(
            x=TEXT_AREA_PADX_LEFT,
            y=MENU_BAR_HEIGHT + TEXT_AREA_PADY_TOP,
            relwidth=1.0 - (TEXT_AREA_PADX_LEFT + TEXT_AREA_PADX_RIGHT) / WINDOW_WIDTH,
            relheight=1.0 - (MENU_BAR_HEIGHT + TEXT_AREA_PADY_TOP + TEXT_AREA_PADY_BOTTOM + HINT_BAR_HEIGHT) / WINDOW_HEIGHT
        )

        # Настройка тегов для шрифтов (комбинации начертаний)
        text_area.tag_configure("font_normal", font=FONT_NORMAL)
        text_area.tag_configure("font_bold", font=FONT_BOLD)
        text_area.tag_configure("font_italic", font=FONT_ITALIC)
        text_area.tag_configure("font_bold_italic", font=FONT_BOLD_ITALIC)

        # Настройка тегов для стилей underline и strikethrough
        text_area.tag_configure("underline", underline=True)
        text_area.tag_configure("strikethrough", overstrike=True)

        # Создаём поле подсказок
        hint_bar = ctk.CTkFrame(
            root,
            height=HINT_BAR_HEIGHT,
            width=WINDOW_WIDTH,
            fg_color=HINT_BAR_BG,
            corner_radius=0
        )
        hint_bar.pack_propagate(False)
        hint_bar.place(
            x=WINDOW_BORDER_WIDTH, 
            y=WINDOW_HEIGHT - WINDOW_BORDER_WIDTH,
            relwidth=(WINDOW_WIDTH - 2 * WINDOW_BORDER_WIDTH) / WINDOW_WIDTH,
            anchor="sw"
        )

        # Создаём три столбца
        hint_label_left = tk.Text(
            hint_bar,
            height=1,
            bg=HINT_BAR_BG,
            fg=HINT_BAR_TEXT_COLOR,
            font=(HINT_BAR_FONT_FAMILY, HINT_BAR_TEXT_FONT_SIZE, "normal"),
            borderwidth=0,
            highlightthickness=0,
            wrap="none",
            state="disabled"  # Запрещаем редактирование
        )
        hint_label_left.place(relx=0, rely=0.5, relwidth=HINT_BAR_LEFT_WIDTH, anchor="w")
        hint_label_left.configure(padx=HINT_BAR_IPADX)

        # Настройка тегов для разных размеров шрифтов
        hint_label_left.tag_configure("icon", font=(HINT_BAR_FONT_FAMILY, HINT_BAR_ICON_FONT_SIZE, "normal"))
        hint_label_left.tag_configure("text", font=(HINT_BAR_FONT_FAMILY, HINT_BAR_TEXT_FONT_SIZE, "normal"))

        hint_label_center = ctk.CTkLabel(
            hint_bar,
            text="",
            font=(HINT_BAR_FONT_FAMILY, HINT_BAR_TEXT_FONT_SIZE, "normal"),
            text_color=HINT_BAR_TEXT_COLOR,
            anchor="center"
        )
        hint_label_center.place(relx=HINT_BAR_LEFT_WIDTH, rely=0.5, relwidth=HINT_BAR_CENTER_WIDTH, anchor="w")
        hint_label_center.configure(padx=HINT_BAR_IPADX)

        hint_label_right = ctk.CTkLabel(
            hint_bar,
            text=CODE_VERSION,
            font=(HINT_BAR_FONT_FAMILY, HINT_BAR_TEXT_FONT_SIZE, "normal"),
            text_color=HINT_BAR_TEXT_COLOR,
            anchor="center"
        )
        hint_label_right.place(relx=HINT_BAR_LEFT_WIDTH + HINT_BAR_CENTER_WIDTH, rely=0.5, relwidth=HINT_BAR_RIGHT_WIDTH, anchor="w")
        hint_label_right.configure(padx=HINT_BAR_IPADX)

        # Настройка тега для ссылок
        text_area.tag_configure(
            "hyperlink",
            foreground=LINK_FG_COLOR,
            underline=LINK_UNDERLINE,
            font=(LINK_FONT_FAMILY, LINK_FONT_SIZE, LINK_FONT_WEIGHT)
        )

        # Функция для подсветки и форматирования ссылок
        def highlight_links(event=None):
            text_area.tag_remove("hyperlink", "1.0", "end")
            content = text_area.get("1.0", "end-1c")
            if not content:
                return
            for match in URL_PATTERN.finditer(content):
                start_idx = f"1.0 + {match.start()} chars"
                end_idx = f"1.0 + {match.end()} chars"
                text_area.tag_add("hyperlink", start_idx, end_idx)
            update_window_title()

        # Функция для открытия ссылки при клике
        def open_link(event):
            try:
                index = event.widget.index(f"@%d,%d" % (event.x, event.y))
                start = text_area.index(f"{index} linestart")
                end = text_area.index(f"{index} lineend")
                for tag in text_area.tag_names(index):
                    if tag == "hyperlink":
                        text = text_area.get(start, end)
                        for match in URL_PATTERN.finditer(text):
                            link_start = f"{start}+{match.start()}c"
                            link_end = f"{start}+{match.end()}c"
                            if text_area.compare(link_start, "<=", index) and text_area.compare(index, "<=", link_end):
                                webbrowser.open(match.group())
                                break
                        break
                return "break"
            except Exception as e:
                logging.error(f"Ошибка при открытии ссылки: {e}")
                return "break"

        text_area.tag_bind("hyperlink", "<Button-1>", open_link)
        text_area.tag_bind("hyperlink", "<Enter>", lambda event: text_area.config(cursor="hand2"))
        text_area.tag_bind("hyperlink", "<Leave>", lambda event: text_area.config(cursor="xterm"))

        # Устанавливаем фокус на текстовое поле
        text_area.focus_set()

        # Функция для авто-капитализации предложений
        def capitalize_sentences(event):
            try:
                content = text_area.get("1.0", "end-1c").rstrip()
                if not content:
                    return

                sentences = []
                current_sentence = ""
                for char in content:
                    current_sentence += char
                    if char in ".!?":
                        sentences.append(current_sentence)
                        current_sentence = ""
                if current_sentence:
                    sentences.append(current_sentence)

                new_text = ""
                for i, sentence in enumerate(sentences):
                    stripped = sentence.lstrip()
                    if stripped:
                        if i == 0 or (i > 0 and sentences[i-1].rstrip() and sentences[i-1].rstrip()[-1] in ".!?"):
                            if stripped[0].isalpha():
                                new_text += sentence[:len(sentence)-len(stripped)] + stripped[0].upper() + stripped[1:]
                            else:
                                new_text += sentence
                        else:
                            new_text += sentence
                    else:
                        new_text += sentence

                if new_text != content:
                    text_area.delete("1.0", "end")
                    text_area.insert("1.0", new_text)

                highlight_links()
            except Exception as e:
                logging.error(f"Ошибка при авто-капитализации: {e}")

        # Привязываем события для обновления иконок кнопок стиля
        text_area.bind("<KeyRelease>", lambda event: [capitalize_sentences(event), highlight_links(), update_style_buttons(event)])
        text_area.bind("<ButtonRelease-1>", update_style_buttons)  # Обновляем иконки при клике мышью
        text_area.bind("<Control-Key>", handle_control_key)

        # Инициализируем иконки кнопок стиля при запуске
        update_style_buttons()

        root.mainloop()
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()
