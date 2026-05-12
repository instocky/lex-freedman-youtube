import os
from dotenv import load_dotenv

# Загружаем переменные из .env в окружение
load_dotenv()

# Секреты
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Постоянные данные (Конфигурация)
CHANNEL_HANDLE = "@lexfridman"
OUTPUT_FILE = "lex_fridman_videos.json"

# Проверка на наличие ключа при запуске
if not API_KEY:
    raise ValueError("Ошибка: YOUTUBE_API_KEY не найден в файле .env")