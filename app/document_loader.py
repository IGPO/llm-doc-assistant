import os
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf(path: str) -> str:
    """
    Загружает PDF-файл и возвращает его текст как одну длинную строку.
    
    :param path: Путь к PDF-файлу
    :return: Весь текст из документа
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл {path} не найден.")

    reader = PdfReader(path)
    text = ""

    for page_num, page in enumerate(reader.pages):
        # Объединяем текст со всех страниц
        content = page.extract_text()
        if content:
            text += content + "\n"
        else:
            print(f"⚠️ Страница {page_num + 1} пуста или не читается.")

    return text

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Делит текст на куски (chunk'и), которые потом можно использовать для обработки LLM.
    
    :param text: Исходный текст
    :param chunk_size: Максимальная длина одного куска
    :param chunk_overlap: Перекрытие между кусками (для контекста)
    :return: Список строк
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],  # от "грубого" к "мелкому"
    )
    return splitter.split_text(text)
