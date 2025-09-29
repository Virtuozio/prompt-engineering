<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Virtuozio/prompt-engineering">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">🧪 Лабораторні роботи з Prompt Engineering</h3>

  <p align="center">
    Цей репозиторій містить мої лабораторні роботи, присвячені вивченню **Prompt Engineering** та інтеграції великих мовних моделей (LLM) у програмні проекти.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Знімок екрана продукту][product-screenshot]](https://example.com)

Цей репозиторій є навчальним і містить реалізацію лабораторних робіт з **Prompt Engineering**.  
Основна мета — сформувати практичні навички взаємодії з API великих мовних моделей, оптимізації промптів і побудови невеликих прототипів застосунків.

Особливості:

- Приклади використання Python для інтеграції з LLM (Google Gemini).
- Кроки для розгортання локального середовища розробки.
- Приклади розрахунку кількості токенів і вартості запитів.

<p align="right">(<a href="#readme-top">повернутися нагору</a>)</p>

### Built With

- [![Python][Python.org]][Python-url]
- [![dotenv][dotenv-shield]][dotenv-url]
- [![Google AI Studio][GoogleAI-shield]][GoogleAI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Щоб запустити проєкт локально, виконайте кроки нижче.

### Prerequisites

1. Python 3.10+
2. Встановлений `pip`
3. Створений API Key у [Google AI Studio](https://aistudio.google.com/api-keys)

### Installation

1. Отримайте безкоштовний API-ключ [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
2. Клонування репозиторію
   ```sh
   git clone https://github.com/Virtuozio/prompt-engineering
   ```
3. Встановлення залежностей
   ```sh
   pip install -r requirements.txt
   ```
4. Створіть файл `.env` і додайте у нього ваш API ключ:
   ```.env
   GEMINI_API_KEY = "ENTER YOUR API"
   ```
5. Запуск прикладу:
   ```sh
   python main.py
   ```
6. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] [Лабораторна робота №2 – Робота з LLM API на Python](../../tree/lab2)
- [x] [Лабораторна робота №3 – Робота з LLM API на Python](../../tree/lab3)
- [ ] [Лабораторна робота №4 – Робота з LLM API на Python](../../tree/lab4)
- [ ] [Підсумковий проект]

See the [open issues](https://github.com/Virtuozio/prompt-engineering/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Будь-які покращення **вітаються 🙌**.

1. Форкніть репозиторій
2. Створіть нову гілку (`git checkout -b feature/AmazingFeature`)
3. Зробіть коміт (`git commit -m 'Add some AmazingFeature'`)
4. Запуште у свою гілку (`git push origin feature/AmazingFeature`)
5. Відкрийте Pull Request

<!-- CONTACT -->

## Contact

Bogdan - nazarchykb@gmail.com

Project Link: [https://github.com/Virtuozio/prompt-engineering](https://github.com/Virtuozio/prompt-engineering)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
