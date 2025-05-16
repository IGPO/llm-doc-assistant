import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Загружаем переменные из .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настраиваем LLM-клиент
llm = ChatOpenAI(
    temperature=0.2,           # Чем меньше — тем строже модель отвечает по теме
    model_name="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def ask_llm(question: str, context_chunks: List[str]) -> str:
    """
    Отправляет запрос в LLM, используя переданные чанки как контекст.
    
    :param question: Вопрос пользователя
    :param context_chunks: Список кусков текста из документа
    :return: Ответ от LLM
    """
    # Объединяем чанки в один контекст
    context = "\n\n".join(context_chunks)

    # Создаём "системное сообщение" — оно определяет поведение модели
    system_prompt = (
        "Ты умный ассистент, помогающий отвечать на вопросы по загруженному документу. "
        "Используй только представленный контекст. Если не знаешь — скажи 'не знаю'."
    )

    # Формируем список сообщений
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Контекст:\n{context}\n\nВопрос: {question}")
    ]

    # Получаем ответ
    response = llm.invoke(messages)
    return response.content

