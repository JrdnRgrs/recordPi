FROM python:slim
RUN apt-get update && apt-get install -y ffmpeg make build-essential wget nano
RUN wget "https://www.thregr.org/~wavexx/software/fIcy/releases/fIcy-1.0.21.tar.gz" && tar -xvzf fIcy-1.0.21.tar.gz && mv fIcy-1.0.21/ /fIcy/
WORKDIR /fIcy/
RUN make install
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt