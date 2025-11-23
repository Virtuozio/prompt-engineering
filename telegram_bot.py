import logging
import os
import asyncio
import chromadb
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    tg_api_key = os.getenv("TELEGRAM_TOKEN")
    client = genai.Client(api_key)
    app = ApplicationBuilder().token(tg_api_key).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 Бот запущено! Натисніть Ctrl+C для зупинки.")
    app.run_polling()

# Налаштування логування (щоб бачити помилки в консолі)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class VectorKnowledgeBase:
    """Клас для роботи з векторною базою даних ChromaDB."""

    def __init__(self):
        self.clientdb = chromadb.Client()

        self.collection = self.clientdb.get_or_create_collection(name="tech_docs")

        self._populate_db()

    def _populate_db(self):
        if self.collection.count() > 0:
            return

        print("📥 Індексація бази знань у ChromaDB...")

        documents = [
            "React Components: Components are the building blocks of any React application. A component is a self-contained module that renders some output.",
            "React Hooks: Hooks allow function components to have access to state and other React features. Class components are generally no longer needed.",
            "useState: A Hook that lets you add React state to function components. Example: const [count, setCount] = useState(0);",
            "useEffect: A Hook that lets you perform side effects in function components. It tells React that your component needs to do something after render.",
            "Props: Props are arguments passed into React components. Props are passed to components via HTML attributes.",
        ]

        ids = [str(i) for i in range(len(documents))]
        embeddings = []
        for doc in documents:
            emb = client.models.embed_content(
                model="gemini-embedding-001",
                contents=doc,
            )["embedding"]
            embeddings.append(emb)

        self.collection.add(documents=documents, embeddings=embeddings, ids=ids)
        print(f"✅ База даних готова! Завантажено {len(documents)} документів.")

    def search(self, query_text, n_results=1):
        query_emb = genai.embed_content(
            model="models/text-embedding-004",
            content=query_text,
            task_type="retrieval_query",
        )["embedding"]

        results = self.collection.query(
            query_embeddings=[query_emb], n_results=n_results
        )

        if results["documents"] and results["documents"][0]:
            return results["documents"][0][0]
        return None


db = VectorKnowledgeBase()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я RAG-бот по документації React.\n"
        "Я використовую ChromaDB та Gemini AI.\n"
        "Запитай мене про хуки або компоненти!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    context_text = db.search(user_query)

    if not context_text:
        context_info = "Інформації в базі не знайдено."
    else:
        context_info = context_text

    system_prompt = f"""
    Ти — технічний консультант. Відповідай на питання, базуючись на цьому контексті:
    "{context_info}"
    
    Якщо інформації немає в контексті, так і скажи. Не вигадуй.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\nПитання: {user_query}",
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Вибач, сталася помилка API: {e}"

    await update.message.reply_text(bot_reply)
