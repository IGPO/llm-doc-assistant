from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import shutil

from app.document_loader import load_pdf, chunk_text
from app.rag_engine import build_vectorstore, retrieve_relevant_chunks
from app.llm_interface import ask_llm

# Создаём FastAPI приложение
app = FastAPI()

# Настраиваем директорию для шаблонов HTML
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Подключаем статику (если будет CSS/JS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

UPLOAD_DIR = os.path.join(BASE_DIR, "../data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
chunks = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return templates.TemplateResponse("index.html", {"request": request, "error": "Только PDF-файлы поддерживаются"})

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = load_pdf(file_path)
    global chunks
    chunks = chunk_text(text)
    build_vectorstore(chunks)

    return templates.TemplateResponse("index.html", {"request": request, "message": "Файл успешно загружен!"})

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    if not chunks:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Сначала загрузите PDF."})

    relevant = retrieve_relevant_chunks(question)
    answer = ask_llm(question, relevant)

    return templates.TemplateResponse("index.html", {"request": request, "answer": answer})