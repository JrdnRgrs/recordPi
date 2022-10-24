from envs import *
import os
from os.path import exists
import json
import requests
token = access_token
container=container_id
url = f"https://api-v2.acrcloud.com/api/fs-containers/{container}/files"
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
  }
def acr_fs_upload(file_path):
  file_name = os.path.basename(file_path)
  print(f"Using file: {file_path}")
  payload={'data_type': 'audio'}
  files=[
    ('file',(file_name,open(file_path,'rb'),'application/octet-stream'))
  ]
  
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  response.encoding = "utf-8"
  result_text=(response.text)
  json_string = json.loads(result_text)
  with open("up_data.json", 'w') as f:
    json.dump(json_string, f, ensure_ascii=False, indent=4)
  return json_string

def get_call(id):
  file_url = f"{url}/{id}"
  payload={}
  response = requests.request("GET", file_url, headers=headers, data=payload)
  response.encoding = "utf-8"
  result_text=(response.text)
  json_string = json.loads(result_text)
  return json_string

def del_call(id):
  file_url = f"{url}/{id}"
  payload={}
  response = requests.request("DELETE", file_url, headers=headers, data=payload)
  #response.encoding = "utf-8"
  #result_text=(response.text)
  #json_string = json.loads(result_text)
  return response


def save_data_file(data):
  good_data = data["data"][0]["results"]
  with open("response.json", 'w') as f:
    #json.dump(good_data, f, ensure_ascii=False, indent=4)
    json.dump(data, f, ensure_ascii=False, indent=4)
  with open("data.json", 'w') as f:
    json.dump(good_data, f, ensure_ascii=False, indent=4)

def acr_fs_get_info(id):
  my_result = get_call(id)
  save_data_file(my_result)
  results = my_result["data"][0]["results"]
  while not results:
    my_result = get_call(id)
    save_data_file(my_result)
    results=my_result["data"][0]["results"]
  #return json_string
  pretty_result = format_fs_info(my_result)
  return pretty_result

def delete_file(file_path):
    file_exists = exists(file_path)
    if file_exists:
        os.remove(file_path)

def format_fs_info(result):
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

def del_from_fs(id):
  my_result = del_call(id)
  #print(my_result)
  print(f"Deleted file ID: {id}")
