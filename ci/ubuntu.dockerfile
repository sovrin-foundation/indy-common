# Development
FROM ubuntu:16.04

ARG uid=1000

# Install environment
RUN apt-get update -y
RUN apt-get install -y \ 
	git \
	wget \
	python3.5 \
	python3-pip \
	python-setuptools \
	python3-nacl
RUN pip3 install -U \ 
	pip \ 
	setuptools \
	virtualenv
RUN useradd -ms /bin/bash -u $uid sovrin
USER sovrin
RUN virtualenv -p python3.5 /home/sovrin/test
USER root
RUN ln -sf /home/sovrin/test/bin/python /usr/local/bin/python
RUN ln -sf /home/sovrin/test/bin/pip /usr/local/bin/pip
USER sovrin
WORKDIR /home/sovrin