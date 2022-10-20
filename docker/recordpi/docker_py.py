from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment
import os
token = os.environ.get("API_TOKEN")
url_flag = os.environ.get("URL_FLAG")
import requests
import json
import shutil
import string
import random
from time import sleep
from os.path import exists
from datetime import datetime
from datetime import timedelta

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

myNum=id_generator(4)
file_name = f"turntable-{myNum}.mp3"
path_name = f"/recordings/{file_name}"
audio_url = f"https://tinymansell.com/audio/{file_name}"
data_filename = "/recordings/data.json"
return_values = 'timecode,spotify'

def is_file_older_than (file, delta): 
    cutoff = datetime.utcnow() - delta
    mtime = datetime.utcfromtimestamp(os.path.getmtime(file))
    if mtime < cutoff:
        return True
    return False

def should_api_run():
    data_file_exists = exists(data_filename)
    if data_file_exists:
        is_file_older_than(data_filename, timedelta(seconds=162))

def get_stream_recording():
    #os.system(f"fIcy -s .mp3 -o /recordings/turntable.mp3 -M 10 -d 192.168.1.244 8000 /turntable.mp3")
    os.system(f"fIcy -s .mp3 -o {path_name} -M 10 -d 192.168.1.244 8000 /turntable.mp3")

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
        return
    result = requests.post('https://api.audd.io/', data=data)
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
        return
    result = requests.post('https://api.audd.io/', data=data, files = files)
    return result

def get_audio_info(file = True, url = False):
    result = None

    if file:
        result = api_call_file(token,return_values,path_name)

    if url:
        result = api_call_url(token,audio_url,return_values,path_name)
    
    jsonString=(result.text)
    #print(jsonString)
    file_exists = exists(path_name)
    if file_exists:
        #sleep(3)
        os.remove(path_name)
    r = json.loads(jsonString)
    if(result.status_code == requests.codes.ok):
        with open(data_filename, 'w') as f:
            json.dump(r, f, ensure_ascii=False, indent=4)
        artist = r["result"]["artist"]
        title = r["result"]["title"]
        album = r["result"]["album"]
        release_date = r["result"]["release_date"]
        release_year = release_date[0:4]
        arrAll = [artist, title, album, release_year]
        return arrAll
    else:
        print(jsonString)

# Record 10 seconds of audio from stream
get_stream_recording()
# Send recording to AuD and output response to data.json
if url_flag == "yes":
    recordPi = get_audio_info(url=True,file=False)
else:
    recordPi = get_audio_info()

if recordPi:
    print(recordPi)
