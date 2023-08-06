FROM python:3.10-alpine
#USER root
#RUN apt update
#RUN apt upgrade -y
#RUN apk add build-base

COPY requirements.txt /usr/local/bin/requirements.txt
RUN cat /usr/local/bin/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install requests --upgrade

RUN pip3 install -r /usr/local/bin/requirements.txt
RUN pip3 freeze