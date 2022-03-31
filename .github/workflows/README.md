# GitHub Actions

GitHub actions to:
- build images using either Dockerfile or Source to Image (S2I) builds.
- push images to two different -tools namespaces
- tag the images in the two -tools namespaces for `dev`, then `test`, and then `prod`

Notes:
- There are separate jobs for "approve" and "tag" because the tag steps use a reusable workflow and can't have an `environment`. Perhaps it would be better to not have the reusable workflow?
- It's kludgy but the "approve" steps have the tags as an output variable. Otherwise, the "tag" steps have a *needs* for `create-image-tags`, and that makes the workflow graph harder to understand.

Gotchas:
- Building during cluster operations can have failures when trying to pull images from Artifactory. Wait for all builds to complete and then "Re-run failed jobs".
- Pushing images to -tools namespaces can be slow when cluster operations are being done. Would it be better to push to Artifactory?

TODO:
1. Make sure the S2I build images are the right ones
1. export tags from the approve to clean up the graph
1. update the image tagger to take multiple image names
1. tag with both `latest` and `PR123`
1. newman tests - how to wait for rollout?
1. Only allow non-dev tagging from bcgov/master
1. document the environments
1. document the secrets
1. document service accounts
1. parallelize the image pushes
1. Fix `insecure_skip_tls_verify=true` in reusable-tag-image
1. passing the image tags from job to job is lousy. composite actions? artifacts, but how to pass those to reusable workflows?
