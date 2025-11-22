import logging
import os
import asyncio
import chromadb
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)



genai.configure(api_key=api_key)

# Налаштування логування (щоб бачити помилки в консолі)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class VectorKnowledgeBase:
    """Клас для роботи з векторною базою даних ChromaDB."""

    def __init__(self):
        # Ініціалізація клієнта Chroma (в пам'яті для прототипу)
        self.client = chromadb.Client()

        # Створення або отримання колекції документів
        # get_or_create дозволяє не падати при перезапуску
        self.collection = self.client.get_or_create_collection(name="tech_docs")

        # Завантаження даних при старті
        self._populate_db()

    def _populate_db(self):
        """Імітація завантаження документації в базу."""
        if self.collection.count() > 0:
            return  # Якщо дані вже є, не дублюємо

        print("📥 Індексація бази знань у ChromaDB...")

        documents = [
            "React Components: Components are the building blocks of any React application. A component is a self-contained module that renders some output.",
            "React Hooks: Hooks allow function components to have access to state and other React features. Class components are generally no longer needed.",
            "useState: A Hook that lets you add React state to function components. Example: const [count, setCount] = useState(0);",
            "useEffect: A Hook that lets you perform side effects in function components. It tells React that your component needs to do something after render.",
            "Props: Props are arguments passed into React components. Props are passed to components via HTML attributes.",
        ]

        # Генеруємо ID для кожного документа
        ids = [str(i) for i in range(len(documents))]

        # Створюємо ембедінги через Gemini
        # Примітка: У продакшені краще написати кастомну embedding function для Chroma,
        # але тут зробимо явно для наочності.
        embeddings = []
        for doc in documents:
            emb = genai.embed_content(
                model="models/text-embedding-004",
                content=doc,
                task_type="retrieval_document",
            )["embedding"]
            embeddings.append(emb)

        # Зберігаємо все в ChromaDB
        self.collection.add(documents=documents, embeddings=embeddings, ids=ids)
        print(f"✅ База даних готова! Завантажено {len(documents)} документів.")

    def search(self, query_text, n_results=1):
        """Пошук релевантних документів."""
        # 1. Векторизуємо запит користувача
        query_emb = genai.embed_content(
            model="models/text-embedding-004",
            content=query_text,
            task_type="retrieval_query",
        )["embedding"]

        # 2. Шукаємо в базі найближчі вектори
        results = self.collection.query(
            query_embeddings=[query_emb], n_results=n_results
        )

        # Повертаємо знайдений текст (якщо є)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0][0]  # Повертаємо найкращий збіг
        return None


# Створюємо глобальний екземпляр бази
db = VectorKnowledgeBase()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка команди /start"""
    await update.message.reply_text(
        "Привіт! Я RAG-бот по документації React.\n"
        "Я використовую ChromaDB та Gemini AI.\n"
        "Запитай мене про хуки або компоненти!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка текстових повідомлень"""
    user_query = update.message.text

    # Індикація "друкує..." в телеграмі, поки ми думаємо
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # 1. RETRIEVAL: Шукаємо контекст у базі
    context_text = db.search(user_query)

    if not context_text:
        context_info = "Інформації в базі не знайдено."
    else:
        context_info = context_text

    # 2. AUGMENTATION & GENERATION
    system_prompt = f"""
    Ти — технічний консультант. Відповідай на питання, базуючись на цьому контексті:
    "{context_info}"
    
    Якщо інформації немає в контексті, так і скажи. Не вигадуй.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"{system_prompt}\n\nПитання: {user_query}")
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Вибач, сталася помилка API: {e}"

    await update.message.reply_text(bot_reply)


if __name__ == "__main__":
    # Перевірка наявності токенів
    
    if (
        GOOGLE_API_KEY == "ТУТ_ВАШ_GOOGLE_KEY"
        or TELEGRAM_TOKEN == "ТУТ_ВАШ_TELEGRAM_TOKEN"
    ):
        print("❌ ПОМИЛКА: Ви забули вставити API ключі у файл!")
        exit()

    # Запуск бота
    app = ApplicationBuilder().token(tg_api_key).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 Бот запущено! Натисніть Ctrl+C для зупинки.")
    app.run_polling()
