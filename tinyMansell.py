from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment
import os
token = os.environ.get("API_TOKEN")
import requests
import json
recordingFile = "/recordings/turntable.mp3"
host = "192.168.1.244"
port = "8000"
mount = "/turntable.mp3"
def get_stream_recording():
    os.system(f"sudo fIcy -s .mp3 -o {recordingFile} -M 10 -d {host} {port} {mount}")


def get_audio_info(file = True, url = False):
    result = None
    recordingSeg = AudioSegment.from_file("/recordings/turntable.mp3")
    loudness = recordingSeg.dBFS
    if loudness <= -55:
        print("The volume of the audio sample is too low.")
        return
    if file:
        files = {
            'file' : open("/recordings/turntable.mp3", "rb"),
        }
        data = {
            'api_token': token,
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data, files = files)
    if url:
        data = {
            'api_token': token,
            'url': "https://tinymansell.com/audio/turntable.mp3", 
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data)
    r = json.loads(result.text)
    if(result.status_code == requests.codes.ok):
        artist = r["result"]["artist"]
        title = r["result"]["title"]
        album = r["result"]["album"]
        release_date = r["result"]["release_date"]
        release_year = release_date[0:4]
        songUrl = r["result"]["spotify"]["external_urls"]["spotify"]
        artistUrl = r["result"]["spotify"]["album"]["artists"][0]["external_urls"]["spotify"]
        imageLink = r["result"]["spotify"]["album"]["images"][0]["url"]
    arrAll = [artist, title, album, songUrl, artistUrl, imageLink]
    #jsonString=(result.text)
    with open('data.json', 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)
    outPrint1 = f"{title} - {artist}"
    outPrint2 = f"{album} ({release_year})"
    print(outPrint1)
    print(outPrint2)
    return arrAll


# Record 10 seconds of audio from stream
get_stream_recording()

# Send recording to AuD and output response to data.json
get_audio_info()
