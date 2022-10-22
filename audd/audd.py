from functions import *
import argparse

parser = argparse.ArgumentParser(description='Audd Tool for Python')

parser.add_argument("-f","--file", help="Specifies the file to upload to the api.", default="/recordings/turntable.mp3")
parser.add_argument("-r","--return_values", help="Specifies the values to return.", default='timecode,spotify')
args = parser.parse_args()
upload_file=args.file
return_values=args.return_values
result=audd_upload(upload_file,return_values)
print(result)
