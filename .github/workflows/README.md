# GitHub Actions CI/CD Pipelines

The GitHub Action `pull-request-deploy.yaml` is only run manually. It will:

- Take a pull request number and environment as input parameters
- Run Cypress tests against the Appointment Frontend
- Build images using Dockerfile and Source to Image (S2I) builds
- Push the built images to the required `-tools` namespace
- Run `oc tag` to tag the images in the `-tools` namespace to `dev` (The Q or QMS) or `test` (The Q)
- Wait for rollout of the new images in the deployment environment
- Run OWASP ZAP tests
- Run Newman tests if the deployment environment is The Q dev

The GitHub Action `master-deploy.yaml` is only run manually. It will:

- Run Cypress tests against the Appointment Frontend
- Build images using Dockerfile and Source to Image (S2I) builds
- Push the built images to two different `-tools` namespaces
- Use GitHub `environments` to define approvers for tagging images to `-dev`, `-test`, and `-prod` namespaces
- Run `oc tag` to tag the images in the two `-tools` namespaces for `dev`, then `test`, and then `prod` tags
- After deployment to The Q dev, wait for rollout of the new images
- After deployment to The Q dev, run Newman and OWASP ZAP tests

## Setup

The following setup items are needed to run the Actions.

### Environments

The Actions use GitHub `Environments` to require approval before a build is deployed to an environment. When the approval job is reached, the reviewers for the defined environment will be notified that their approval is needed to allow the deployment.

Set up the following environments in your repository Settings:

1. `QMS Dev`
1. `QMS Test`
1. `QMS Prod`
1. `The Q Dev`
1. `The Q Test`
1. `The Q Prod`

In each of these environments set up `Environment protection rules` with at least one `Required reviewer`.

### OpenShift Service Accounts

A Service Account is used to:
- push images to OpenShift `-tools` namespaces
- tag images for deployment to different environments
- wait for new images to roll out before tests are run

The Service Account named `github-actions` needs to be set up in all the `-tools`, `-dev`, `-test`, and `-prod` namespaces for both QMS and The Q. This Service Account will have the bare minimum of permissions that are needed to perform the `oc` calls needed for these Actions.

Using [the OpenShift template](openshift/service_account.yaml) run:

```
$ oc process -f service_account.yaml | oc -n <namespace> apply -f -
```

### GitHub Secrets

There are many GitHub Secrets that are needed to run the Actions:

