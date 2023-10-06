# Mender
## About mender
[Mender](https://mender.io/) is an over-the-air (OTA) update system for Linux. Updates in the Mender context--called deployments--are complete operating system overwrites backed by a dual-partition system which allow OS rollbacks in the event of a failed deployment. While the base unit of an update is a full OS overwrite, deployments can--additionally--run pre- and postinstall [scripts](https://docs.mender.io/1.7/artifacts/state-scripts) before and after it writes the root file system. This allows Mender to modify components of the OS outside of baked in deployment. 

## Implementation
The system is made up of two applications which work together to fascilitate updates: `server` and `client`.

### Server
The server side of the application is made up of a collection of microservices. More details about these microservices can be found in the [Mender Integration](https://github.com/mendersoftware/integration) git repo and in the [openshift/README](./openshift/README.md) in this git repo.

At its core, the server side application provides management of users, clients, and deployments. The core functionality of the application can be accessed through the web UI. Additionally, the application itself has an extensive [API](https://docs.mender.io/1.7/apis) allowing for automation as well as the official [CLI](https://docs.mender.io/1.7/server-integration/using-the-apis).

### Client
The client side of the application is effectively a single compiled application running on the client devices. This application communicates with the server application to facilitate device registration, update status information, and downloading deployments. Once a deployment is downloaded, the client side application is also responsible for installing the update, restarting the client, and assessing if the update was a success (and rolling back if failed).   