# GitHub Actions CI/CD Pipelines

The GitHub Action `pull-request-deploy.yaml` is only run manually. It will:

- Take a pull request number and environment as input parameters
- Build images using either Dockerfile or Source to Image (S2I) builds
- Push the built images to the required `-tools` namespace
- Run `oc tag` to tag the images in the `-tools` namespace to `dev` (The Q or QMS) or `test` (The Q)
- Wait for rollout of the new images in the deployment environment
- Run OWASP ZAP tests
- Run Newman tests if the deployment environment is The Q dev

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
$ oc process -f service-account.yaml | oc -n <namespace> apply -f -
```

### GitHub Secrets

There are many GitHub Secrets that are needed to run the Actions:

| Secret Name | Description |
| ----------- | ----------- |
| ARTIFACTORY_PASSWORD | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_REGISTRY | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_USERNAME | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
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
| SA_PASSWORD_QMS_TEST | The token for the Service Account `github-actions` in the QMS test namespace |
| SA_PASSWORD_QMS_TOOLS | The token for the Service Account `github-actions` in the QMS tools namespace |
| SA_PASSWORD_QMS_PROD | The token for the Service Account `github-actions` in the QMS prod namespace |
| SA_PASSWORD_THEQ_DEV | The token for the Service Account `github-actions` in The Q dev namespace |
| SA_PASSWORD_THEQ_TEST | The token for the Service Account `github-actions` in The Q test namespace |
| SA_PASSWORD_THEQ_TOOLS | The token for the Service Account `github-actions` in The Q tools namespace |
| SA_PASSWORD_THEQ_PROD | The token for the Service Account `github-actions` in The Q prod namespace |
| SA_USERNAME | The name of the Service Account: `github-actions` in namespaces |
| ZAP_APPTMNTURL_QMS_DEV | The URL of the QMS dev Appointments application used for running the OWASP ZAP tests |
| ZAP_APPTMNTURL_THEQ_DEV | The URL of The Q dev Appointments application used for running the OWASP ZAP tests |
| ZAP_APPTMNTURL_THEQ_TEST | The URL of The Q test Appointments application used for running the OWASP ZAP tests |
| ZAP_STAFFURL_QMS_DEV | The URL of QMS dev used for running the OWASP ZAP tests |
| ZAP_STAFFURL_THEQ_DEV | The URL of The Q dev used for running the OWASP ZAP tests |
| ZAP_STAFFURL_THEQ_TEST | The URL of The Q test used for running the OWASP ZAP tests |

(note: there is a script to set these up automatically, but it can't be committed)

## Notes
- The Artifacts aren't visible until after the workflow has completed running. It would be ideal if they were available as soon as the tests finish running. On the other hand, on test failure they should be immediately available and perhaps this is good enough? Details here: https://github.com/actions/upload-artifact/issues/53

## Enhancements Backlog
1. Delete the OWASP ZAP artifact `zap_scan` - using the API doesn't work as the Artifact hasn't been marked as `complete` yet, so the GET API call won't get the Artifact.
