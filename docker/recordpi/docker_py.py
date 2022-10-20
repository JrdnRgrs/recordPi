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

def get_audio_info(file = True, url = False):
    result = None

    if file:
        recordingSeg = AudioSegment.from_file(path_name)
        loudness = recordingSeg.dBFS
        if loudness <= -55:
            print("The volume of the audio sample is too low.")
            return
        files = {
            'file' : open(path_name, "rb"),
        }
        data = {
            'api_token': token,
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data, files = files)
    if url:
        file_exists = exists(path_name)
#        if file_exists:
#             sleep(10)
        mr = requests.get(audio_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        if mr.status_code == 200:
            with open(path_name, 'wb') as f:
                mr.raw.decode_content = True
                shutil.copyfileobj(mr.raw, f)
        recordingSeg = AudioSegment.from_file(path_name)
        loudness = recordingSeg.dBFS
        #print(f"Using audio_url: {audio_url}")
        if loudness <= -55:
            print("The volume of the audio sample is too low.")
            return
        data = {
            'api_token': token,
            'url': audio_url,
            'return': 'timecode,spotify',
        }
#        sleep(1)
#        run_api = should_api_run()
#        while run_api == False:
#            sleep(10)
#            run_api = should_api_run()
#        if run_api:
        result = requests.post('https://api.audd.io/', data=data)
    print(result.text)
    #jsonString=(result.text)
    if file_exists:
        #sleep(3)
        os.remove(path_name)
    r = json.loads(result.text)
    if(result.status_code == requests.codes.ok):
        with open(data_filename, 'w') as f:
            json.dump(r, f, ensure_ascii=False, indent=4)
        artist = r["result"]["artist"]
        title = r["result"]["title"]
        album = r["result"]["album"]
        release_date = r["result"]["release_date"]
        release_year = release_date[0:4]
        #songUrl = r["result"]["spotify"]["external_urls"]["spotify"]
        #artistUrl = r["result"]["spotify"]["album"]["artists"][0]["external_urls"]["spotify"]
        #imageLink = r["result"]["spotify"]["album"]["images"][0]["url"]
        #arrAll = [artist, title, album, songUrl, artistUrl, imageLink]
        arrAll = [artist, title, album, release_date]
        #outPrint1 = f"{title} - {artist}"
        #outPrint2 = f"{album} ({release_year})"
        #print(outPrint1)
        #print(outPrint2)
        return arrAll
    else:
        print(result.text)

# Record 10 seconds of audio from stream
#get_stream_recording()

# Send recording to AuD and output response to data.json
if url_flag == "yes":
    get_stream_recording()
    get_audio_info(url=True,file=False)
    #recordPi = get_audio_info(url=True,file=False)
else:
    get_stream_recording()
    get_audio_info()
#recordPi = get_audio_info()

#if recordPi:
#    print(recordPi)
