import pyaudio
p = pyaudio.PyAudio()
#for ii in range(p.get_device_count()):
#    print(p.get_device_info_by_index(ii).get('name'))

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))