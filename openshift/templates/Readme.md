# OpenShift Deploymetn information

## Prerequestites

1. Keycloak instance running and setup for authentication.
Patroni: HA Postgres instance

2. Postgres Database

* We are using Patroni for HA Postgresql database. Instructions on install can be found here: https://github.com/BCDevOps/platform-services/tree/master/apps/pgsql/patroni
* Assumption is that patroni service is called: patroni-master

3. Rabbit MQ instance is running

* We are using the following installation: https://github.com/redhat-cop/containers-quickstarts/tree/master/rabbitmq
* We assume the installation the rabbit service is called: rabbitmq
* Used for to support high availability API interactivity. This syncs the requests between multiple API pods.


## Deployment Configuration

### Installation for basic Queue Management

- queue-management-frontend-dc.yml - Creates the queue management Front End Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.
- queue-management-api-dc.yml - Creates the queue management API Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.
- crond-send-appointment-reminder-deploy - creates reminder pods for sending email reminders. Also creates two Config Maps that needs to be updated with authentication details

- appointment-frontend-dc.yaml - creates appointment front end Pods. This also creates a Config Map that needs to be updated with your authentication details.
### Installation for Appointments on Online

## Build Configuration Templates

It is assumed that you will already have a Jenkins & SonarQube instance.

- rabbit-mq-build - Used in the imagestream for RabbitMQ
- queue-managmement-chained-builds.yml - Used to create the imagestreams for both the API & Front End pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables. These are used with the Jenkinsfile as well. Review the comments in the Jenkinsfiles for more information.

Required information in the ConfigMap includes:

1. `userid_qtxn=<set to cfms-postman-operator>`
1. `password_qtxn=<cfms-postman-operator userid password>`
1. `userid_nonqtxn=<set to cfms-postman-non-operator>`
1. `password_nonqtxn=<cfms-postman-non-operator userid password>`
1. `client_secret=<keycloak client secret></keycloak>`
1. `zap_with_url=/zap/zap-baseline.py -r baseline.html -t <queue management frontend URL>`
1. `dev_namespace=<Openshift Development Workspace>`
1. `url=<API URL>/api/v1/`
1. `auth_url=<keycloak URL>`
1. `clientid=<keycloak Client ID>`
1. `realm=<Keycloak Realm>`

Once the statefulset is up and running, set the guest passwod by going each of the pods and running the following command in the terminal:
`rabbitmqctl change_password guest <password>`