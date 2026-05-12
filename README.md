# YouTube Channel Data Collector

Набор скриптов для полного и инкрементального сбора метаданных видео с YouTube-канала Lex Fridman, а также для подсчета токенов в текстовых файлах.

## Текущая конфигурация

- Канал: `@lexfridman`
- Конфиг: [`config.py`](/C:/Projects/_Others/0512_lex-freedman-youtube/config.py)
- API-ключ: `YOUTUBE_API_KEY` в `.env`
- Файл вывода: `lex_fridman_videos.json`
- Общий клиент YouTube API: [`youtube_client.py`](/C:/Projects/_Others/0512_lex-freedman-youtube/youtube_client.py)

## Структура

```text
0512_lex-freedman-youtube/
├── config.py
├── youtube_client.py
├── lex_fridman_videos.json
├── tools/
│   ├── full_sync.py
│   ├── update_videos.py
│   └── calk_tokens.py
├── .env
├── .env.example
└── README.md
```

## Установка

```bash
python -m venv venv
.\venv\Scripts\activate
pip install google-api-python-client python-dotenv tiktoken
```

## Настройка

1. Создайте `.env` по образцу `.env.example`.
2. Добавьте `YOUTUBE_API_KEY`.
3. При необходимости измените `CHANNEL_HANDLE` и `OUTPUT_FILE` в [`config.py`](/C:/Projects/_Others/0512_lex-freedman-youtube/config.py).

## Скрипты

- `python tools/full_sync.py` - полный сбор всех видео и сохранение в JSON.
- `python tools/update_videos.py` - догрузка только новых видео в существующий JSON.
- `python tools/calk_tokens.py` - подсчет токенов в текстовом файле.

## Примечания

- `full_sync.py` скачивает весь набор данных заново.
- `update_videos.py` использует локальный JSON как базу и добавляет только новые ролики.
- `youtube_client.py` содержит общий клиент для работы с YouTube Data API.
- `lex_fridman_videos.json` - рабочий артефакт, который может быть перегенерирован скриптами.
