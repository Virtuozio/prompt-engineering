import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

# --- НАЛАШТУВАННЯ ---
# Завантаження змінних з .env
load_dotenv()

# Отримання API-ключа
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Не знайдено GEMINI_API_KEY у .env файлі")

# Конфігурація Google Generative AI
genai.configure(api_key=api_key)

# --- ЗАВАНТАЖЕННЯ ДАНИХ ---
try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_text = f.read()
    print("✅ Дані завантажено успішно.")
except FileNotFoundError:
    raise FileNotFoundError("❌ Файл knowledge.txt не знайдено!")
print(knowledge_text[:200])  # Можна розкоментувати для перевірки
