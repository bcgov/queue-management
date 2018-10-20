# Installation Instructions - **Work in Progress**

Prequisites: Keycloak

Openshift Environment split into at least two or more workspaces:
1. Tools Workspace - Location to include Jenkins, SonarQube, Build Configs
1. Dev, Test, Prod Workspaces - Deployment Configs for Percona, queue-management-api, queue-management-frontend and rabbitmq

Within the Tools Workspace, you will be required to add two config maps.

```keycloak-dev``` with the following attibutes:
1. client_id=```<keycloak client name>```
1. client_secret=```<keycloak client secret>```
1. keycloak_realm=```<realm>```
1. auth_server_url=```<auth URL>```

```postman-passwords``` with the following attibutes:
1. password_qtxn=```<required keycloak user "cfms-postman-operator" password>```
1. password_nonqtxn=```<required keycloak user "cfms-postman-non-operator" password```>
1. client_secret=```<keycloak client secret>```



**To Do:** Provide sample from Installation instance of Keycloak
