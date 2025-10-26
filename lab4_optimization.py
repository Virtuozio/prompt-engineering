import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Завантаження змінних оточення
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Налаштування API
genai.configure(api_key=api_key)

# Ініціалізуємо дві моделі для порівняння
model_pro = genai.GenerativeModel("gemini-2.5-pro")
model_flash = genai.GenerativeModel("gemini-2.5-flash")

# Приклад контексту, який знайшла RAG-система
context = (
    "Метою вивчення навчальної дисципліни «PROMPT інжиніринг» є формування "
    "у майбутніх програмістів системних знань"
    "та практичних навичок з проєктування, розробки та інтеграції великих мовних моделей (LLM) у сучасні програмні системи та продукти. Навчальна дисципліна «PROMPT інжиніринг» забезпечує формування у здобувачів освіти другого (магістерського) освітнього рівня вищої освіти таких компетентностей: Загальні компетентності:  ЗК 01 Здатність до абстрактного мислення, аналізу та синтезу ЗК 02 Здатність застосовувати знання у практичних ситуаціях. ЗК 05 Здатність вчитися й оволодівати сучасними знаннями. Спеціальні (фахові) компетентності спеціальності: СК 02 Здатність формалізувати предметну область певного проєкту у вигляді СК 05 відповідної інформаційної моделі. Здатність розробляти, описувати, аналізувати та оптимізувати архітектурні рішення інформаційних та комп'ютерних систем різного призначення. СК 07 Здатність розробляти програмне забезпечення відповідно до сформульованих вимог з урахуванням наявних ресурсів та обмежень. 3. Результати навчання У результаті успішного завершення курсу «PROMPT інжиніринг та інтеграція LLM-систем» здобувачі вищої освіти сфокусовано розвинуть ключові інженерні навички, необхідні для роботи з передовими технологіями штучного інтелекту. Курс концентрується на формуванні здатності до створення інноваційних програмних рішень, від розробки концептуальної моделі та архітектури до безпосередньої реалізації, що повністю відповідає наступним програмним результатам "
)

# Запит користувача
query = "Яка мета курсу 'Prompt інжиніринг'?"

# Формуємо фінальний промпт
final_prompt = f"Контекст: {context}\n\nЗапитання: {query}\n\nВідповідь:"

# --- ЗАВДАННЯ ДЛЯ АНАЛІЗУ ---

# # 1. Підрахунок токенів
# input_tokens_pro = model_pro.count_tokens(final_prompt)
# print(f"Кількість вхідних токенів для Gemini Pro: {input_tokens_pro.total_tokens}")

# # 2. Генерація відповіді (поки що закоментовано, щоб не витрачати токени)
# response = model_pro.generate_content(final_prompt)
# output_tokens_pro = model_pro.count_tokens(response.text)
# print(f"Кількість вихідних токенів: {output_tokens_pro.total_tokens}")
# print(f"Відповідь: {response.text}")

# # 3. Розрахунок вартості (використовуємо умовні ціни станом на липень 2025)
# # Умовні ціни за 1 мільйон токенів:
# # Gemini Pro: $1.00 (вхідні), $3.00 (вихідні)
# # Gemini Flash: $0.10 (вхідні), $0.30 (вихідні)

# print("\n--- Аналіз швидкодії ---")
# # Тестуємо Gemini Pro
# start_time_pro = time.time()
# response_pro = model_pro.generate_content(final_prompt)
# end_time_pro = time.time()
# print(f"Час відповіді Gemini Pro: {end_time_pro - start_time_pro:.2f} секунд.")

# # Тестуємо Gemini Flash
# start_time_flash = time.time()
# response_flash = model_flash.generate_content(final_prompt)
# end_time_flash = time.time()
# print(f"Час відповіді Gemini Flash: {end_time_flash - start_time_flash:.2f} секунд.")

# --- 2. Потоковий режим (stream=True) ---
# ---------------------------------------
print("\nРЕЖИM: Потоковий (stream=True)")
print("Відправка запиту... Отримання відповіді частинами (chunks)...")
prompt = """
Напиши коротку, але цікаву історію про робота-дослідника, 
який знайшов на Марсі щось несподіване.
"""

print(f"Промпт: {prompt}\n")
print("-" * 30)

start_time_stream = time.time()
time_to_first_token = None

try:
    # Цей виклик повертає ітератор *негайно*
    response_stream = model_pro.generate_content(prompt, stream=True)

    # Ми починаємо отримувати "частини" (chunks) відповіді
    for chunk in response_stream:
        # Вимірюємо час до отримання *першої* частини
        if time_to_first_token is None:
            time_to_first_token = time.time() - start_time_stream

        # Друкуємо кожну частину тексту, як тільки вона надходить
        # flush=True примусово виводить текст у термінал негайно
        print(chunk.text, end="", flush=True)

    # Вимірюємо загальний час генерації
    total_stream_time = time.time() - start_time_stream

    print(f"\n\n[Час до першого токену: {time_to_first_token:.2f} сек]")
    print(f"[Загальний час потоку: {total_stream_time:.2f} сек]")
except Exception as e:
    print(f"Виникла помилка: {e}")


print("\nРЕЖИM: Потоковий (stream=True)")
print("Відправка запиту... Отримання відповіді частинами (chunks)...")

start_time_stream = time.time()
time_to_first_token = None

try:
    # Цей виклик повертає ітератор *негайно*
    response_stream = model_flash.generate_content(prompt, stream=True)

    # Ми починаємо отримувати "частини" (chunks) відповіді
    for chunk in response_stream:
        # Вимірюємо час до отримання *першої* частини
        if time_to_first_token is None:
            time_to_first_token = time.time() - start_time_stream

        # Друкуємо кожну частину тексту, як тільки вона надходить
        # flush=True примусово виводить текст у термінал негайно
        print(chunk.text, end="", flush=True)

    # Вимірюємо загальний час генерації
    total_stream_time = time.time() - start_time_stream

    print(f"\n\n[Час до першого токену: {time_to_first_token:.2f} сек]")
    print(f"[Загальний час потоку: {total_stream_time:.2f} сек]")

except Exception as e:
    print(f"Виникла помилка: {e}")
