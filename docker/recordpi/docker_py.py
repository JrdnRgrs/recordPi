from dotenv import load_dotenv
from pydub import AudioSegment
import os
import requests
import json
import shutil
import string
import random
from time import sleep
from os.path import exists
from datetime import datetime
from datetime import timedelta

# Read Env Vars
load_dotenv()
token = os.environ.get("API_TOKEN")
url_flag = os.environ.get("URL_FLAG")
return_values = 'timecode,spotify'
audio_local_dir = "/recordings"
data_file_path = f"{audio_local_dir}/data.json"
clip_prefix = "turntable-"
recording_seconds = "11"
ice_host = "192.168.1.244 8000"
ice_port = "8000"
ice_mount = "/turntable.mp3"
url_prefix = "https://tinymansell.com/audio"
api_url="https://api.audd.io/"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def is_file_older_than (file, delta): 
    cutoff = datetime.utcnow() - delta
    mtime = datetime.utcfromtimestamp(os.path.getmtime(file))
    if mtime < cutoff:
        return True
    return False

def should_api_run(data_filename):
    data_file_exists = exists(data_filename)
    if data_file_exists:
        is_file_older_than(data_filename, timedelta(seconds=162))

def get_stream_recording(clip_path,recording_seconds,ice_host,ice_port,ice_mount):
    os.system(f"fIcy -s .mp3 -o {clip_path} -M {recording_seconds} -d {ice_host} {ice_port} {ice_mount}")

def download_stream_recording(clip_url,save_path):
    mr = requests.get(clip_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    if mr.status_code == 200:
        with open(save_path, 'wb') as f:
            mr.raw.decode_content = True
            shutil.copyfileobj(mr.raw, f)

def is_clip_quiet(clip_path):
    recordingSeg = AudioSegment.from_file(clip_path)
    loudness = recordingSeg.dBFS
    if loudness <= -55:
        print("The volume of the audio sample is too low.")
        return True
    else:
        return False

def delete_clip(clip_path_name):
    file_exists = exists(clip_path_name)
    if file_exists:
        os.remove(clip_path_name)

def api_call_url(api_token,clip_url,api_return_values,local_path_name):
    data = {
        'api_token': api_token,
        'url': clip_url,
        'return': api_return_values,
    }
    # Download the fIcy recorded file
    download_stream_recording(clip_url,local_path_name)
    # Test if the file is too quiet
    if is_clip_quiet(local_path_name):
        delete_clip(local_path_name)
        return
    result = requests.post(api_url, data=data)
    return result
def api_call_file(api_token,api_return_values,local_path_name):
    data = {
        'api_token': api_token,
        'return': api_return_values,
    }
    files = {
        'file' : open(local_path_name, "rb"),
    }
    # Test if the file is too quiet
    if is_clip_quiet(local_path_name):
        delete_clip(local_path_name)
        return
    result = requests.post(api_url, data=data, files = files)
    return result

def get_audio_info(aud_url,clip_path_name,file = False, url = True):
    result = None

    if file:
        result = api_call_file(token,return_values,path_name)

    if url:
        result = api_call_url(token,aud_url,return_values,clip_path_name)
    
    if not result:
        return

    result_text=(result.text)
    json_string = json.loads(result_text)
    delete_clip(clip_path_name)
    #file_exists = exists(clip_path_name)
    #if file_exists:
    #    os.remove(clip_path_name)
    if(result.status_code == requests.codes.ok):
        with open(data_file_path, 'w') as f:
            json.dump(json_string, f, ensure_ascii=False, indent=4)
        pretty_result = format_result(json_string)
        return pretty_result
    else:
        print(result_text)

    

def format_result(r):
    artist = r["result"]["artist"]
    title = r["result"]["title"]
    album = r["result"]["album"]
    release_date = r["result"]["release_date"]
    release_year = release_date[0:4]
    arrAll = [artist, title, album, release_year]
    return arrAll

def record_pi():
    call_num=id_generator(4)
    clip_file_name = f"{clip_prefix}-{call_num}.mp3"
    clip_path_name = f"{audio_local_dir}/{clip_file_name}"
    audio_clip_url = f"{url_prefix}/{clip_file_name}"
    # Record 10 seconds of audio from stream
    get_stream_recording(clip_path_name,recording_seconds,ice_host,ice_port,ice_mount)

    # Send recording to AuD and output response to data.json
    if url_flag == "no":
        recordPi = get_audio_info(clip_path_name=clip_path_name,url=False,file=True)
    else:
        recordPi = get_audio_info(audio_clip_url,clip_path_name,url=True,file=False)
    if recordPi:
        print(recordPi)

# Run idefinitely, sleeping for 30 seconds in between.
while True:
    print("Running RecordPi")
    record_pi()
    print("Sleeping for 30 seconds")
    sleep(30)
