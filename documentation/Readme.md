# Installation Guide - Work in Progress

We use Openshift in our environment. We recommend you setup an openshift (or minishift) for this project. You can then use our build / deployment configs found in the openshift directory.

## Key features of the platform:

Jenkins Build process includes:

- SonarQube
- Building our Flask/Python API
- Building our Vue FrontEnd and copying the output to CADDY Webserver
- Postman tests
- Zap Vulnerability tests

There are JEST tests as well but I am still working on integrating them to our pipeline. The can be manually run by typing: npm test in the frontend folder.

They require the following environment Variables to be set:

export CFMS_DEV_URL="http://localhost:8080"
export POSTMAN_OPERATOR_PASSWORD= "keycloak password"

Additionally, for the Postman and Jest Tests, you require two additional IDs created in keycloak:

- cfms-postman-non-operator
- cfms-postman-operator

If you want to just try out the application, here are some instructions to get it running on Ubuntu (I used Windows 10 WSL Ubuntu):

- Note we do not use RabbitMQ for local testing but this is used to manage multiple pods and syncing messages between them.

## Setup MySQL instance & run it:

1. ```sudo apt-get install mysql-server```
1. ```sudo service mysql start```
1. ```sudo mysql --defaults-file=/etc/mysql/debian.cnf```
1. ```CREATE USER 'demo'@'localhost' IDENTIFIED BY 'demo';```
1. ```GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost';```
1. ```CREATE DATABASE IF NOT EXISTS queue_management;```
1. ```FLUSH PRIVILEGES;```

## Setup docker & install Keycloak:

1. ```git clone https://github.com/bcgov/queue-management.git```
1. ```export DOCKER_HOST=tcp://0.0.0.0:2375```
1. ```cd /queue-management/keycloak-local-testserver```
1. ```docker build -t keycloak .```
1. ```docker run -it --name keycloak -p 8085:8080 keycloak```

You should be able to login in with admin/admin  on http://localhost:8085/auth

## Setup Flask Python API Container:

Ensure you have python 3. I also had to install: gcc, python3-venv, libmysqlclient-dev and python3-dev installed.

### Setup API Server:

1. ```python3 -m venv env```
1. ```source env/bin/activate```
1. ```cd /queue-management/api```
1. ```pip3 install -r requirements.txt```

### Add two required keycloak config files

1. ```cp /queue-management/documentation/demo-files/secrets.json /queue-management/api/client_secrets/secrets.json```
1. ```cp /queue-management/documentation/demo-files/keycloak-local.json /queue-management/frontend/static/keycloak-local.json```

### Set Enviornment Variables required:

1. ```export DATABASE_ENGINE=mysql```
1. ```export DATABASE_USERNAME=demo```
1. ```export DATABASE_PASSWORD=demo```
1. ```export DATABASE_NAME=queue_management```
1. ```export DATABASE_HOST=127.0.0.1```
1. ```export DATABASE_PORT=3306```
1. ```export THEQ_SNOWPLOW_CALLFLAG=False```

### Update Database with required tables:

1. ```python3 manage.py db upgrade```

### Update the Database with demo data:

1. ```python3 manage.py bootstrap```

### Run API Server:

1. ```python3 -m flask run```

## Setup for  FrontEnd Development

Install npm:

1. ```sudo apt-get install npm```
1. ```/usr/bin/npm install```

## To Start FRONTEND:

1. ```npm start localhost```

**IMPORTANT: To login, use the Keycloak Login link at the bottom right hand corner. The main login is used with Single Signon integration to our Enterprise Active Directory Domain.**

You should be able to login in using the following IDs:  
user/user - Regular Customer Service Representative (CSR)  
admin/admin - Manager of the office (Government Agent)  



Additional API Enviornment Variables of note:

1. SECRET_KEY - Keycloak client key
1. SLACK_URL - used to send feedback to Slack
1. THEQ_CLEAR_COMMENTS_FLAG - used to not remove comments for debugging purposes
1. THEQ_SNOWPLOW_ENDPOINT - Snowplow URL
1. THEQ_SNOWPLOW_APPID - Snowplow Application ID
1. THEQ_SNOWPLOW_NAMESPACE - Snowplow NameSpace
1. THEQ_SNOWPLOW_CALLFLAG (True/False) - Used to disable calls to SnowPlow

We are using Snowplow & Looker to display our Analytics.

For more information, please see the following repositories:

https://github.com/bcgov/GDX-Analytics
https://github.com/bcgov/GDX-Analytics-Looker-cfms_block
