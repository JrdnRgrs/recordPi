from envs import *
from time import sleep
import os
import requests
import json
from os.path import exists
import base64
import hmac
import hashlib
import time

#### Shared Functions


def clip_api_call():
    response = requests.request("GET", clip_api_url)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

def clip_file_call():
    response =json.load(open(f'{clip_base_path}/clip.json'))
    clip_obj = response["clip"]
    return clip_obj

def should_run_api(clip_call):
    should_run = clip_call[0]["should_run"]
    if should_run:
        print("Audio Detected: The API will run")
        return True
    else:
        print("No Audio Detected: The API WILL NOT run")
        return False

def delete_file(file_path):
    file_exists = exists(file_path)
    if file_exists:
        os.remove(file_path)

### Audd Specific
audd_api_url="https://api.audd.io/"
def audd_post_call(file_path,return_values):
    data = {
        'api_token': audd_token,
        'return': return_values,
    }
    files = {
        'file' : open(file_path, "rb"),
    }
    response = requests.post(audd_api_url, data=data, files = files)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string
def audd_upload(file_path,return_values):
    print(f"Using file: {file_path}")
    json_string = audd_post_call(file_path,return_values)
    save_audd_data_file(json_string)
    #json_string = json.loads(response)
    pretty_result = format_audd_result(json_string)
    return pretty_result

def format_audd_result(r):
    artist = r["result"]["artist"]
    title = r["result"]["title"]
    album = r["result"]["album"]
    release_date = r["result"]["release_date"]
    release_year = release_date[0:4]
    arrAll = [artist, title, album, release_year]
    return arrAll

def save_audd_data_file(data):
    with open(f"{clip_base_path}/response.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    if data["status"] == "success":
        good_data = data["result"]
        out_data = {
            "music": [good_data]
        }
        with open(f"{clip_base_path}/data.json", 'w') as f:
            json.dump(out_data, f, ensure_ascii=False, indent=4)
    else:
        print("API Call was not a success. Check response.json for more information.")
#### ACR Cloud Specific
### ACR FS
acr_token = acr_access_token
acr_container = acr_container_id
acr_fs_url = f"https://api-v2.acrcloud.com/api/fs-containers/{acr_container}/files"
acr_fs_headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {acr_token}'
    }
def save_acr_fs_data_file(data):
  good_data = data["data"][0]["results"]
  with open("response.json", 'w') as f:
    #json.dump(good_data, f, ensure_ascii=False, indent=4)
    json.dump(data, f, ensure_ascii=False, indent=4)
  with open("data.json", 'w') as f:
    json.dump(good_data, f, ensure_ascii=False, indent=4)

## Upload to FS
# Writes to up_data.json and returns json object with the ID needed for GEt
def acr_fs_upload(file_path):
    file_name = os.path.basename(file_path)
    print(f"Using file: {file_path}")
    payload={'data_type': 'audio'}
    files=[
    ('file',(file_name,open(file_path,'rb'),'application/octet-stream'))
    ]

    response = requests.request("POST", acr_fs_url, headers=acr_fs_headers, data=payload, files=files)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    with open("up_data.json", 'w') as f:
        json.dump(json_string, f, ensure_ascii=False, indent=4)
    return json_string

# RAW CALL: (get_call) Get info from ACR based on ID of file uploaded to FS
# Takes in id from acr_fs_upload and returns output
# If not processed, will say ....
# If processed will, say ...
def acr_get_call(id):
    file_url = f"{acr_fs_url}/{id}"
    payload={}
    response = requests.request("GET", file_url, headers=acr_fs_headers, data=payload)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

# Get info info from ACR based on ID of file uploaded to FS
# Continuously use the acr_get_call function to update local data file
#   until a valid result is returned
def acr_fs_get_info(id):
  my_result = acr_get_call(id)
  #print(my_result)
  save_acr_fs_data_file(my_result)
  results = my_result["data"][0]["results"]
  while not results:
    my_result = acr_get_call(id)
    save_acr_fs_data_file(my_result)
    results=my_result["data"][0]["results"]
  #return json_string
  pretty_result = format_acr_fs_info(my_result)
  #print(pretty_result)
  return pretty_result

# Format info from fs get calls
def format_acr_fs_info(result):
    music_data_p = result["data"][0]["results"]["music"][0]
    valid_spotify = False
    valid_youtube = False
    music_data = music_data_p["result"]
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

# Delete file from ACR FS
# Delete once info has been retrieved
# Should have no response if succesful
def del_call(id):
  file_url = f"{acr_fs_url}/{id}"
  payload={}
  response = requests.request("DELETE", file_url, headers=acr_fs_headers, data=payload)
  #response.encoding = "utf-8"
  #result_text=(response.text)
  #json_string = json.loads(result_text)
  return response

# Wrapper around the del_call
def del_from_fs(id):
  my_result = del_call(id)
  #print(my_result)
  print(f"Deleted file ID: {id}")

#### ACR ID
acr_host = acr_id_host
acr_id_url = f"http://{acr_host}/v1/identify"
acr_key = acr_access_key
acr_secret = acr_access_secret

# Save the raw response to response.json, if successful:
#  save to data.json
def save_acr_id_data_file(data):
    with open(f"{clip_base_path}/response.json", 'w') as f:
    #json.dump(good_data, f, ensure_ascii=False, indent=4)
        json.dump(data, f, ensure_ascii=False, indent=4)
    if data["status"]["msg"] == "Success":
        good_data = data["metadata"]#["music"]
        del good_data["timestamp_utc"]
        with open(f"{clip_base_path}/data.json", 'w') as f:
            json.dump(good_data, f, ensure_ascii=False, indent=4)
    else:
        print("API Call was not a success. Check response.json for more information.")

# Return base64 encoded signature with the access key and secret 
def acr_id_sign_call(data_type,signature_version,timestamp):
    http_method = "POST"
    http_uri = "/v1/identify"
    string_to_sign = http_method + "\n" + http_uri + "\n" + acr_key + "\n" + data_type + "\n" + signature_version + "\n" + str(timestamp)
    sign = base64.b64encode(hmac.new(acr_secret.encode('ascii'), string_to_sign.encode('ascii'), digestmod=hashlib.sha1).digest()).decode('ascii')
    return sign

# Grab the file and sign it with the creds
# return the fully prepared data in the form:
#  [files,data]
def acr_id_prepare_data(file_path):
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    sign = acr_id_sign_call(data_type,signature_version,timestamp)
    f = open(file_path, "rb")
    sample_bytes = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    print(f"Using file: {file_path}")
    files = [
        ('sample', (file_name, f, 'audio/mpeg'))
    ]
    data = {'access_key': acr_key,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version}
    call_data = [files,data]
    return call_data

# HTTP Post to the ACR ID apit using the data in the form of [files,data]
def acr_id_post_call(files,data):
    response = requests.post(acr_id_url, files=files, data=data)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

# Pass prepared data to the post call function, format the result
def acr_id_api(file_path):
    call_data = acr_id_prepare_data(file_path)
    json_string = acr_id_post_call(call_data[0], call_data[1])
    save_acr_id_data_file(json_string)
    pretty_result = format_acr_id_info(json_string)
    return pretty_result

# Format ACR ID data
def format_acr_id_info(r):
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



