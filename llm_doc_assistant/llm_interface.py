from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY
from llm_doc_assistant.logger import logger  # ✅ our logger

# Initialize the LLM instance with key from config
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2)

def ask_llm(question: str, context: str) -> str:
    """
    Sends a question along with context to the LLM and returns the generated answer.
    """
    logger.info("Received question for LLM.")
    messages = [
        HumanMessage(content=f"Context: {context}\n\nQuestion: {question}")
    ]

    try:
        response = llm.invoke(messages)
        logger.info("LLM response successfully generated.")
        return response.content
    except Exception as e:
        logger.exception("LLM failed to generate a response.")
        return "An error occurred while querying the language model."
