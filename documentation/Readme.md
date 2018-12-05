# Installation Guide - Work in Progress

We use Openshift in our environment. We recommend you setup an openshift (or minishift) for this project. You can then use our build / deployment configs found in the openshift directory.

## Key features of the platform:

Jenkins Build process includes:

- SonarQube
- Building our Flask/Python API
- Building our Vue FrontEnd and copying the output to CADDY Webserver
- Postman tests
- Zap Vulnerability tests

If you want to just try out the application, here are some instructions to get it running on Ubuntu (I used Windows 10 WSL Ubuntu):

- Note we do not use RabbitMQ for local testing but this is used to manage multiple pods and syncing messages between them.

## Setup MySQL instance & run it:

1. `sudo apt-get install mysql-server`
1. `sudo service mysql start`
1. `sudo mysql --defaults-file=/etc/mysql/debian.cnf`
1. `CREATE USER 'demo'@'localhost' IDENTIFIED BY 'demo';`
1. `GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost';`
1. `CREATE DATABASE IF NOT EXISTS queue_management;`
1. `FLUSH PRIVILEGES;`

## Setup docker & install Keycloak:

1. `git clone https://github.com/bcgov/queue-management.git`
1. `export DOCKER_HOST=tcp://0.0.0.0:2375`
1. `cd queue-management/keycloak-local-testserver`
1. `chmod +x *.sh`
1. `docker build -t keycloak .`
1. `docker run -it --name keycloak -p 8085:8080 keycloak`

You should be able to login in with admin/admin on http://localhost:8085/auth

## Setup Flask Python API Container:

Ensure you have python 3. I also had to install: gcc, python3-venv, libmysqlclient-dev and python3-dev installed.

### Setup API Server:

1. `python3 -m venv env`
1. `source env/bin/activate`
1. `cd queue-management/api`
1. `pip3 install -r requirements.txt`

### Add two required keycloak config files

1. `cd queue-management`
1. `cp documentation/demo-files/secrets.json api/client_secrets/secrets.json`
1. `cp documentation/demo-files/keycloak-local.json frontend/static/keycloak-local.json`

### Set Enviornment Variables required:

1. `export DATABASE_ENGINE=mysql`
1. `export DATABASE_USERNAME=demo`
1. `export DATABASE_PASSWORD=demo`
1. `export DATABASE_NAME=queue_management`
1. `export DATABASE_HOST=127.0.0.1`
1. `export DATABASE_PORT=3306`
1. `export THEQ_SNOWPLOW_CALLFLAG=False`

### Update Database with required tables:

1. `python3 manage.py db upgrade`

### Update the Database with demo data:

1. `python3 manage.py bootstrap`

### Run API Server:

1. `python3 -m flask run`

## Setup for  FrontEnd Development

Install npm:

1. `sudo apt-get install npm`
1. `/usr/bin/npm install`

## To Start FRONTEND:

1. `npm start localhost`

**IMPORTANT: To login, use the Keycloak Login link at the bottom right hand corner. The main login is used with Single Signon integration to our Enterprise Active Directory Domain.**

You should be able to login in using the following IDs:  
user/user - Regular Customer Service Representative (CSR)  
admin/admin - Manager of the office (Government Agent)

Additional API Enviornment Variables of note:

1. SECRET_KEY - Flask required key
1. SLACK_URL - used to send feedback to Slack (Will be integrating ServiceNOW soon)
1. THEQ_CLEAR_COMMENTS_FLAG - used to not remove comments for debugging purposes
1. THEQ_SNOWPLOW_ENDPOINT - Snowplow URL
1. THEQ_SNOWPLOW_APPID - Snowplow Application ID
1. THEQ_SNOWPLOW_NAMESPACE - Snowplow NameSpace
1. THEQ_SNOWPLOW_CALLFLAG (True/False) - Used to disable calls to SnowPlow
1. SERVER_NAME - required for API POD if not localhost.
1. LOG_ERRORS (True/Flase) - To log socket.io errors
1. THEQ_FEEDBACK - String of endpoint names to send Feedback to (eg. 'Slack, Service Now' or 'Slack')
1. SERVICENOW_INSTANCE - the instance of your Service Now environment
1. SERVICENOW_USER - the login ID of a Service Now ID used to create Service Now incidents
1. SERVICENOW_PASSWORD - the password of the SERVICENOW_USER account

We are using Snowplow & Looker to display our Analytics.

For more information, please see the following repositories:

- https://github.com/bcgov/GDX-Analytics
- https://github.com/bcgov/GDX-Analytics-Looker-cfms_block

# Running Tests

There are JEST tests as well but I am still working on integrating them to our pipeline. The can be manually run by typing: npm test in the frontend folder.

For tests to run, you require two additional IDs created in your keycloak:

- cfms-postman-non-operator
- cfms-postman-operator

## Postman Tests

Below is an example suing the localhost keycloak created above:

- Create users & set passwords for the postman users in your keycloak instance:

1. cfms-postman-operator
1. cfms-postman-non-operator

Go \queue-manaement\api\postman & run the following command:

1. npm install newman

You will need the following information:

1. password_qtxn=<cfms-postman-operator userid password>
1. password_nonqtxn=<cfms-postman-non-operator userid password>
1. client_secret=5abdcb03-9dc6-4789-8c1f-8230c7d7cb79
1. url=http://localhost:5000/api/v1/
1. auth_url=http://localhost:8085
1. clientid=account
1. realm=registry

For this test, I created the password for the two users as demo. From the postman folder run the following command to run the postman tests:

`./node_modules/newman/bin/newman.js run postman_tests.json -e postman_env.json --global-var password=demo --global-var password_nonqtxn=demo --global-var client_secret=5abdcb03-9dc6-4789-8c1f-8230c7d7cb79 --global-var url=http://localhost:5000/api/v1/ --global-var auth_url=http://localhost:8085 --global-var clientid=account --global-var realm=registry`

## Jest Test

### Setup For Jest tests

- Note this doesn't work with Windows 10 WSL
- You can also run this headless if you update queue-management/frontend/src/test/index.test.js file and change "headless" setting from false to true.
- If you having installed the requirements for the frontend on this box also install puppateer. Use this command: `npm install puppateer`

1. `export CFMS_DEV_URL=http://localhost:8080`
1. `export POSTMAN_OPERATOR_PASSWORD=keycloak password`

### Run tests

From the queue-management/frontend folder run the following command:

1. npm test

You should now see a chromium browser open and go through the tests we created.
