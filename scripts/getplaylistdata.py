import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import config
from youtube_client import YouTubeChannelClient


URL_PLAYLIST = "https://www.youtube.com/playlist?list=PLLY5OYVYOkFbznJ15Jr6kKwABbgpL8jwb"
ID_PLAYLIST = ""
FILE_NAME_JSON = "menshova-briki.json"


def extract_playlist_id(url_playlist: str, id_playlist: str) -> str:
    if id_playlist.strip():
        return id_playlist.strip()

    if not url_playlist.strip():
        raise ValueError("Set URL_PLAYLIST or ID_PLAYLIST at the top of the script.")

    parsed = urlparse(url_playlist.strip())
    playlist_id = parse_qs(parsed.query).get("list", [""])[0].strip()
    if not playlist_id:
        raise ValueError("Could not extract playlist ID from URL_PLAYLIST.")

    return playlist_id


def main() -> None:
    playlist_id = extract_playlist_id(URL_PLAYLIST, ID_PLAYLIST)
    output_path = PROJECT_ROOT / FILE_NAME_JSON

    client = YouTubeChannelClient(config.API_KEY)
    video_ids = client.get_all_video_ids(playlist_id)
    print(f"Found videos in playlist: {len(video_ids)}")

    videos_data = client.get_videos_details_batched(video_ids)
    print(f"Fetched video details: {len(videos_data)}")

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(videos_data, f, ensure_ascii=False, indent=4)

    print(f"Done. Data saved to {output_path}")


if __name__ == "__main__":
    main()
