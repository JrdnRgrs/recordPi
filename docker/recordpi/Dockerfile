FROM python:slim
WORKDIR /recordpi
COPY *.py ./
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "docker_py.py"]