# Mender + OpenShift Quickstart
## About
This document provides every command required for get Mender running in OpenShift.

**Note**: Be sure to set all ENV variables before running any of the other commands.

## Step 1 - Setup Project ENV Variables
The ENV are used to configure the deployment. Not all of them are strictly necessary since the `parameters` in templates have default values. However, the default values are not definitive best choices.

```
TOOLS_WORKSPACE=<your tools location>
PROJECTNAME=<your deployment location>
IMAGESTREAM_TAG=<dev|prod>
MENDER_DEFAULT_USERNAME=<default username email address>
MINIO_VOLUME_CAPACITY=<some volume capacity>
MONGO_VOLUME_CAPACITY=<some volume capacity>
REDIS_VOLUME_CAPACITY=<some volume capacity>
ELASTICSEARCH_VOLUME_CAPACITY=<some volume capacity>
MINIO_ROUTE_HOSTNAME=<s3mender.pathfinder.gov.bc.ca | s3mender-dev.pathfinder.gov.bc.ca>
API_GATEWAY_ROUTE_HOSTNAME=<mender.pathfinder.gov.bc.ca | mender-dev.pathfinder.gov.bc.ca> 
```

## Step 2 - Generate Keys for `mender-useradm` and `mender-deviceauth`
A handy key generator script handles generation of the two keys needed for this project.

```
cd queue-management/mender/openshift
./rsa_keygen.sh
```
**NOTE**: do not commit files generated from this step to git

Store generated keys as `ENV` variables for later use:

```
USERADM_KEY="$(cat ./keys-generated/keys/useradm/private.key)"
DEVICEAUTH_KEY="$(cat ./keys-generated/keys/deviceauth/private.key)"
```

## Step 3 - Add ImageBuild and ImageStreams to Tools Space
All the ImageBuild and ImageStreams are handled by a single template. All ImageStreams are initially tagged as `latest` and are--in later steps--tagged depending on which deployment context is desired.

**Note**: Make sure to set the `TOOLS_WORKSPACE` ENV before running this command.

```
oc process -f ./templates/mender-image-build-template.yaml | oc create -n $TOOLS_WORKSPACE -f -
```

## Step 4 - Deploy Minio (BCDevOps Version)
The following command creates an instance of the `minio` DeploymentConfig from the BCDevOps git repo. Unfortunatelly, the `app` tag is automatically set to `minio` (instead of `mender`) so this component will show up as an independent application. Mender will ahve no problem communicating with it.

```
oc process \
    -f https://raw.githubusercontent.com/BCDevOps/minio-openshift/master/openshift/minio-deployment.json \
    -p IMAGESTREAM_NAMESPACE=bcgov \
    -p IMAGESTREAM_TAG=v1-latest \
    -p VOLUME_CAPACITY=${MINIO_VOLUME_CAPACITY} | oc create -n $PROJECTNAME -f -
```

## Step 5 - Deploy Mender
### mender-mongodb
```
oc process -f ./templates/mender-mongodb-deployment-template.yaml \
    -p IMAGESTREAM_TAG=${IMAGESTREAM_TAG} \
    -p TOOLS_WORKSPACE=${TOOLS_WORKSPACE} \
    -p MONGO_VOLUME_CAPACITY=${MONGO_VOLUME_CAPACITY} | oc create -n $PROJECTNAME -f -
```

### mender-conductor
```
oc process -f ./templates/mender-conductor-deployment-template.yaml \
    -p IMAGESTREAM_TAG=${IMAGESTREAM_TAG} \
    -p TOOLS_WORKSPACE=${TOOLS_WORKSPACE} \
    -p REDIS_VOLUME_CAPACITY=${REDIS_VOLUME_CAPACITY} \
    -p ELASTICSEARCH_VOLUME_CAPACITY=${ELASTICSEARCH_VOLUME_CAPACITY} | oc create -n $PROJECTNAME -f -
```

### mender-components (core services)
```
oc process -f ./templates/mender-component-deployment-template.yaml \
    -p IMAGESTREAM_TAG=${IMAGESTREAM_TAG} \
    -p TOOLS_WORKSPACE=${TOOLS_WORKSPACE} \
    -p MINIO_ROUTE_HOSTNAME=${MINIO_ROUTE_HOSTNAME} \
    -p USERADM_KEY=${USERADM_KEY} \
    -p DEVICEAUTH_KEY=${DEVICEAUTH_KEY} \
    -p MENDER_DEFAULT_USERNAME=${MENDER_DEFAULT_USERNAME} | oc create -n $PROJECTNAME -f -
```

### mender-frontend (gatway and gui)
```
oc process -f ./templates/mender-frontend-deployment-template.yaml \
    -p API_GATEWAY_ROUTE_HOSTNAME=${API_GATEWAY_ROUTE_HOSTNAME} \
    -p TOOLS_WORKSPACE=${TOOLS_WORKSPACE} \
    -p IMAGESTREAM_TAG=${IMAGESTREAM_TAG} | oc create -n $PROJECTNAME -f -
```

## Step 6 - Tag ImageStreams in Sequence to Bring Them Up
These steps likely can be done all at once but have only been tested in sequence. It is likely best to wait after each step to make sure all systems are ready before tagging the next set of ImageStreams.

### mender-conductor
```
oc tag -n ${TOOLS_WORKSPACE} mender-redis-stream:latest mender-redis-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-elasticsearch-stream:latest mender-elasticsearch-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-conductor-stream:latest mender-conductor-stream:${IMAGESTREAM_TAG}
```

### mender-mongodb
```
oc tag -n ${TOOLS_WORKSPACE} mender-mongodb-stream:latest mender-mongodb-stream:${IMAGESTREAM_TAG}
```

### mender-components
```
oc tag -n ${TOOLS_WORKSPACE} mender-inventory-stream:latest mender-inventory-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-deployments-stream:latest mender-deployments-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-device-auth-stream:latest mender-device-auth-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-useradm-stream:latest mender-useradm-stream:${IMAGESTREAM_TAG}
```

### mender-frontend (gatway and gui)
```
oc tag -n ${TOOLS_WORKSPACE} mender-gui-stream:latest mender-gui-stream:${IMAGESTREAM_TAG}
oc tag -n ${TOOLS_WORKSPACE} mender-api-gateway-stream:latest mender-api-gateway-stream:${IMAGESTREAM_TAG}
```