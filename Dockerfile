# FROM python:3.7-alpine
# WORKDIR /wpa
#
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .

FROM ubuntu:latest
#WORKDIR /wpa
WORKDIR .
ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.8 python3-pip\
    apache2 libapache2-mod-wsgi-py3 libmysqlclient-dev libmysqlclient21
RUN ln /usr/bin/python3 /usr/bin/python
RUN ln /usr/bin/pip3 /usr/bin/pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm  /etc/apache2/sites-available/*
#COPY apache2_configuration /etc/apache2
COPY ./demo_site.conf /etc/apache2/sites-available/000-default.conf
#COPY . /var/www/html/

#RUN a2enmod rewrite  && a2ensite register && apache2ctl start
EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]
# && a2dissite 000-default default-ssl
#CMD ["apache2ctl", "-D", "FOREGROUND"]
#CMD ["apache2ctl", "-DFOREGROUND"]
