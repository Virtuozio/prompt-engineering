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
file_names = ["knowledge.txt", "knowledge2.txt", "knowledge3.txt"]  # список файлів
texts = []

for fname in file_names:
    try:
        with open(fname, "r", encoding="utf-8") as f:
            texts.append(f.read())
        print(f"✅ Файл {fname} завантажено.")
    except FileNotFoundError:
        print(f"⚠️ Файл {fname} не знайдено, пропускаю.")

# Об'єднуємо всі тексти в один
knowledge_text = "\n".join(texts)
print("✅ Всі тексти об’єднано.")
print(knowledge_text[:300])  # для перевірки

# --- РОЗБИТТЯ НА ЧАНКИ ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)

chunks = text_splitter.split_text(knowledge_text)
print(f"✅ Документи розбито на {len(chunks)} чанків.")
print(chunks[0])  # Можна розкоментувати для перевірки


# --- СТВОРЕННЯ ЕМБЕДИНГІВ ---
embedding_model = "models/text-embedding-004"  # Актуальна модель ембедингів

embeddings = genai.embed_content(
    model=embedding_model, content=chunks, task_type="retrieval_document"
)["embedding"]

print(f"✅ Створено {len(embeddings)} векторних представлень.")
print(embeddings[0][:5])  # Можна розкоментувати для перевірки

# --- СТВОРЕННЯ ВЕКТОРНОЇ БД ---
client = chromadb.Client()

collection = client.get_or_create_collection("course_syllabus")

# Додаємо наші чанки та їх ембединги до колекції
collection.add(
    ids=[str(i) for i in range(len(chunks))],  # ID для кожного чанка
    embeddings=embeddings,
    documents=chunks,
)

print("✅ Векторну базу даних створено та наповнено.")

# --- ПОШУК ТА ГЕНЕРАЦІЯ ---
query = "Що є неприпустимим  у використанні ШІ?"
print(f"\n✅ Запит користувача: {query}")

# 1. Створюємо ембединг для запиту
query_embedding = genai.embed_content(
    model=embedding_model, content=query, task_type="retrieval_query"
)["embedding"]

# 2. Шукаємо релевантні чанки у векторній БД
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,  # Кількість найбільш релевантних чанків
)

retrieved_documents = results["documents"][0]
context = "\n".join(retrieved_documents)

print("\n📚 Знайдений контекст:")
print(context)

# 3. Формуємо фінальний промпт
final_prompt = f"""
Ти - чат-бот-консультант по робочій програмі курсу "Prompt інжиніринг".
Твоя задача - чітко відповідати на питання студента, базуючись **виключно** на наданому контексті.
Якщо відповіді немає в контексті, так і скажи:
"На жаль, у наданих матеріалах немає інформації на це питання."

**Контекст:**
{context}

**Запитання:**
{query}
"""

# 4. Генеруємо відповідь
generative_model = genai.GenerativeModel("gemini-2.5-flash")
response = generative_model.generate_content(final_prompt)

print("\n🤖 Відповідь ШІ:")
print(response.text)
