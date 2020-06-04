# FROM python:3.7-alpine
# WORKDIR /wpa
#
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .

FROM ubuntu:latest
WORKDIR /wpa
ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.8 python3.8-venv python3-pip\
    apache2 libapache2-mod-wsgi-py3 libmysqlclient-dev libmysqlclient21
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .