FROM registry.gitlab.com/jrdnrgrs/recordpi/python-tools
WORKDIR /recordPi/
COPY docker_py docker_py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV URL_FLAG "no"
CMD [ "python3", "docker_py.py"]