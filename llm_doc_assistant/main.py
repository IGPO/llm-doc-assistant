# 📁 app/main.py

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from llm_doc_assistant.document_loader import load_pdf, chunk_text
from llm_doc_assistant.rag_engine import build_vectorstore, retrieve_relevant_chunks
from llm_doc_assistant.llm_interface import ask_llm
from llm_doc_assistant.logger import logger

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile):
    try:
        logger.info(f"Received file upload: {file.filename}")
        text = load_pdf(file.file)
        chunks = chunk_text(text)
        build_vectorstore(chunks)
        logger.info("Document processed and vectorstore updated.")
        return templates.TemplateResponse("index.html", {"request": request, "message": "Document uploaded and indexed successfully."})
    except Exception as e:
        logger.exception("Failed to upload and process PDF.")
        return templates.TemplateResponse("index.html", {"request": request, "error": "Error processing the document."})

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    try:
        logger.info(f"Received question: {question}")
        context = retrieve_relevant_chunks(question)
        answer = ask_llm(question, context)
        logger.info("Answer generated successfully.")
        return templates.TemplateResponse("index.html", {"request": request, "answer": answer})
    except Exception as e:
        logger.exception("Failed to process question.")
        return templates.TemplateResponse("index.html", {"request": request, "error": "Error generating answer."})