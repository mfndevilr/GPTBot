
---

# ChatGPT-4 Telegram Bot

## Описание

Этот проект представляет собой Telegram-бота, использующего мощь нейросети ChatGPT-4 для общения с пользователями. Бот может отвечать на вопросы, поддерживать беседы и выполнять различные задачи, связанные с обработкой естественного языка.

## Установка

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/mfndevilr/gptbot.git
    cd chatgpt-telegram-bot
    ```

2. **Создайте виртуальное окружение и активируйте его:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте переменные окружения:**
    Создайте файл `.env` и добавьте в него следующие строки:
    ```env
    TELEGRAM_TOKEN=your_telegram_bot_token
    OPENAI_API_KEY=your_openai_api_key
    ```

## Использование

1. **Запустите бота:**
    ```bash
    python python.py
    ```

2. **Начните общение с ботом в Telegram:**
    Найдите вашего бота в Telegram и начните с ним общение.

## Структура проекта

- `main.py`: Основной файл для запуска бота.
- `requirements.txt`: Файл с зависимостями проекта.
- `.env`: Файл с переменными окружения (не включен в репозиторий).
- `README.md`: Этот файл.

---

