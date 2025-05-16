from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Хранилище векторного индекса (будет создан в памяти)
vectorstore = None

def build_vectorstore(chunks: List[str]):
    """
    Создаёт векторное представление чанков текста для дальнейшего поиска по ним.
    
    :param chunks: Список текстовых чанков
    """
    global vectorstore

    # Оборачиваем каждый чанк в объект Document (ожидается FAISS'ом)
    documents = [Document(page_content=chunk) for chunk in chunks]

    # Создаём векторные представления через OpenAI Embeddings
    embedding_model = OpenAIEmbeddings()

    # Создаём векторную БД (в памяти)
    vectorstore = FAISS.from_documents(documents, embedding_model)

def retrieve_relevant_chunks(query: str, k: int = 3) -> List[str]:
    """
    Находит наиболее релевантные чанки по запросу (query).
    
    :param query: Вопрос пользователя
    :param k: Количество чанков, которые нужно вернуть
    :return: Список релевантных текстов
    """
    if vectorstore is None:
        raise ValueError("Векторное хранилище не создано. Сначала вызовите build_vectorstore().")

    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
