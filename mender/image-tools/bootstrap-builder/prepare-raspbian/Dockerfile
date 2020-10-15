FROM ubuntu:20.04

ARG MENDER_ARTIFACT_VERSION=3.3.0

RUN apt-get update && apt-get install -y \
    simg2img img2simg \
    qemu-user-static

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]