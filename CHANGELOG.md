# Changelog

## 2026-05-12

- Вынес общий YouTube-клиент в [`youtube_client.py`](/C:/Projects/_Others/0512_lex-freedman-youtube/youtube_client.py).
- Обновлен [`README.md`](/C:/Projects/_Others/0512_lex-freedman-youtube/README.md) под текущую структуру проекта.
- Зафиксирована текущая конфигурация проекта: `CHANNEL_HANDLE = "@lexfridman"`.
- Зафиксирована текущая конфигурация проекта: `OUTPUT_FILE = "lex_fridman_videos.json"`.
- Зафиксирована текущая конфигурация проекта: `YOUTUBE_API_KEY` читается из `.env`.
- Зафиксирована текущая конфигурация проекта: общий клиент используется обоими скриптами в `tools/`.
- Текущий набор скриптов: `tools/full_sync.py`, `tools/update_videos.py`, `tools/calk_tokens.py`.
