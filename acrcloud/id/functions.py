
from envs import *
import base64
import hashlib
import hmac
import os
import sys
import time

import requests
import json

requrl = f"http://{host}/v1/identify"

http_method = "POST"
http_uri = "/v1/identify"
# default is "fingerprint", it's for recognizing fingerprint, 
# if you want to identify audio, please change data_type="audio"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

def sign_call():
    
    string_to_sign = http_method + "\n" + http_uri + "\n" + access_key + "\n" + data_type + "\n" + signature_version + "\n" + str(
        timestamp)

    sign = base64.b64encode(hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                    digestmod=hashlib.sha1).digest()).decode('ascii')
    return sign

def prepare_data(file_path):
    sign = sign_call()
    f = open(file_path, "rb")
    sample_bytes = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    print(f"Using file: {file_path}")
    files = [
        ('sample', (file_name, f, 'audio/mpeg'))
    ]
    data = {'access_key': access_key,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version}
    call_data = [files,data]
    return call_data

def acr_id_api(file_path):
    call_data = prepare_data(file_path)
    json_string = post_call(call_data[0], call_data[1])
    save_data_file(json_string)
    pretty_result = format_result(json_string)
    return pretty_result

def post_call(files,data):
    response = requests.post(requrl, files=files, data=data)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

def save_data_file(data):
    with open("response.json", 'w') as f:
    #json.dump(good_data, f, ensure_ascii=False, indent=4)
        json.dump(data, f, ensure_ascii=False, indent=4)
    if data["status"]["msg"] == "Success":
        good_data = data["metadata"]#["music"]
        del good_data["timestamp_utc"]
        with open("data.json", 'w') as f:
            json.dump(good_data, f, ensure_ascii=False, indent=4)
    else:
        print("API Call was not a success. Check response.json for more information.")

def format_result(r):
    #time_stamp = r["metadata"]["timestamp_utc"]
    music_data_p = r["metadata"]["music"]
    music_data = music_data_p[0]
    valid_spotify = False
    valid_youtube = False
    album = music_data["album"]["name"]
    title = music_data["title"]
    artist = music_data["artists"][0]["name"]
    external_metadata = music_data["external_metadata"]
    if "spotify" in external_metadata:
        valid_spotify = True
        spotify_data = external_metadata["spotify"]
        spotify_artist = spotify_data["artists"][0]["name"]
        spotify_title = spotify_data["track"]["name"]
        spotify_album = spotify_data["album"]["name"]
    if "youtube" in external_metadata:
        valid_youtube = True
        youtube_suffix = external_metadata["youtube"]["vid"]
        youtube_url = f"http://youtu.be/{youtube_suffix}"
    release_date = music_data["release_date"]
    release_year = release_date[0:4]
    if valid_spotify and valid_youtube:
        arrAll = [spotify_title, spotify_artist, spotify_album, release_year, youtube_url]
    else:
        arrAll = [title, artist, album, release_year]
    return arrAll
