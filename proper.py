from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment
import os
token = os.environ.get("api-token")
import requests
import pyaudio
import wave
import json

def get_recording(recSeconds = 10, deviceIndex = 0,outputFilename='recording.wav'):
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = recSeconds
    dev_index = deviceIndex
    wav_output_filename = outputFilename

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def get_audio_info(file = True, url = False,recordingFile='./recording.wav'):
    result = None
    recordingSeg = AudioSegment.from_file(recordingFile)
    loudness = recordingSeg.dBFS
    if loudness <= -55:
        print("The volume of the audio sample is too low.")
        return
    if file:
        files = {
            'file' : open(recordingFile, "rb"),
        }
        data = {
            'api_token': token,
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data, files = files)
    if url:
        data = {
            'api_token': token,
            'url': "https://tinymansell.com/audio/recording.wav", 
            'return': 'timecode,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data)
    #tmp = result.json()
    #if (tmp["result"] == None):
    #    return (None, None)
    #print("title: " + str(tmp["result"]["title"]))
    #print("artist: " + str(tmp["result"]["artist"]))
    jsonString=(result.text)
    #newJson = pp_json(jsonString)
    with open('data.json', 'w') as f:
        json.dump(jsonString, f, ensure_ascii=False, indent=4)
    #return (str(tmp["result"]["title"]), str(tmp["result"]["artist"]))
    
    #return tmp

# Record 10 seconds of audio
get_recording()
# Send recording to AuD and output response to data.json
get_audio_info()