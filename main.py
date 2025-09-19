import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


# Визначаємо наші інструменти
def add(a: float, b: float) -> float:
    """Adds two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b


def subtract(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a - b


def divide(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a / b


# Завантажуємо змінні оточення з файлу .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Конфігуруємо SDK
client = genai.Client(api_key=api_key)
print("Модель успішно ініціалізовано!")

# # Надсилаємо промпт до моделі
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Поясни концепцію рекурсії в програмуванні, використовуючи аналогію з ляльками-матрьошками.",
# )
# # Виводимо текстову відповідь
# print(response.text)

# Надсилаємо запит, який має викликати функцію
# prompt = "Скільки буде, якщо 5 помножити на 12, а потім додати 8?"
prompt = "Скільки буде 100 поділити на 4?"
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[add, multiply, subtract, divide],
    ),
)

print(f"Фінальна текстова відповідь: {response.text}")
