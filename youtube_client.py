from googleapiclient.discovery import build


class YouTubeChannelClient:
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_channel_info(self, handle):
        request = self.youtube.channels().list(
            part="id,contentDetails",
            forHandle=handle,
        )
        response = request.execute()
        if not response.get("items"):
            raise Exception(f"Channel {handle} not found")

        channel_data = response["items"][0]
        return {
            "id": channel_data["id"],
            "uploads_playlist_id": channel_data["contentDetails"]["relatedPlaylists"]["uploads"],
        }

    def get_channel_uploads_id(self, handle):
        return self.get_channel_info(handle)["uploads_playlist_id"]

    def list_upload_video_ids(self, uploads_playlist_id):
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            response = request.execute()
            for item in response.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return video_ids

    def get_all_video_ids(self, uploads_playlist_id):
        return self.list_upload_video_ids(uploads_playlist_id)

    def get_all_current_video_ids(self, uploads_playlist_id):
        return self.list_upload_video_ids(uploads_playlist_id)

    def fetch_video_details_batched(self, video_ids):
        details = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(batch),
            )
            response = request.execute()
            details.extend(response.get("items", []))

        return details

    def get_videos_details_batched(self, video_ids):
        return self.fetch_video_details_batched(video_ids)

    def fetch_details_batched(self, video_ids):
        return self.fetch_video_details_batched(video_ids)
