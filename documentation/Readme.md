# Installation Guide - Work in Progress

We use OpenShift in our environment, and it is our recommendation for running this project. You can then use our build / deployment configs found in the openshift directory.

For development, we recommend you use Visual Studio Code's *Remote - Containers* to run the application in docker containers, as described below.

## Key features of the platform:

Jenkins Build process includes:

- Building our Flask/Python API
- Building our Vue FrontEnd and copying the output to CADDY Webserver
- Postman tests
- Zap Vulnerability tests

## Running the code with VSCode *Remote - Containers*

This repo is configured to use Visual Studio Code's *Remote - Containers* (aka *devcontainers*) to run the applications in docker containers.

To run the code in devcontainers you need:
1. VSCode
1. WSL2 with a Linux distribution (we like LTS Ubuntu)
1. *docker-compose* installed in your WSL2 Linux
1. *dockerd* running in your WSL2 Linux

Clone the code in this repo:

```
$ git clone https://github.com/bcgov/queue-management
```

Opening the cloned repo in VSCode will detect the *.devcontainer* directory and recommend that you re-open in *Remote - Containers*. This will build and start the docker containers that are needed:

1. PostgreSQL database
2. Application code in a Python + Node container

## Directory Structure for Configuration Files

```
queue-management
    ├───.devcontainer
    │       devcontainer.json
    │       docker-compose.yml
    │       postCreateCommand.sh
    │
    ├───api
    │       .env
    │
    ├───appointment-frontend
    │   └───public
    │       └───config
    │           │   configuration.json
    │           │
    │           └───kc
    │                   keycloak-public.json
    │
    ├───feedback-api
    │       .env
    │
    ├───frontend
    │   └───public
    │       ├───config
    │       │       configuration.json
    │       │
    │       └───static
    │           └───keycloak
    │                   keycloak.json
    │
    ├───jobs
    │   └───appointment_reminder
    │           .env
    │
    └───notifications-api
            .env
```

## Frequently Asked Questions

<details>
<summary>How do I run the application(s)?</summary>

The *.vscode/launch.json* file in the repo contains launchers for:

1. **appointment_frontend**: the Vue.js code in *appointment_frontend*
1. **queue_management_api**: the Python code in *api*
1. **queue_management_frontend**: the Vue.js code in *frontend*
1. **Queue Management**: starts both *queue_management_api* and *queue_management_frontend*

Select the item you want from the dropdown list and hit F5. You can run multiple items at one time. The *PORTS* tab of the *Panel* will list the ports that are being used.

Note: starting Vue.js applications takes a long time for the webpack. When run on the commmand line there is a progress indicator, but this does not appear when using the launcher. Watching the `top` command and waiting for node processes to drop their CPU usage is one way of telling when the application is ready. Ideally we'll find a way to display the progress indicator, or perhaps there is a better way to start the Vue.js processes during development.

</details>

<details>
<summary>How do I do development on Python code?</summary>

The *.vscode/launch.json* file in the repo contains launchers for the API. Select the API you want from the drop-down list and then hit F5 to run it in *gunicorn*. Once the code is running, whenever you save a file *gunicorn* will automatically reload itself with the changes. You can set breakpoints in the code and then test with a browser, newman, or postman.

</details>

<details>
<summary>How do I wipe/initialize the PostgreSQL database?</summary>

To run the application your database needs to have tables created and a small amount of default data set up. The *api/manage.py* script is used to manipulate the database.

Rebuilding the container should set up the table. However, if your database contains no tables, create them with:

```
workspace$ (cd api; env/bin/python manage.py db upgrade)
```

If your database either:

1. contains tables but no default data, or
1. contains tables and data, but you want to re-initialize with default data:

```
workspace$ (cd api; env/bin/python manage.py bootstrap)
```

If you really want to wipe and rebuild your database:

1. Either switch out of devcontainers or shut down VSCode
1. In docker remove both the database container and its volume
1. Restart VSCode in devcontainer mode

</details>

<details>
<summary>How do I update a Python requirements.txt?</summary>

The best way to update Python requirements is to:

1. Update the *requirements.txt* file
1. Run *pip install -r requirements.txt*
1. Run the tests and ensure success

To rebuild the container with the new requirements, click the green section of the *Status Bar* and select *Rebuild Container*.

</details>

<details>
<summary>How do I update a Node packages.json?</summary>

The best way to update Node packages is to:

1. Update the *packages.json* file
1. Run *npm install*
1. Run the tests and ensure success

To rebuild the container with the new packages, click the green section of the *Status Bar* and select *Rebuild Container*.

</details>

<details>
<summary>How do I change the Python version?</summary>

The development environment should be as close as possible to production, including the patch release version of Python. The production version of Python is defined by the Red Hat UBI in our buildconfigs. We should match versions in the devcontainers, even though setting it up is tedious and not straightforward.

1. In a live container get the production version to target with *python --version*
1. Look at https://mcr.microsoft.com/v2/vscode/devcontainers/python/tags/list and take a guess as an image that will match
1. Update the *VARIANT* in *.devcontainer/docker-compose.yml* and rebuild the container
1. Check the Python version, and start over at step 2 until you have the most recent image matching the target version

</details>

<details>
<summary>How do I change the Node version?</summary>

The development environment should be as close as possible to production, including the version of Node. The production version of Node is defined by the Red Hat UBI in our buildconfigs.

1. In a live container get the production version to target with *node --version*
1. Update the *NODE_VERSION* in *.devcontainer/docker-compose.yml* and rebuild the container

</details>

<details>
<summary>How do I change the PostgreSQL version?</summary>

The development environment should be as close as possible to production, including the version of PostgreSQL. The version of PostgreSQL is defined as a Docker Hub identifier in *.devcontainer/docker-compose.yml* in the *services.db.image* value.

It's probably a good idea to delete your database volume when changing the version. Upgrades *may* work, downgrades will probably fail.

1. Update *.devcontainer/docker-compose.yml* with the PostgreSQL version that you want
1. Click the green section of the *Status Bar* and select *Reopen Folder in WSL*
1. In the Docker extension remove the container and then the volume
1. Click the green section of the *Status Bar* and select *Reopen in Container*

</details>

## To use FRONTEND:

Use your IDIR to authenticate against our dev Keycloak realm.

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

There are Jest tests as well but I am still working on integrating them to our pipeline. The can be manually run by typing: npm test in the frontend folder.

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
