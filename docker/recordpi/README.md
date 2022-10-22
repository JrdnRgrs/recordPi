First, save your api token to `.env` as `API_TOKEN`

This will record 10 seconds of audio from the stream, upload to the API and print the song, artist, and album, while outputting the raw json to `data.json` at an s3 bucket

```
docker build --tag recordpi .
```

Once built, you can run it with the following command, or just run the `docker_run.sh` file which will do everything for you all at once, or

```
docker run --name "recordPi" --rm -v /media/Library/docker/apache/basic/audio/:/recordings/ --env-file ./.env registry.gitlab.com/jrdnrgrs/recordpi
```

One last thing I added was to add a volume on the above docker container that is created so that the data.json file written in the end is written to a path where an apache server is serving. This is more of just a proof of concept of a super simple "API" for this service..