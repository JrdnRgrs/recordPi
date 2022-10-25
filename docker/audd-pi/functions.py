from envs import *
import os
import requests
import json

api_url="https://api.audd.io/"
def post_call(file_path,return_values):
    data = {
        'api_token': token,
        'return': return_values,
    }
    files = {
        'file' : open(file_path, "rb"),
    }
    response = requests.post(api_url, data=data, files = files)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

def save_data_file(data):
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

def audd_upload(file_path,return_values):
    print(f"Using file: {file_path}")
    json_string = post_call(file_path,return_values)
    save_data_file(json_string)
    #json_string = json.loads(response)
    pretty_result = format_result(json_string)
    return pretty_result

def format_result(r):
    artist = r["result"]["artist"]
    title = r["result"]["title"]
    album = r["result"]["album"]
    release_date = r["result"]["release_date"]
    release_year = release_date[0:4]
    arrAll = [artist, title, album, release_year]
    return arrAll

def clip_api_call():
    response = requests.request("GET", clip_api_url)
    response.encoding = "utf-8"
    result_text=(response.text)
    json_string = json.loads(result_text)
    return json_string

def should_run_api(clip_call):
    should_run = clip_call[0]["should_run"]
    if should_run:
        print("Audio Detected: The API will run")
        return True
    else:
        print("No Audio Detected: The API WILL NOT run")
        return False