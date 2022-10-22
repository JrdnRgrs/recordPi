from functions import *
import argparse
parser = argparse.ArgumentParser(description='Python Tool for ACR File Scan API')

parser.add_argument("-f","--file", help="Specifies the file to upload to the api.", default="/recordings/turntable.mp3")
args = parser.parse_args()
upload_file=args.file

try:
    up_result = acr_fs_upload(upload_file)
    file_id= up_result["data"]["id"]
    print(f"Uploaded: {upload_file} to ACR, processing...")
    #file_id = ""
    get_result = acr_fs_get_info(file_id)
    print(get_result)
finally:
    print("Deleting from ACR...")
    del_from_fs(file_id)