FROM registry.gitlab.com/jrdnrgrs/recordpi/python-tools
WORKDIR /recordPi/
COPY . .
RUN pip3 install -r requirements.txt
ENV URL_FLAG "yes"
CMD [ "python3", "docker_py.py"]