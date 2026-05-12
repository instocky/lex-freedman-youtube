import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from youtube_client import YouTubeChannelClient


if __name__ == "__main__":
    collector = YouTubeChannelClient(config.API_KEY)

    try:
        channel_info = collector.get_channel_info(config.CHANNEL_HANDLE)
        uploads_id = channel_info["uploads_playlist_id"]

        all_ids = collector.get_all_video_ids(uploads_id)
        print(f"Found videos: {len(all_ids)}")
        full_data = collector.get_videos_details_batched(all_ids)

        with open(config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)

        print(f"\nDone. Data saved to {config.OUTPUT_FILE}")

    except Exception as e:
        print(f"Error: {e}")
