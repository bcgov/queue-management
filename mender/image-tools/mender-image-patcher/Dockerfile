FROM ubuntu:18.04

ARG MENDER_ARTIFACT_VERSION=2.3.0

RUN apt-get update && apt-get install -y \
    simg2img img2simg jq gettext \
    qemu-user-static

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
