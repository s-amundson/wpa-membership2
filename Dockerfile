
FROM ubuntu:latest

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
COPY ./apache2_configuration/sites-available/register.conf /etc/apache2/sites-available/000-default.conf
#RUN python /var/www/wpa/manage.py qcluster --settings=wpa.local_settings &
# RUN python manage.py collectstatic -l --no-input --settings=wpa.local_settings
EXPOSE 80 443
CMD ["apache2ctl", "-D", "FOREGROUND"]

