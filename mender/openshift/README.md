# Mender + OpenShift

## About
Mender is installed using a [Helm Chart](https://github.com/mendersoftware/mender-helm). The instructions on this repository were used as a starting point but required changes to get Mender running in OpenShift.

This document outlines different details of the application.

### Setup in OpenShift
Follow the [quickstart guide](mender_deployment_quickstart.md) for exact steps for setup of Mender in OpenShift. 

## Certificates and Keys
More detail outlining the certificate and keys requirements of the system can be found in the [Mender documentation](https://docs.mender.io/3.2/server-installation/certificates-and-keys).

### Certificates
Mender Clients (e.g. Raspberry Pi) require TLS authentication for communicating with the `api-gateway` component of the Mender application.

With OpenShift the TLS termination happens at the `route`, and the certificates are issued by a Certificate Authority. There is no added requirement for Mender Clients to have copies of the public parts of the certificate since these are provided automatically (through the magic of the Internet). It is important to note that in this configuration Mender Clients need `ca-certificates` installed.

### Keys
There are two components in the Mender application--`device-auth` and `useradm`--which use RSA keys to sign their work. The keys should be generated with `openssl` and stored for the lifetime of the application.

The [quickstart guide](mender_deployment_quickstart.md) shows how to generate the keys and use them as input parameters for the related Mender templates. These keys become secrets--`rsa-device-auth` and `rsa-useradm`--in the application and are used by the appropriate components.

## User Accounts
User accounts for the `gui` are handled by the `useradm` component. A username and password can be added by logging into the `useradm` pod and running:

```
/usr/bin/useradm create-user --username=<username> --password=<password>
```

## Application Components
The Mender application consists of many components. A sizable amount of information about these components is in the [Mender Integration](https://github.com/mendersoftware/integration) git repo.
