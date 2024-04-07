import requests
import json
import os
from flask import Flask, redirect, jsonify, request, session, url_for
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

app=Flask(__name__)

API_KEY = os.getenv('api_key')
name=os.getenv('name')
id=os.getenv('id')
page_id=os.getenv('page_id')
ig_id=os.getenv('ig_id')
access_token=os.getenv('access_token')
api_key=os.getenv('api_key')
channel_id=os.getenv('channel_id')
result_size=10

params={"fields":"username,name,media,followers_count,follows_count,media_count,id,ig_id",
        "access_token":access_token}

fb_url=f"https://graph.facebook.com/v19.0/{ig_id}"
base_url=f"https://graph.facebook.com/v19.0"
media=[]
post_params={"fields":"comments_count,like_count,media_url,thumbnail_url,permalink,timestamp,caption,comments",
             "access_token":access_token}

@app.route('/')
def allData():
    response=requests.get(fb_url,params=params).json()
    for i in response["media"]["data"]:
        media.append(i['id'])
    # with open("user_data.json",'w+') as file:
    #     json.dump([response],file)
    return response

@app.route('/all_posts_data')
def all_posts_data():
    post_data=[]
    for i in media:
        response=requests.get(f"{base_url}/{i}",params=post_params).json()
        post_data.append(response)
    # with open("post_data.json",'w+') as file:
    #     json.dump(post_data,file)
    return post_data


# ********************* Youtube data *********************

def get_channel_info(channel_id, ResultSize):
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

            channel_data = {
                "channel_title": channel_title,
                "subscriber_count": subscriber_count,
                "view_count": view_count,
                "total_videos": video_count,
                "videos": []
            }

            video_request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=ResultSize,
                type='video'
            )
            video_response = video_request.execute()

            if 'items' in video_response:
                for video in video_response['items']:
                    video_id = video['id']['videoId']
                    video_info = get_video_info(youtube, video_id)
                    channel_data["videos"].append(video_info)
            else:
                channel_data["error"] = "No videos found for this channel."

            return jsonify(channel_data)
        else:
            return jsonify({"error": "Channel not found or API quota exceeded."})

    except Exception as e:
        return jsonify({"error": str(e)})

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
        return {"error": "Video not found or API quota exceeded."}

@app.route(f"/get_channel_info/{channel_id}/{result_size}", methods=['GET'])
def get_yt_data():
    return get_channel_info(channel_id, result_size)
        
@app.route(f"/get_video_info/{channel_id}/{result_size}", methods=['GET'])
def get_video_info():
    return get_video_info(channel_id, result_size)        
