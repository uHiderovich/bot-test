import os
import sys

BOOK_PATH = "book/book.txt"
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end_symbols = {",", ".", "!", ":", ";", "?"}
    end = min(start + size, len(text))
    cut = text[start:end]

    # Обрезаем всю последовательность символов если она разбита
    if cut[-1] in end_symbols and cut[-2] in end_symbols:
        c_len = len(cut) - 1
        char = cut[c_len]
        while char in end_symbols:
            c_len -= 1
            char = cut[c_len]
        cut = cut[0:c_len]

    # Ищем индекс последнего знака препинания
    last_index = -1
    for char in end_symbols:
        idx = cut.rfind(char)
        if idx > last_index:
            last_index = idx

    # Если знак найден, обрезаем строку
    if last_index != -1:
        cut = cut[: last_index + 1]  # Включаем сам символ

    return (cut, len(cut))


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    pass


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
