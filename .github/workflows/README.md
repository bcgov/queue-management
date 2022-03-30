# GitHub Actions

GitHub actions to:
 - build images using either Dockerfile or Source to Image (S2I) builds.
 - push images to two different -tools namespaces
 - tag the images in the two -tools namespaces for `dev`, `test`, and `prod`

Note:
 - There are separate jobs for "approve" and "tag" because the tag steps use a reusable workflow and can't have an `environment`. Perhaps it would be better to not have the reusable workflow?

TODO:
1. update the image tagger to take multiple image names
1. tag with both `latest` and `PR123`
1. newman tests - how to wait for rollout?
1. Only allow non-dev tagging from bcgov/master
1. document the environments
3. document the secrets
