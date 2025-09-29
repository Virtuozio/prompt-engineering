import os
import google.generativeai as genai
from dotenv import load_dotenv

# Завантаження змінних оточення
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Налаштування API
genai.configure(api_key=api_key)

# Ініціалізуємо дві моделі для порівняння
model_pro = genai.GenerativeModel("gemini-1.5-pro-latest")
model_flash = genai.GenerativeModel("gemini-1.5-flash-latest")

# Приклад контексту, який знайшла RAG-система
context = (
    "Метою вивчення навчальної дисципліни «PROMPT інжиніринг» є формування "
    "у майбутніх програмістів системних знань..."
    # (вставте сюди 2-3 абзаци з робочої програми)
)

# Запит користувача
query = "Яка мета курсу 'Prompt інжиніринг'?"

# Формуємо фінальний промпт
final_prompt = f"Контекст: {context}\n\nЗапитання: {query}\n\nВідповідь:"

# --- ЗАВДАННЯ ДЛЯ АНАЛІЗУ ---

# 1. Підрахунок токенів
input_tokens_pro = model_pro.count_tokens(final_prompt)
print(f"Кількість вхідних токенів для Gemini Pro: {input_tokens_pro.total_tokens}")

# 2. Генерація відповіді (поки що закоментовано, щоб не витрачати токени)
# response = model_pro.generate_content(final_prompt)
# output_tokens_pro = model_pro.count_tokens(response.text)
# print(f"Кількість вихідних токенів: {output_tokens_pro.total_tokens}")
# print(f"Відповідь: {response.text}")

# 3. Розрахунок вартості (використовуємо умовні ціни станом на липень 2025)
# Умовні ціни за 1 мільйон токенів:
# Gemini Pro: $1.00 (вхідні), $3.00 (вихідні)
# Gemini Flash: $0.10 (вхідні), $0.30 (вихідні)
