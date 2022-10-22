from functions import *
import argparse
parser = argparse.ArgumentParser(description='Python Tool for ACR ID API')

parser.add_argument("-f","--file", help="Specifies the file to upload to the api.", default="/recordings/turntable.mp3")
args = parser.parse_args()
upload_file=args.file


result = acr_id_api(upload_file)
print(result)