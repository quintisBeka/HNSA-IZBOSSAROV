# Hybrid: Network Security Auditor / Гибридный аудитор

⚠️ Только для образовательных, лабораторных и авторизованных проверок.

## Локальный запуск (Python)
1. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)
2. `pip install -r requirements.txt`
3. `python app.py`
4. Открыть `http://127.0.0.1:5000`

## Сборка EXE для запуска на Windows
Чтобы запускать на любом компьютере **без установленного Python**, соберите standalone EXE:

1. Перейдите в проект в `cmd` на Windows.
2. Запустите `build_exe.bat`.
3. Получите файл `dist\\HybridAuditor.exe`.
4. Скопируйте EXE на другой компьютер и запустите.
5. Откройте браузер: `http://127.0.0.1:5000`

> Примечание: EXE собирается под ту же ОС, где выполняется сборка.
> Для Windows нужен билд на Windows.

## Настройка Telegram
- Установить переменные окружения `BOT_TOKEN`, `CHAT_ID`.

## Возможности
- Авторизация (Admin/Analyst), безопасное хранение паролей.
- Скан IP/CIDR на открытые порты.
- Оценка риска и рекомендации.
- История, логи, PDF отчеты.
- Геолокация IP, DNS/reverse DNS, uptime, базовый discovery.
- RU/KZ локализация, Dashboard с Chart.js.


## Если build_exe.bat пишет: "pyinstaller не является командой"
Это означает, что в PATH не найден исполняемый файл `pyinstaller`.
Обновлённый `build_exe.bat` запускает сборку через модульный вызов:
- `py -m PyInstaller` или `python -m PyInstaller`

Сделайте так:
1. Откройте **обычный CMD** (не старый терминал с битым PATH).
2. Проверьте Python:
   - `py --version` или `python --version`
3. Если Python не найден — переустановите Python и включите галочку **Add python.exe to PATH**.
4. Запустите:
   - `build_exe.bat`

Ручной вариант (если нужно):
- `py -m pip install --upgrade pip`
- `py -m pip install -r requirements.txt`
- `py -m pip install pyinstaller`
- `py -m PyInstaller --onefile --name HybridAuditor hybrid_launcher.py --add-data "templates;templates" --add-data "static;static" --add-data "translations;translations" --add-data "instance;instance"`

Если проект лежит в OneDrive и возникают странные ошибки доступа/кодировки, перенесите папку в `C:\Projects\HybridAuditor` и повторите сборку.
