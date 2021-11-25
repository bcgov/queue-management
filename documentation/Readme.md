# Installation Guide - Work in Progress

We use OpenShift in our environment. We recommend you setup an OpenShift (or Red Hat CodeReady Containers) for this project. You can then use our build / deployment configs found in the openshift directory.

## Key features of the platform:

Jenkins Build process includes:

- SonarQube
- Building our Flask/Python API
- Building our Vue FrontEnd and copying the output to CADDY Webserver
- Postman tests
- Zap Vulnerability tests

## Running the code with VSCode Remote - Containers

TODO: blurb

Clone the code in this repo:

```
$ git clone https://github.com/bcgov/queue-management
```

Opening the cloned repo in VSCode will detect the *.devcontainer* directory and recommend that you re-open in *Remote - Containers*. This will build and start the docker containers that are needed.

The first time VSCode switches to the container, you have to populate the empty database with:
```
/workspace$ (cd api; env/bin/python manage.py bootstrap)
```

## TODO: Complete these.

Set up FAQ. How do I...
1. Launch
1. APIs debugging, hot reload
1. Front Ends, hot reload?
1. Run Python tests?
1. Run newman tests?
1. Run Jest tests?
1. Update requirements.txt?
1. Update packages.json?
1. Change python version?
1. Change node version?
1. Change PostgreSQL version?
1. Wipe DB?
1. Do stuff in Keycloak?
1. Do stuff with analytics?
1. What else?

### Configure Keycloak

TODO: this will change when we have a Keycloak pod.

```
queue-management$ mkdir api/client_secrets
queue-management$ cp documentation/demo-files/secrets.json api/client_secrets/
queue-management$ cp documentation/demo-files/keycloak.json frontend/static/
```

TODO: .env file for API, once we have docker keycloak.
TODO: configuration.json file for frontend.

# TODO: REMOVE/REVISE/INCLUDE EVERYTHING BELOW

## Running with Ubuntu
If you want to just try out the application, here are some instructions to get it running on Ubuntu (I used Windows 10 WSL Ubuntu):

- Note we do not use RabbitMQ for local testing but this is used to manage multiple pods and syncing messages between them.

## Setup Postgresql instance & run it:

1. `sudo apt-get install postgresql`
1. `sudo passwd postgres`
1. `Enter password: postgres`
1. `sudo service postgresql start`
1. `sudo -u postgres createuser demo`
1. `sudo -u postgres createdb queue_management`
1. `sudo -u postgres psql`
1. `alter user demo with encrypted password 'demo';`
1. `grant all privileges on database queue_management to demo ;`

## Setup docker & install Keycloak:

1. `git clone https://github.com/bcgov/queue-management.git`
1. `export DOCKER_HOST=tcp://0.0.0.0:2375`
1. `cd queue-management/keycloak-local-testserver`
1. `chmod +x *.sh`
1. `docker build -t keycloak .`
1. `docker run -it --name keycloak -p 8085:8080 keycloak`

You should be able to login in with admin/admin on http://localhost:8085/auth
1. Go to Groups, add new.  theq_internal_user
1. Go to Users, view all users, edit 'admin', 
    - under Groups, under Available Groups, join theq_internal_user
    - under Role Mappings, select internal_user, add selected, should see under assigned role
1. Go to Clients, edit account, scope, set full scope allowed to ON
## Setup Flask Python API Container:

Ensure you have python 3. I also had to install: gcc, python3-venv, libmysqlclient-dev and python3-dev installed.

### Setup API Server:

1. `python3 -m venv env`
1. `source env/bin/activate`
1. `cd queue-management/api`
1. `pip3 install -r requirements.txt`

### Copy two required files to the correct place in your directory structure

1. `cd queue-management`
1. `cp documentation/demo-files/keycloak.json frontend/static/keycloak.json`
1. `cd api`
1. `mkdir client_secrets`
1. `cd ..`
1. `cp documentation/demo-files/secrets.json api/client_secrets/secrets.json`

### Set Environment Variables required:

1. `cd queue-management`
1. `cp documentation/demo-files/.env .`

### Update Database with required tables:

1. `python3 manage.py db upgrade`

### Update the Database with demo data:

1. `python3 manage.py bootstrap`

### Run API Server:

1. `gunicorn wsgi --bind=0.0.0.0:5000 --access-logfile=- --config gunicorn_config.py`

## Setup for FrontEnd Development

Install npm:

1. `sudo apt-get install npm`
1. `/usr/bin/npm install`

## To Start FRONTEND:

1. `npm start localhost`

**IMPORTANT: To login, use the Keycloak Login link at the bottom right hand corner. The main login is used with Single Signon integration to our Enterprise Active Directory Domain.**

You should be able to login in using the following IDs:  
user/user - Regular Customer Service Representative (CSR)  
admin/admin - Manager of the office (Government Agent)

Additional API Environment Variables of note, which you can add to the .env file

1. SECRET_KEY - Flask required key
1. SERVER_NAME - required for API POD if not localhost.
1. POSTMAN_OPERATOR_PASSWORD - required for Postman and Jest testing.

Additional features that can be turned on by environment variables (see the .env file for details)

1. Integration with Snowplow Analytics
1. Integration with Teams
1. Integration with Rocket Chat
1. Integration with Service Now

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

- The application is now secured by roles. To add roels to the token, go to the client (id : account) and enable 'Full Scope Allowed' under Scope tab.
- Create internal_user role and assign to anyone who will be accessing the application as a staff user
- Create online_appointment_user role and assign to anyone who will be accessing the application as a public user

- Create users & set passwords for the postman users in your keycloak instance:

1. cfms-postman-operator (role: internal_user)
1. cfms-postman-non-operator (role: internal_user)
2. cfms-postman-public-user (role: online_appointment_user, with an attribute displayName and map it as display_name in token)

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
1. public_url=http://localhost:5000/api/v1/
1. public_user_id=cfms-postman-public-user
1. public_user_password=<cfms-postman-public-user userid password>

For this test, I created the password for the two users as demo. From the postman folder run the following command to run the postman tests:

`./node_modules/newman/bin/newman.js run API_Test_TheQ_Booking.json -e postman_env.json --global-var userid=cfms-postman-operator --global-var password=demo --global-var userid_nonqtxn=cfms-postman-non-operator --global-var password_nonqtxn=demo --global-var client_secret=5abdcb03-9dc6-4789-8c1f-8230c7d7cb79 --global-var url=http://localhost:5000/api/v1/ --global-var auth_url=http://localhost:8085 --global-var clientid=account --global-var realm=registry --global-var public_url=http://localhost:5000/api/v1/ --global-var public_user_id=cfms-postman-public-user --global-var public_user_password=password
`

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