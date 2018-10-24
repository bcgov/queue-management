# OpenShift Template information

Prerequesite: Keycloak instance running and setup for authentication.

## Deployment Configuration Templates:

- percona-dc.yml - Creates a high availability MySQL Statefull set.
- rabbit-mq-dc.yml - Creates a RabbitMQ Statefull set. Used for to support high availability API interactivity. This syncs the requests between pods.
- queue-management-api-dc.yml - Creates the queue management API Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.
- queue-management-frontend-dc.yml - Creates the queue management Front End Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.

## Build Configuration Templates

It is assumed that you will already have a Jenkins & SonarQube instance.

- rabbit-mq-build - Used in the imagestream for RabbitMQ
- queue-managmement-chained-builds.yml - Used to create the imagestreams for both the API & Front End pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables. These are used with the Jenkinsfile as well. Review the comments in the Jenkinsfiles for more information.

Required information in the ConfigMap includes:

1. `password_qtxn=<<cfms-postman-operator userid password>`
1. `password_nonqtxn=<cfms-postman-non-operator userid password>`
1. `client_secret=<keycloak client secret></keycloak>`
1. `zap_with_url=/zap/zap-baseline.py -r baseline.html -t <queue management frontend URL>`
1. `dev_namespace=<Openshift Development Workspace>`
1. `url=<API URL>/api/v1/`
1. `auth_url=<keycloak URL>`
1. `clientid=<keycloak Client ID>`
1. `realm=<Keycloak Realm>`
