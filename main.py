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

# --- РОЗБИТТЯ НА ЧАНКИ ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Розмір одного чанка в символах
    chunk_overlap=100,  # Перекриття між чанками
)

chunks = text_splitter.split_text(knowledge_text)
print(f"✅ Документ розбито на {len(chunks)} чанків.")
print(chunks[0])  # Можна розкоментувати для перевірки


# --- СТВОРЕННЯ ЕМБЕДИНГІВ ---
embedding_model = "models/text-embedding-004"  # Актуальна модель ембедингів

embeddings = genai.embed_content(
    model=embedding_model, content=chunks, task_type="retrieval_document"
)["embedding"]

print(f"✅ Створено {len(embeddings)} векторних представлень.")
print(embeddings[0][:5])  # Можна розкоментувати для перевірки
