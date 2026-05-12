import json
import sys
import os

# Добавляем корень проекта в путь поиска модулей, 
# чтобы скрипт из папки tools мог импортировать config.py из корня
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from googleapiclient.discovery import build
import config

class YouTubeChannelCollector:
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_channel_id(self, handle):
        request = self.youtube.channels().list(
            part="id,contentDetails",
            forHandle=handle
        )
        response = request.execute()
        if not response.get("items"):
            raise Exception(f"Канал {handle} не найден")
        
        channel_data = response["items"][0]
        return {
            "id": channel_data["id"],
            "uploads_playlist_id": channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
        }

    def get_all_video_ids(self, uploads_playlist_id):
        video_ids = []
        next_page_token = None
        print("Сбор ID всех видео с канала...")
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
        print(f"Найдено видео: {len(video_ids)}")
        return video_ids

    def get_videos_details_batched(self, video_ids):
        all_details = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            ids_string = ",".join(batch)
            print(f"Загрузка данных для батча {i//50 + 1}...")
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=ids_string
            )
            response = request.execute()
            all_details.extend(response.get("items", []))
        return all_details

if __name__ == "__main__":
    # Используем данные из config.py
    collector = YouTubeChannelCollector(config.API_KEY)
    
    try:
        channel_info = collector.get_channel_id(config.CHANNEL_HANDLE)
        uploads_id = channel_info["uploads_playlist_id"]
        
        all_ids = collector.get_all_video_ids(uploads_id)
        full_data = collector.get_videos_details_batched(all_ids)
        
        with open(config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)
            
        print(f"\nГотово! Данные сохранены в {config.OUTPUT_FILE}")

    except Exception as e:
        print(f"Ошибка: {e}")