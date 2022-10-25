from time import sleep
from functions import *

while True:
    try:
        clip_call_result = clip_api_call()
        file_name = clip_call_result[0]["clip_name"]
        upload_file = f"{clip_base_path}/{file_name}.mp3"
        should_run = should_run_api(clip_call_result)
        if should_run:
            print("Running RecordPi - Audd API")
            result=audd_upload(upload_file,return_values)
            print(result)
        else:
            print("To save on API calls, the API WILL NOT run.")
    finally:
        print("Sleeping for 60 seconds")
        sleep(60)
