# wpa-membership2

This web application manages memberships for the Woodley Park Archers. 
This site is designed to be a subdomain of another site.

The application is used for: membership registration, membership renewal, JOAD registration, JOAD pin shoots

The application is written in python, uses MySQL for the database, and is intended to run on appache2 web server 
with mod_wsgi. It uses Square's API to charge credit cards for the registration, renewal, pin shoot, and pins.

The file settings.cfg holds the configuration settings for the application. Such as the database settings, 
Gmail settings, and costs.

### `Requirements`

Python 3 >= 3.4 with the following packages: 
flask
flask-session
pymysql
squareup
python-dateutil

### `Setup`
clone the repository to a folder accessible to the web server. 
Copy settings_template.cfg to settings.cfg and adjust the settings to meet your needs.