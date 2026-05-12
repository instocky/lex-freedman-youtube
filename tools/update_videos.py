import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from youtube_client import YouTubeChannelClient


def main():
    updater = YouTubeChannelClient(config.API_KEY)

    existing_data = []
    if os.path.exists(config.OUTPUT_FILE):
        with open(config.OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print("File is corrupted, starting from scratch.")

    existing_ids = {video["id"] for video in existing_data}
    print(f"Existing videos in local file: {len(existing_ids)}")

    try:
        uploads_id = updater.get_channel_uploads_id(config.CHANNEL_HANDLE)
        all_current_ids = updater.get_all_current_video_ids(uploads_id)

        new_ids = [vid_id for vid_id in all_current_ids if vid_id not in existing_ids]

        if not new_ids:
            print("All videos are already up to date.")
            return

        print(f"New videos found: {len(new_ids)}")
        new_videos_data = updater.fetch_details_batched(new_ids)

        updated_data = existing_data + new_videos_data

        with open(config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)

        print(f"\nDone. Added {len(new_videos_data)} videos. Total: {len(updated_data)}")

    except Exception as e:
        print(f"Update error: {e}")


if __name__ == "__main__":
    main()
