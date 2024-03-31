from googleapiclient.discovery import build
import os

API_KEY = os.getenv('api_key')

def get_channel_info(channel_id,ResultSize):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        channel_request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        channel_response = channel_request.execute()

        if 'items' in channel_response:
            channel = channel_response['items'][0]
            channel_title = channel['snippet']['title']
            subscriber_count = channel['statistics']['subscriberCount']
            view_count = channel['statistics']['viewCount']
            video_count = channel['statistics']['videoCount']

            print("\n")
            print(f"Channel Title: {channel_title}")
            print(f"Subscriber Count: {subscriber_count}")
            print(f"Total Views: {view_count}")
            print(f"Total Videos: {video_count}")

            video_request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=ResultSize, 
                type='video' 
            )
            video_response = video_request.execute()

            if 'items' in video_response:
                print("\nVideos in channel:- ")
                for video in video_response['items']:
                    video_id = video['id']['videoId']
                    video_info = get_video_info(youtube, video_id)
                    print("Title:", video_info['title'])
                    print("Link:", video_info['link'])
                    print("Thumbnail:", video_info['thumbnail'])
                    print("\n")
            else:
                print("No videos found for this channel.")
        else:
            print("Channel not found or API quota exceeded.")

    except Exception as e:
        print("An error occurred:", str(e))

def get_video_info(youtube, video_id):
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
        return {
            'title': video_title,
            'link': video_link,
            'thumbnail': video_thumbnail
        }
    else:
        return "Video not found or API quota exceeded."

if __name__ == "__main__":
    channel_id = os.getenv('channel_id')
    get_channel_info(channel_id,2)
