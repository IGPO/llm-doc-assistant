# 📁 app/rag_engine.py

import os
from config import EMBEDDING_MODEL, VECTORSTORE_DIR
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from llm_doc_assistant.logger import logger

# Initialize embedding model from config
embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Global variable to hold vectorstore reference
vectorstore = None

def build_vectorstore(chunks: list[str]) -> None:
    """
    Build a FAISS vectorstore from text chunks and store in global reference.
    """
    global vectorstore
    logger.info("Building vectorstore from provided text chunks...")

    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    vectorstore = FAISS.from_texts(chunks, embedding_model)
    vectorstore.save_local(VECTORSTORE_DIR)
    logger.info("Vectorstore built and saved locally.")

def retrieve_relevant_chunks(query: str, k: int = 5) -> str:
    """
    Loads vectorstore and returns top-k relevant chunks for the query.
    """
    global vectorstore
    logger.debug(f"Retrieving top {k} relevant chunks for query: '{query}'")

    if vectorstore is None:
        if not os.path.exists(VECTORSTORE_DIR):
            logger.error("Vectorstore not found. You must build it first.")
            raise ValueError("Vectorstore not found. Please build it first.")

        vectorstore = FAISS.load_local(VECTORSTORE_DIR, embedding_model)
        logger.info("Vectorstore loaded from disk.")

    docs = vectorstore.similarity_search(query, k=k)
    logger.info(f"Retrieved {len(docs)} documents from vectorstore.")
    return "\n\n".join([doc.page_content for doc in docs])
