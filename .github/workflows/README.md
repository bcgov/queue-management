# GitHub Actions CI/CD Pipeline

The GitHub Action `queue-management.yaml` is _currently_ only run manually. It will:

- Build images using either Dockerfile or Source to Image (S2I) builds
- Push the built images to two different `-tools` namespaces
- Use GitHub `environments` to define approvers for tagging images to `-dev`, `-test`, and `-prod` namespaces
- Run `oc tag` to tag the images in the two `-tools` namespaces for `dev`, then `test`, and then `prod` tags
- After deployment run newman tests against one `-dev` namespace

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

## Notes
- There are separate jobs for "approve" and "tag" because the tag jobs use a reusable workflow and can't have an `environment`. Perhaps it would be better to not have the reusable workflow? Would Composite Actions help?
- It's kludgy that the build tags have to be passed into and out of every job so they can be used for the "tag" jobs. One option would be that the "tag" jobs have a `needs` for `create-image-tags`, but that makes the workflow graph harder to understand. Would Composite Actions help? What about using Artifacts?

## Gotchas
- Building during cluster operations can have failures when trying to pull images from Artifactory. Running the workflow again will eventually work but isn't ideal.
- Pushing images to `-tools` namespaces can be slow or fail when cluster operations are being done. Would it be better to push to Artifactory? Can we use the `extra-args` in `push-to-registry` to make the long pushes faster? (do retries and reduce timeout, etc? - wild speculation)

## TODO
1. update the image tagger to take multiple image names
1. tag with both `latest` and `PR123`
1. newman tests - how to wait for rollout?
1. Only allow non-dev tagging from bcgov/master
1. document the secrets
1. document service accounts
1. Fix `insecure_skip_tls_verify=true` in reusable-tag-image
1. https://github.com/marketplace/actions/owasp-zap-full-scan
1. figure out additional triggers for running action. PR merge. Manual against a PR. Developer against a fork branch. More?
