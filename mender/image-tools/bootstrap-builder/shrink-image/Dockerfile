FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    parted util-linux

COPY docker-entrypoint.sh /usr/local/bin/
COPY pishrink.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]
