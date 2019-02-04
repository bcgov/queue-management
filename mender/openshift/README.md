# Mender + OpenShift
## About
The files in this directory provide everything required to utilize Mender in an OpenShift environment.

This document outlines different details of the application.

### Setting Up in OpenShift
Follow the [quickstart guide](mender_deployment_quickstart.md) for exact steps for setup Mender in OpenShift. 

## Certificates and Keys
More detail outlining the certs and keys requirements of the system can be found in the [Mender documentation](https://docs.mender.io/1.7/administration/certificates-and-keys).

### Certs
Mender Clients (i.e. raspberry pi) require SSL authentication for communicating with the Mender application (both for the `mender-api-gateway` and `minio` components). 

In a fully Docker Compose version of the application, SSL termination happens in the containers themselves (`mender-api-gateway` and a container called `storage-proxy`--which is not used with OpenShift).

However, with OpenShift, SSL termination happens at the `Router`. Because of this, the `nginx.conf` for `mender-api-gateway` has been modified to remove SSL termination inside the container. This allows the unencrypted traffic from the `route` to arrive at the `service` and function correctly. This modification is achieved during the `ImageBuild` stage for the `mender-api-gateway`. `minio`, on the other hand, comes already configured to handle SSL termination at the router.

Because the certs used by the `pathfinder.gov.bc.ca` are backed by a Certificate Authority, there is no added requirement for Mender Clients (PIs) to have copies of the public parts of the certificate since these are provided automatically (through the magic of the Internet). It is important to note that in this configuration Mender Clients need `ca-certificates` installed.

### Keys
There are two components in the Mender application--`mender-useradm` and `mender-device-auth`--which use RSA keys to sign their work.

The keys should be generated with `rsa_keygen.sh` and stored for the lifetime of the application. This utility is based on [this tool](https://github.com/mendersoftware/integration/blob/master/keygen) from the Mender Integration git repo.

The [quickstart guide](mender_deployment_quickstart.md) shows how to generate the keys and use them as input parameters for the related Mender templates. These keys become secrets--`mender-device-auth-key-secret` and `mender-useradm-key-secret`--in the application and are used by the appropriate components.

## User Accounts
User accounts for the `mender-Gui` are handled by the `mender-useradm` service.

A username and password can be added by running:

```
/usr/bin/useradm create-user --username=<username> --password=<password>
```
from within a `mender-useradm` `pod`.

The way the OpenShift implementation is structured, a default *username* is added as a template parameter with a *password* which is automatically generated. This *username* and *password* become an OpenShift secret--`mender-login-secret`. This process is outlined in the [quickstart guide](mender_deployment_quickstart.md).

## Application Components
The Mender application consists of 11 components. A sizable amount of information--albeit incomplete--about each of these components can be found in the [Mender Integration](https://github.com/mendersoftware/integration) git repo.

These components have been broken down into "sub-applications"--each having its own template--and are explained blow.

### Mender-Frontend
This sub-application provides all the interface components for the application.

#### Mender-API-Gateway
The role of this component is to act as an entrypoint for all HTTP communication with Mender. Its main responsibility is the proxying of requests to other Mender components, while rewriting URLs from a public API scheme to an internal one.

More details: [mender-api-gateway git](https://github.com/mendersoftware/mender-api-gateway-docker)

#### Mender Gui
The `mender-gui` component lives inside the application but is served via the `mender-gateway-api` component. 

The role of this component is to provide a GUI web page for interacting with the Mender application.

More details: [mender-gui git](https://github.com/mendersoftware/gui)

### Mender-Component
#### mender-deployments
The role of this component is to manage artifacts, deployments, and reports of outcome of deployments.

More details: [mender-deployments git](https://github.com/mendersoftware/deployments)

#### mender-inventory
The role of this component is to keep track of all clients in the system.  It stores attributes about devices reported by Mender clients, and supports searching and sorting of attributes.

More details: [mender-inventory git](https://github.com/mendersoftware/inventory)

#### mender-device-auth
The role of this component is to handle issuing, maintaining and verifying JWT authentication tokens used by devices in Mender API calls. In essence, it handles all Client authentication for the whole application.

More details: [mender-device-auth git](https://github.com/mendersoftware/deviceauth)

#### mender-useradm
The role of this component is to handle all user management and authentication of the system (e.g. add/remove users, login, etc).

More details: [mender-useradm git](https://github.com/mendersoftware/useradm)

### Mender-Mongodb
This sub-application is a single component, Mongodb. Every service in the `Mender-Component` sub-application use this database to persist state.

**Note**: This component is an unmodified Mongodb instance.

### Mender-Conductor
This sub-application is named after the main component underlying it--`mender-conductor`. This component is responsible for handling API requests which target multiple application components. In other words, when the `mender-api-gateway` needs to communicate with multiple components, it does it through `mender-conductor`.

The other two components in this sub-application are `mender-redis` and `mender-elasticsearch`. These components allow `mender-conductor` to do its job and are not used by any other components (hence their existence in a sub-application). However it is unclear exactly what their role is.

If `mender-conductor` is removed, much of the application will still function, however errors will show up in the GUI and it will not be possible to decommission devices.

**Note**: `mender-conductor` is really covered in the Mender Integration](https://github.com/mendersoftware/integration) git repo.

### Minio
This sub-application consists of one component--`minio`. This component comes unmodified from the [BCDevOps](https://github.com/BCDevOps/minio-openshift) git repo. Because of this, it shows up as a separate application from `mender`.

`minio` is effectively a clone of the Amazon S3 Bucket system. In the Mender application, the `mender-deployments` component is the only system which directly interacts with `minio`. It uses `minio` to store artifacts as well as provide Clients with URLs for downloading artifacts.