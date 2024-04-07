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
youtube = build('youtube', 'v3', developerKey=API_KEY)


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

@app.route("/getChannelInfo/<string:_channel_id>")
def ChannelInfo(_channel_id):
    channel_id = _channel_id
    return jsonify(get_channel_info(channel_id))

@app.route("/getVideos/<string:channel_id>/<int:result_size>")
def VideoInfo(channel_id, result_size):
    return jsonify(get_video_info(channel_id, result_size))


@app.route("/getVideos")
def Video():
    result = {
        "Not Found":"give channel_id and result size"
    }
    return jsonify(result)
