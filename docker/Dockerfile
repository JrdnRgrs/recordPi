FROM python
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN apt-get update && apt-get install -y ffmpeg
ENV URL_FLAG "yes"
CMD [ "python3", "docker_py.py"]