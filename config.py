# 📁 config.py
# Central configuration loader for environment variables

import os
from dotenv import load_dotenv

# Load from .env file into system environment
load_dotenv()

# Example variables to be used across your app
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "data/vectorstore")

# Add more config as needed

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file.")