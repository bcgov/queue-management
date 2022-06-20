# Mender + OpenShift Quickstart

## About
This document provides every command required for get Mender running in OpenShift. These instructions are based on the https://github.com/mendersoftware/mender-helm readme but are modified to get Mender running in OpenShift.

## Step 1 - Install MongoDB

This step is only needed when installing into a new namespace. When doing a Mender update you will want to re-use the existing installation.

<details>
<summary>What is the installation process for a new namespace?</summary>

Use the `MongoDB` template from the OpenShift Catalog with a `MongoDB Database Name` of `mongo`.

</details>

## Step 2 - Install MinIO

This step is only needed when installing into a new namespace. When doing a Mender update you will want to re-use the existing installation. **This is particularly true in production, where MinIO is shared by other applications and you do not want to delete production data.**

<details>
<summary>What is the installation process for a new namespace?</summary>

You probably want to install using the BCDevOps [GitHub Repository](https://github.com/BCDevOps/minio-openshift). Otherwise, the Mender Helm Chart readme describes installing MinIO using a Helm Chart, which works but isn't straightforward in OpenShift.

<details>
<summary>What is the installation process using a Helm Chart?</summary>

Note that the documentation says to use v6.0.5 but a newer version may be preferable.

Generate a random `<ACCESS_KEY>` and `<SECRET_KEY>` (we used 16 and 24 random characters).

```
helm repo add minio https://helm.min.io/
helm repo update
helm -n <namespace> install minio minio/minio --version 6.0.5 --set "accessKey=<ACCESS_KEY>,secretKey=<SECRET_KEY>,persistence.size=15Gi,securityContext.enabled=false,resources.requests.memory=50m"
```

<details>
<summary>What are all these settings in the helm install command?</summary>

The documentation says to run the command

```
helm -n <namespace> install minio minio/minio --version 6.0.5 --set "accessKey=<ACCESS_KEY>,secretKey=<SECRET_KEY>"
```

but this fails because of the huge PVC request

```
Error: INSTALLATION FAILED: persistentvolumeclaims "minio" is forbidden: exceeded quota: storage-quota, requested: requests.storage=500Gi, used: requests.storage=54Gi, limited: requests.storage=256Gi
```

So we can drop from 500Gi to 15Gi by running

```
helm -n <namespace> install minio minio/minio --version 6.0.5 --set "accessKey=<ACCESS_KEY>,secretKey=<SECRET_KEY>,persistence.size=15Gi"
```

which produces the ReplicaSet event

```
Error creating: pods "minio-58bdddb854-" is forbidden: unable to validate against any security context constraint: [provider "anyuid": Forbidden: not usable by user or serviceaccount, provider "pipelines-scc": Forbidden: not usable by user or serviceaccount, provider restricted: .spec.securityContext.fsGroup: Invalid value: []int64{1000}: 1000 is not an allowed group, spec.containers[0].securityContext.runAsUser: Invalid value: 1000: must be in the ranges: [1001060000, 1001069999], provider "nonroot": Forbidden: not usable by user or serviceaccount, provider "rsync-anyuid": Forbidden: not usable by user or serviceaccount, provider "hostmount-anyuid": Forbidden: not usable by user or serviceaccount, provider "aqua-scc": Forbidden: not usable by user or serviceaccount, provider "log-collector-scc": Forbidden: not usable by user or serviceaccount, provider "machine-api-termination-handler": Forbidden: not usable by user or serviceaccount, provider "hostnetwork": Forbidden: not usable by user or serviceaccount, provider "hostaccess": Forbidden: not usable by user or serviceaccount, provider "node-exporter": Forbidden: not usable by user or serviceaccount, provider "privileged": Forbidden: not usable by user or serviceaccount, provider "trident": Forbidden: not usable by user or serviceaccount]
```

We can do

```
helm -n <namespace> install minio minio/minio --version 6.0.5 --set "accessKey=<ACCESS_KEY>,secretKey=<SECRET_KEY>,persistence.size=15Gi,securityContext.enabled=false"
```

which produces

```
Error creating: Pod "minio-784dcfd57b-7jhlr" is invalid: spec.containers[0].resources.requests: Invalid value: "4Gi": must be less than or equal to memory limit
```

which brings us to

```
helm -n <namespace> install minio minio/minio --version 6.0.5 --set "accessKey=<ACCESS_KEY>,secretKey=<SECRET_KEY>,persistence.size=15Gi,securityContext.enabled=false,resources.requests.memory=50m"
```

</details>
</details>
</details>

## Step 3 - Install NATS

This step is only needed when installing into a new namespace. When doing a Mender update you will want to re-use the existing installation.

<details>
<summary>What is the installation process for a new namespace?</summary>

```
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm repo update
helm -n <namespace> install nats nats/nats --version 0.15.1 --set "nats.image=nats:2.7.4-alpine" --set "nats.jetstream.enabled=true"
```

</details>

## Step 4 - Install Mender

### Step 4.1 - Clone Mender Helm Chart

Clone the repo https://github.com/mendersoftware/mender-helm.

### Step 4.2 - Fix Privileged Ports Problems

By default, Mender is set up to use the privileged ports (under 1024) and will fail because the processes are not running as root.

Change the following ports:

1. `mender/templates/api-gateway-deploy.yaml`
- change `--entrypoints.http.address=:80` to `--entrypoints.http.address=:8888`
- change `--entrypoints.https.address=:443` to `--entrypoints.https.address=:8443`
- change `containerPort: 80` to `containerPort: 8888`
- change the liveness, readiness, and startup probe ports from `80` to `8888`

2. `mender/templates/api-gateway-svc.yaml`
- change `targetPort: 80` to `targetPort: 8888`

3. `mender/templates/gui-deploy.yaml`
- change the liveness and readiness probe ports from `80` to `8888`

4. `mender/templates/gui-svc.yaml`
- change `targetPort: 80` to `targetPort: 8888`

### Step 4.3 - Fix GUI Runtime Problems

Among other things, the `gui` pod tries to write a file to a readonly filesystem. We can work around this by generating the file (log into a debug pod and edit the script to print the file) and then mounting it from the [mender-gui-config ConfigMap](templates/mender-gui-config_configmap.yaml):

```
oc -n <namespace> apply -f templates/mender-gui-config_configmap.yaml
```

In `mender/templates/gui-deploy.yaml`:

- mount the volume in the `gui` container in `spec.template.spec.containers`:

```
        volumeMounts:
          - name: mender-gui-config
            mountPath: /var/www/mender-gui/dist/env.js
            subPath: env.js
```

- add a volume for the `mender-gui-config` ConfigMap in `spec.template.spec`:

```
      volumes:
        - name: mender-gui-config
          configMap:
            name: mender-gui-config
            defaultMode: 420
```

The image is still going to error when it starts up, so build another image that does not write the file to `/var/www/mender-gui/dist/env.js`. Also fix other problems with the image:
1. Create the necessary temporary file directories in `/var/cache/nginx`
1. Change the nginx configuration to listen on port 8888 instead of port 80
1. Allow a process identifier file to be written to `/var/run`

Create a new [imagestream](templates/mender-gui_imagestream.yaml) as well as the [buildconfig](templates/mender-gui_buildconfig.yaml):

```
oc -n <tools-namespace> apply -f templates/mender-gui_imagestream.yaml
oc -n <tools-namespace> apply -f templates/mender-gui_buildconfig.yaml
```

### Step 4.4 - Set Up the values.yaml File

In the repo create a `values.yaml` file:

```
global:
  enterprise: false
  image:
    username: null
    password: null
  url: https://<hostname>

api_gateway:
  certs:
    cert: |-
      -----BEGIN CERTIFICATE-----
      [...insert here...]
      -----END CERTIFICATE-----
    key: |-
      -----BEGIN PRIVATE KEY-----
      [...insert here...]
      -----END PRIVATE KEY-----
  env:
    SSL: false

device_auth:
  certs:
    key: |-
      -----BEGIN RSA PRIVATE KEY-----
      [...insert here...]
      -----END RSA PRIVATE KEY-----

useradm:
  certs:
    key: |-
      -----BEGIN RSA PRIVATE KEY-----
      [...insert here...]
      -----END RSA PRIVATE KEY-----
```

Generate the TLS certificate and keys with:

```
openssl req -x509 -sha256 -nodes -days 3650 -newkey ec:<(openssl ecparam -name prime256v1) -keyout private.key -out certificate.crt -subj /CN="<hostname>"

openssl genpkey -algorithm RSA -out device_auth.key -pkeyopt rsa_keygen_bits:3072
openssl rsa -in device_auth.key -out device_auth_converted.key
mv device_auth_converted.key device_auth.key

openssl genpkey -algorithm RSA -out useradm.key -pkeyopt rsa_keygen_bits:3072
openssl rsa -in useradm.key -out useradm_converted.key
mv useradm_converted.key useradm.key
```

Use the contents of the generated files to fill in the `values.yaml` file:
* `api_gateway.certs.cert`: from `certificate.crt`
* `api_gateway.certs.key`: from `private.key`
* `device_auth.certs.key`: from `device_auth.key`
* `useradm.certs.key`: from `useradm.key`

### Step 4.5 - Run the Helm Install

```
make package

helm -n <namespace> install mender -f values.yaml mender-3.2.2.tgz --set "global.mongodb.URL=mongodb://<ADMIN_USER>:<ADMIN_PASSWORD>@mongodb,global.s3.AWS_ACCESS_KEY_ID=<ACCESS_KEY>,global.s3.AWS_SECRET_ACCESS_KEY=<SECRET_KEY>,gui.image.registry=image-registry.openshift-image-registry.svc:5000/<tools-namespace>,gui.image.repository=mender-gui,gui.image.tag=3.2.0-custom"
```

### Step 4.6 - Add Users

Open a terminal in the `useradm` pod and create users with

```
useradm create-user --username=<Firstname.Lastname>@gov.bc.ca --password=<password>
```

## Known Issue

The `deployments` pod needs the `api-gateway` pod, but when Mender is first installed they start at the same time. There might be a restart of the `deployments` pod if the `api-gateway` pod is slower in starting. Deleting the `deployments` pod will start it afresh and will look cleaner.
