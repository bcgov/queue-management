# OpenShift Deploymetn information

## Prerequestites

1. Keycloak instance running and setup for authentication.

2. Postgres Database

* We are using Patroni for HA Postgresql database. Instructions on install can be found here: https://github.com/BCDevOps/platform-services/tree/master/apps/pgsql/patroni
* Assumption is that patroni service is called: patroni-master

3. Rabbit MQ instance is running

* We are using the following installation: https://github.com/redhat-cop/containers-quickstarts/tree/master/rabbitmq
* We assume the installation the rabbit service is called: rabbitmq
* Used for to support high availability API interactivity. This syncs the requests between multiple API pods.

4. We are using artifactory to pull some of our docker images due to the rate limiting change.  Please see the following for how we set that up.

    https://github.com/BCDevOps/OpenShift4-Migration/issues/51

5. We assume that you will already have a Jenkins & SonarQube instance.  


## Deployment Configuration

### Installation for basic Queue Management

- queue-management-frontend-dc.yml - Creates the queue management Front End Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.
- queue-management-api-dc.yml - Creates the queue management API Pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables.
- queue-managmement-chained-builds.yml - Used to create the imagestreams for both the API & Front End pods. Please note that this also creates a Config Map that needs to be updated with your Openshift & Keycloak variables. These are used with the Jenkinsfile as well. **Review the comments in the Jenkinsfiles for more information.**



<br>
### Installation for Appointments on Online
<br><br>
## Build Configuration Templates
<br><br>

- appointment-frontend-dc.yaml - creates appointment front end Pods. This also creates a Config Map that needs to be updated with your authentication details.
- crond-send-appointment-reminder-deploy - creates reminder pods for sending email reminders. Also creates two Config Maps that needs to be updated with authentication details.  ** This is now using Artificatory to pull the base docker image.