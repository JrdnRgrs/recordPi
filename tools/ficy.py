import os
import argparse

# MUST HAVE fIcy installed to work
# https://gitlab.com/wavexx/fIcy
parser = argparse.ArgumentParser(description='Python fIcy')
parser.add_argument("-o","--output", help="Specifies the path to the output file.", default="~/turntable.mp3")
parser.add_argument("-u","--host", help="Specifies the host url download the file from.", default="tt.tinymansell.com")
parser.add_argument("-m","--mount", help="Name of the mount (after the url) of the stream.", default="turntable.mp3")
args = parser.parse_args()
output=args.output
host=args.host
mount=args.mount
secs=10
port=80
def get_stream_recording(clip_path):
    os.system(f"fIcy -s .mp3 -n -o {clip_path} -M {secs} -d {host} {port} /{mount}")

get_stream_recording(output)
print(f"Saved file to {output}")