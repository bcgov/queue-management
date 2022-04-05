# GitHub Actions CI/CD Pipeline

The GitHub Action `queue-management.yaml` is _currently_ only run manually. It will:

- Build images using either Dockerfile or Source to Image (S2I) builds
- Push the built images to two different `-tools` namespaces
- Use GitHub `environments` to define approvers for tagging images to `-dev`, `-test`, and `-prod` namespaces
- Run `oc tag` to tag the images in the two `-tools` namespaces for `dev`, then `test`, and then `prod` tags
- After deployment run Newman and OWASP ZAP tests against one `-dev` namespace

## Setup

The following setup is needed to run the Actions.

### Environments

The Actions use GitHub `Environments` to provide a way to approve when a build is deployed to an environment. When the approval job is reached, the reviewers for the defined environment will be notified that their approval is needed to allow the deployment.

Set up the following environments in your repository Settings:

1. `qms-dev`
1. `qms-test`
1. `qms-prod`
1. `theq-dev`
1. `theq-test`
1. `theq-prod`

In each of these environments set up `Environment protection rules` with at least one `Required reviewer`.

### OpenShift Service Accounts

A Service Account is used to push images to OpenShift, and then to tag those images for deployment to different environments. The Service Account called `github-actions` needs to be set up in the two namespaces where the images are pushed. Using [the OpenShift template](openshift/service_account.yaml), for each of the two namespaces run:

```
$  oc process -f service-account.yaml | oc -n <namespace> apply -f -
```

### GitHub Secrets

There are many GitHub Secrets that are needed to run the Actions:

| Secret Name | Description |
| ----------- | ----------- |
| ARTIFACTORY_PASSWORD | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_REGISTRY | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| ARTIFACTORY_USERNAME | Some of the builds use Dockerfiles that pull images from Artifactory. This value comes from the `artifactory-creds` secret |
| NAMESPACE_QMS | The `-tools` namespace name for the "QMS" deployment |
| NAMESPACE_QMS_USERNAME | The Service Account name `github-actions` |
| NAMESPACE_QMS_PASSWORD | The token for the Service Account `github-actions` |
| NAMESPACE_THEQ |  The `-tools` namespace name for the "The Q" deployment |
| NAMESPACE_THEQ_USERNAME | The Service Account name `github-actions` |
| NAMESPACE_THEQ_PASSWORD | The token for the Service Account `github-actions` |
| OPENSHIFT_API | The URL of the OpenShift API used to make API calls |
| OPENSHIFT_REGISTRY | The Image Registry used for pushing images to `-tools` namespaces |
| POSTMAN_AUTH_URL | The Keycloak server used to authenticate Postman clients |
| POSTMAN_CLIENTID | The Keycloak Client used to run Postman tests |
| POSTMAN_CLIENT_SECRET | The Client Secret used to run Postman tests |
| POSTMAN_PASSWORD | The Password of the Keycloak user used to run The Q tests |
| POSTMAN_PASSWORD_NONQTXN | The Password of the Keycloak user used to run non-Q tests |
| POSTMAN_PUBLIC_API_URL | The API URL used to run the non-Q tests |
| POSTMAN_PUBLIC_USERID | The Username of the Keycloak user used to run public API tests |
| POSTMAN_PASSWORD_PUBLIC_USER | The Password of the Keycloak user used to run public API tests |
| POSTMAN_REALM | The Keycloak realm used to run the Postman tests |
| POSTMAN_API_URL | The API URL used to run The Q tests |
| POSTMAN_USERID | The Username of the Keycloak user used to run The Q tests |
| POSTMAN_USERID_NONQTXN | The Username of the Keycloak user used to run non-Q tests |
| ZAP_STAFFURL | The URL of The Q used for running the OWASP ZAP tests |
| ZAP_APPTMNTURL | The URL of the Appointments application used for running the OWASP ZAP tests |

(note: there is a script to set these up automatically, but it can't be committed)

## Notes
- There are separate jobs for "approve" and "tag" because the tag jobs use a reusable workflow and can't have an `environment`. Perhaps it would be better to not have the reusable workflow? Would Composite Actions help?
- It's kludgy that the build tags have to be passed into and out of every job so they can be used for the "tag" jobs. One option would be that the "tag" jobs have a `needs` for `create-image-tags`, but that makes the workflow graph harder to understand. Would Composite Actions help? What about using Artifacts?
- The Artifacts aren't visible until after the workflow has completed running. It would be ideal if they were available as soon as the tests finish running. On the other hand, on test failure they should be immediately available and perhaps this is good enough? Details here: https://github.com/actions/upload-artifact/issues/53

## Requirements for MVP
1. Pushing images sometimes takes over an hour, for no discernable reason - could be due to cluster patching? Would it be better to push to Artifactory? Can we use the `extra-args` in `push-to-registry` to make the long pushes faster? (do retries and reduce timeout, etc? - wild speculation)
1. Figure out additional triggers for running action. PR merge. Manual against a PR. Developer against a fork branch. More?

## Enhancements Backlog
1. Only allow non-dev tagging from bcgov/master
1. Tag with both `latest` and `PR123`
1. Delete the OWASP ZAP artifact `zap_scan` - but using the API requires authentication.
1. It's lousy to use an approval step to wait for image rollouts before Newman and OWASP tests. Can `oc` be used to watch the rollouts?
