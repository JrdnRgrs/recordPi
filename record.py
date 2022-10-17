import os
recordingFile = "/recordings/turntable.mp3"
host = "192.168.1.244"
port = "8000"
mount = "/turntable.mp3"
def get_stream_recording():
    os.system(f"sudo fIcy -s .mp3 -o {recordingFile} -M 10 -d {host} {port} {mount}")

get_stream_recording()