from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment
import os
token = os.environ.get("api-token")
import requests
import json

def get_stream_recording():
    os.system("sudo fIcy -s .mp3 -o /recordings/turntable.mp3 -M 10 -d 192.168.1.244 8000 /turntable.mp3")


def get_audio_info(file = True, url = False, recordingFile="./recording.wav"):
    result = None
    recordingSeg = AudioSegment.from_file(recordingFile)
    loudness = recordingSeg.dBFS
    if loudness <= -55:
        print("The volume of the audio sample is too low.")
        return
    if file:
        files = {
            'file' : open(recordingFile, "rb"),
        }
        data = {
            'api_token': token,
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data, files = files)
    if url:
        data = {
            'api_token': token,
            'url': "https://tinymansell.com/audio/recording.wav", 
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
    #newJson = pp_json(jsonString)
    
    #return (str(tmp["result"]["title"]), str(tmp["result"]["artist"]))
    
    #return tmp

# Record 10 seconds of audio
#get_recording()

get_stream_recording()
get_audio_info(recordingFile="/recordings/turntable.mp3")
# Send recording to AuD and output response to data.json
#get_audio_info()