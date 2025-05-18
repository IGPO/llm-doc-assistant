from pypdf import PdfReader
from typing import List, IO
from llm_doc_assistant.logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file: IO[bytes]) -> str:
    """
    Extracts all text from a PDF file-like object.
    This function is used after uploading a file via FastAPI.
    """
    logger.debug("Reading PDF content from uploaded file object.")
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def chunk_text(text: str) -> List[str]:
    """
    Splits the full document text into overlapping chunks.
    This is useful for feeding manageable context pieces into the LLM.
    """
    logger.debug("Splitting text into chunks for vectorstore indexing.")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)