| Secret Name | Description |
| ----------- | ----------- |
| ARTIFACTORY_PASSWORD | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_REGISTRY | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_USERNAME | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| CYPRESS_BCEID_ENDPOINT | The endpoint to log into BCeID for Cypress testing |
| CYPRESS_BCEID_PASSWORD | The password to log into BCeID for Cypress testing |
| CYPRESS_BCEID_USERNAME | The username to log into BCeID for Cypress testing |
| CYPRESS_PROJECT_ID | The project ID used for the Cypress Dashboard |
| CYPRESS_RECORD_KEY | The record key used for the Cypress Dashboard |
| KEYCLOAK_APPOINTMENTS_FRONTEND_CLIENT | The Keycloak client that is used for the Appointment Frontend |
| KEYCLOAK_AUTH_URL_DEV | The Keycloak URL for the development environment |
| KEYCLOAK_REALM | The Keycloak realm |
| LICENCE_PLATE_QMS | The six character "licence plate" prefix for the QMS namespaces |
| LICENCE_PLATE_THEQ | The six character "licence plate" prefix for The Q namespaces |
| OPENSHIFT_API | The URL of the OpenShift API used to make API calls |
| OPENSHIFT_REGISTRY | The Image Registry used for pushing images to `-tools` namespaces |
| POSTMAN_API_URL_THEQ_DEV | The Q dev API URL used to run tests |
| POSTMAN_AUTH_URL_DEV | The Keycloak server used to authenticate Postman clients in dev |
| POSTMAN_CLIENT_SECRET_DEV | The Client Secret used to run Postman tests in dev |
| POSTMAN_CLIENTID_DEV | The Keycloak Client used to run Postman tests in dev |
| POSTMAN_PASSWORD | The Password of the Keycloak user used to run The Q tests |
| POSTMAN_PASSWORD_NONQTXN | The Password of the Keycloak user used to run non-Q tests |
| POSTMAN_PASSWORD_PUBLIC_USER | The Password of the Keycloak user used to run public API tests |
| POSTMAN_PUBLIC_API_URL_THEQ_DEV | The Q dev API URL used to run the non-Q tests |
| POSTMAN_PUBLIC_USERID | The Username of the Keycloak user used to run public API tests |
| POSTMAN_REALM | The Keycloak realm used to run the Postman tests |
| POSTMAN_USERID | The Username of the Keycloak user used to run The Q tests |
| POSTMAN_USERID_NONQTXN | The Username of the Keycloak user used to run non-Q tests |
| SA_PASSWORD_QMS_DEV | The token for the Service Account `github-actions` in the QMS dev namespace |
| SA_PASSWORD_QMS_TOOLS | The token for the Service Account `github-actions` in the QMS tools namespace |
| SA_PASSWORD_THEQ_DEV | The token for the Service Account `github-actions` in The Q dev namespace |
| SA_PASSWORD_THEQ_TEST | The token for the Service Account `github-actions` in The Q test namespace |
| SA_PASSWORD_THEQ_TOOLS | The token for the Service Account `github-actions` in The Q tools namespace |
| SA_USERNAME | The name of the Service Account: `github-actions` in namespaces |
| ZAP_APPTMNTURL_QMS_DEV | The URL of the QMS dev Appointments application used for running the OWASP ZAP tests |
| ZAP_APPTMNTURL_THEQ_DEV | The URL of The Q dev Appointments application used for running the OWASP ZAP tests |
| ZAP_APPTMNTURL_THEQ_TEST | The URL of The Q test Appointments application used for running the OWASP ZAP tests |
| ZAP_STAFFURL_QMS_DEV | The URL of QMS dev used for running the OWASP ZAP tests |
| ZAP_STAFFURL_THEQ_DEV | The URL of The Q dev used for running the OWASP ZAP tests |
| ZAP_STAFFURL_THEQ_TEST | The URL of The Q test used for running the OWASP ZAP tests |

(note: in OneNote there is a script to set these up automatically, but it can't be committed)

## Third-Party Actions

The following actions are being used:

- [actions/checkout](https://github.com/actions/checkout): checks the code out of the GitHub repository
- [actions/upload-artifact](https://github.com/actions/upload-artifact): uploads the Cypress test and OWASP ZAP scan artifacts
- [cypress-io/github-action](https://github.com/cypress-io/github-action): runs Cypress tests
- [redhat-actions/buildah-build](https://github.com/redhat-actions/buildah-build): builds using a Dockerfile
- [redhat-actions/oc-login](https://github.com/redhat-actions/oc-login): logs into OpenShift using `oc`
- [redhat-actions/podman-login](https://github.com/redhat-actions/podman-login): logs into Artifactory to be able to pull images for builds
- [redhat-actions/push-to-registry](https://github.com/redhat-actions/push-to-registry): pushes built images into the tools namespaces
- [redhat-actions/s2i-build](https://github.com/redhat-actions/s2i-build): builds using Source to Image (S2I)
- [zaproxy/action-full-scan](https://github.com/zaproxy/action-full-scan): runs an OWASP ZAP scan against the Staff Frontend and the Appointment Frontend

## Notes
- The Artifacts aren't visible until after the workflow has completed running. It would be ideal if they were available as soon as the tests finish running. On the other hand, on test failure they should be immediately available and perhaps this is good enough? Details here: https://github.com/actions/upload-artifact/issues/53
- There is an artifact called `zap-scan` that is created and should be ignored. Waiting on an enhancement from ZAP so that we can specify the name of the Artifact: https://github.com/zaproxy/action-baseline/issues/45
