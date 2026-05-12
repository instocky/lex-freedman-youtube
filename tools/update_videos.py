import json
import sys
import os

# Добавляем корень проекта в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from googleapiclient.discovery import build
import config

class YouTubeUpdater:
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_channel_uploads_id(self, handle):
        """Получает ID плейлиста со всеми загрузками"""
        request = self.youtube.channels().list(
            part="contentDetails",
            forHandle=handle
        )
        response = request.execute()
        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def get_all_current_video_ids(self, uploads_playlist_id):
        """Собирает все актуальные ID видео с канала"""
        video_ids = []
        next_page_token = None
        while True:
            request = self.youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        return video_ids

    def fetch_details_batched(self, video_ids):
        """Запрашивает детали только для переданного списка ID"""
        details = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            ids_string = ",".join(batch)
            print(f"Загрузка новых видео: батч {i//50 + 1}...")
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=ids_string
            )
            response = request.execute()
            details.extend(response.get("items", []))
        return details

def main():
    updater = YouTubeUpdater(config.API_KEY)
    
    # 1. Загружаем существующие данные
    existing_data = []
    if os.path.exists(config.OUTPUT_FILE):
        with open(config.OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print("Файл поврежден, начинаем сбор с нуля.")

    # Создаем set из ID уже имеющихся видео для мгновенного поиска O(1)
    existing_ids = {video["id"] for video in existing_data}
    print(f"В локальном файле уже есть {len(existing_ids)} видео.")

    try:
        # 2. Получаем актуальный список всех ID с канала
        uploads_id = updater.get_channel_uploads_id(config.CHANNEL_HANDLE)
        all_current_ids = updater.get_all_current_video_ids(uploads_id)
        
        # 3. Находим только те ID, которых нет в нашем файле
        new_ids = [vid_id for vid_id in all_current_ids if vid_id not in existing_ids]
        
        if not new_ids:
            print("Все видео уже актуальны. Обновление не требуется.")
            return

        print(f"Найдено новых видео: {len(new_ids)}")

        # 4. Загружаем детали только для новых видео
        new_videos_data = updater.fetch_details_batched(new_ids)
        
        # 5. Объединяем и сохраняем
        updated_data = existing_data + new_videos_data
        
        with open(config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)
            
        print(f"\nУспешно! Добавлено {len(new_videos_data)} видео. Всего в базе: {len(updated_data)}")

    except Exception as e:
        print(f"Ошибка при обновлении: {e}")

if __name__ == "__main__":
    main()