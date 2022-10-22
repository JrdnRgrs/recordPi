# Record Pi 3.0 (once more with feeling)

The third try at trying to identify the songs I am listening to on my record player.

## Background

This idea has had many iterations, but this is the 2022 version, this time with more knowledge.

### Pre Reqs

See [Hardware.md](./Hardware.md) for details on the backend set up. That is the easy part.

### Grabbing and Identifying the Audio

You will need [fIcy](https://gitlab.com/wavexx/fIcy) on your machine for this. See the link for installation instructions.

fIcy will take the URL of a stream and record a clip for us to pass to the APIs. Usually, you'd run this:

``` sh
sudo fIcy -s .mp3 -o {recordingFile} -M 10 -d {host} {port} {mount}
```

I have simplified this down to [./tools/ficy.py](./tools/ficy.py) for ease of use. You can now run it like this:

``` python
python3 ./tools/ficy.py -o /recordings/turntable.mp3 -u {stream_host} -m {stream_mount}
```

-o, --output - output file. You'll pass this into the other scripts later.
-u, --host - host of the stream to record from. For this project, this is the icecast server.
-m, --mount - icecast mount/endpoint. (ex: stream.mp3)

Now we have a 10 second recording of our stream at `/recordings/turntable.mp3` to give to an API.

## Music Recognition Services

### Audd.io

- Very simple API.
- 1000 requests a month for $5
- $5 for every 1000 after

- [Dashboard](https://dashboard.audd.io/)

Entry Script

``` python
python3 ./audd/audd.py -f /recordings/turntable.mp3
```

### ACR Cloud

2 tools for recognition:

- Identify API
- File Scanner

Pricing is unknown, but could be anywhere from 100-1000 requests a month for free.

- [Identify Projects](https://console.acrcloud.com/avr?region=us-west-2#/projects/online) (upload)
- [File Scanning Containers](https://console.acrcloud.com/filescanning?region=us-west-2#/fs-containers) (upload+url)

Entry Scripts

ID API

``` python
python3 ./acrcloud/id/acr_id.py -f /recordings/turntable.mp3
```

File Scan API

``` python
python3 ./acrcloud/fs/acr_fs.py -f /recordings/turntable.mp3
```

### Shazam API

A bit stricter rules for uploading, but can do it with smaller files.

500 requests a month for free

5000 requests a month for $20, + $0.02 each other

- [Web Api](https://rapidapi.com/apidojo/api/shazam)

### audiotag.info

Archaic, can't even get it to work.

- 100k credits - $40 (double free monthly)

- [Docs](https://user.audiotag.info/doc/AudioTag-API.pdf)
- [Dashboard](https://user.audiotag.info/)