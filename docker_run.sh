#!/bin/sh
python3 record.py
docker run --name "recordPi" --rm -v /recordings/turntable.mp3:/recordings/turntable.mp3 --env-file ./.env python-docker