from app.document_loader import load_pdf, chunk_text
from app.llm_interface import ask_llm
from app.rag_engine import build_vectorstore, retrieve_relevant_chunks

# Загружаем документ
text = load_pdf("data/samples/example.pdf")
chunks = chunk_text(text)

# Создаём векторное представление
build_vectorstore(chunks)

# Вопрос от пользователя
query = "О чем документ?"

# Находим подходящие чанки
relevant_chunks = retrieve_relevant_chunks(query)

# Отправляем их в LLM
answer = ask_llm(query, relevant_chunks)
print("Ответ LLM:", answer)
