from functions import *
### Individual Wrapper functions

# Aud
def audd_api_wrapper():
    #while True:
    try:
        # To run this against the clip api
        #clip_call_result = clip_api_call()
        # To run this against a local file instead of using clip api
        # The main difference (for now) is that with the api you can check to make sure everything is moving
        clip_call_result = clip_file_call()
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
# ACR FS
def acr_fs_api_wrapper():
    #while True:
    try:
        clip_call_result = clip_file_call()
        file_name = clip_call_result[0]["clip_name"]
        upload_file = f"{clip_base_path}/{file_name}.mp3"
        should_run = should_run_api(clip_call_result)
        if should_run:
            print("Running RecordPi - ACR FS API")
            up_result = acr_fs_upload(upload_file)
            sleep(2)
            file_id= up_result["data"]["id"]
            print(f"Uploaded: {upload_file} to ACR, processing...")
            get_result = acr_fs_get_info(file_id)
            print(get_result)
        else:
            print("To save on API calls, the API WILL NOT run.")
    finally:
        print("Deleting from ACR...")
        del_from_fs(file_id)
        print("Sleeping for 60 seconds")
        sleep(60)
# ACR ID
def acr_id_api_wrapper():
    try:
        clip_call_result = clip_file_call()
        file_name = clip_call_result[0]["clip_name"]
        upload_file = f"{clip_base_path}/{file_name}.mp3"
        should_run = should_run_api(clip_call_result)
        if should_run:
            print("Running RecordPi - ACR ID API")
            result = acr_id_api(upload_file)
            print(result)
        else:
            print("To save on API calls, the API WILL NOT run.")
    finally:
        print("Sleeping for 60 seconds")
        sleep(60)