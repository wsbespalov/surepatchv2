FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
COPY . /surepatch
WORKDIR /surepatch
RUN pip3 install -r requirements.txt
CMD ["/bin/bash"]