from googleapiclient.discovery import build
import os

API_KEY = "AIzaSyDZsi7hHAROKYm9z0v2iLdll56tx5HNXtI"
def get_channel_info(channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        channel_request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        channel_response = channel_request.execute()

        print(channel_response)
        if 'items' in channel_response:
            channel = channel_response['items'][0]
            channel_title = channel['snippet']['title']
            subscriber_count = channel['statistics']['subscriberCount']
            view_count = channel['statistics']['viewCount']
            video_count = channel['statistics']['videoCount']
            creation_date = channel['snippet']['publishedAt']
            resp = {
                        "Title": channel_title,
                        "subscribers":subscriber_count ,
                        "totalViews":view_count,
                        "totalVideos":video_count,
                        "creationDate": creation_date
                    }
            return resp
        else:
            resp = {
                "error":"Channel not found or API quota exceeded.",
                "solution":"check if the channel_id is valid or not",
                "if still not working":"Try again later as api quota might have exceeded the limit."
            }
            return resp

    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)

def get_video_info(channel_id, result_size):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=result_size,
        type='video'
    )
    video_response = video_request.execute()

    video_list = []
    for video in video_response['items']:
        video_id = video['id']['videoId']
        video_request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        video_response = video_request.execute()

        if 'items' in video_response:
            video = video_response['items'][0]
            video_title = video['snippet']['title']
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_thumbnail = video['snippet']['thumbnails']['medium']['url']
            resp = {
                'title': video_title,
                'thumbnail': video_thumbnail,
                'link': video_link
            }
            video_list.append(resp)

    return video_list
