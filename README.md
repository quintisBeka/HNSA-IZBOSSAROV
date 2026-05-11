# Hybrid: Network Security Auditor / Гибридный аудитор

⚠️ Только для образовательных, лабораторных и авторизованных проверок.

## Запуск
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python app.py`
4. Открыть `http://127.0.0.1:5000`

## Настройка Telegram
- Установить переменные окружения `BOT_TOKEN`, `CHAT_ID`.

## Возможности
- Авторизация (Admin/Analyst), безопасное хранение паролей.
- Скан IP/CIDR на открытые порты.
- Оценка риска и рекомендации.
- История, логи, PDF отчеты.
- Геолокация IP, DNS/reverse DNS, uptime, базовый discovery.
- RU/KZ локализация, Dashboard с Chart.js.
