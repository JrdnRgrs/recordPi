from envs import *
import os
import time
import random
import string
import json
from pydub import AudioSegment
# MUST HAVE fIcy and ffmpeg installed to work
# https://gitlab.com/wavexx/fIcy

### Functions
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_stream_recording(clip_suffix,secs=recording_secs,host=ice_host,port=ice_port,mount=ice_mount):
    clip_path = f"{clip_base_path}/{clip_base_name}-{clip_suffix}.mp3"
    os.system(f"fIcy -s .mp3 -o {clip_path} -M {secs} -d {host} {port} /{mount}")
    return clip_path

def delete_old_clips():
    with os.scandir(clip_base_path) as listOfEntries:
        for entry in listOfEntries:
            if f"{clip_base_name}-" in entry.name:
                age = time.time() - entry.stat().st_mtime
                if age > 180:
                    os.remove(os.path.join(clip_base_path, entry.name))

def get_clip_suffix(num_digits):
    clip_suffix=id_generator(num_digits)
    return clip_suffix

def is_clip_quiet(clip_path):
    recordingSeg = AudioSegment.from_file(clip_path)
    loudness = recordingSeg.dBFS
    if loudness <= -55:
        print("The volume of the audio sample is too low.")
        return True
    else:
        return False

def prepare_api_data(clip_name,suffix,should_run):
    data = json.load(open('clip.json'))
    data["clip"][0]["clip_name"] = clip_name
    data["clip"][0]["clip_suffix"] = suffix
    data["clip"][0]["should_run"] = should_run
    return data

def set_api_data(clip_name,suffix,should_run):
    data = prepare_api_data(clip_name,suffix,should_run)
    with open(f"{clip_base_path}/clip.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)