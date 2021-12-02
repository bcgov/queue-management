# Note: the python container provided for use with VSCode is running Debian.
# This is different from the RHEL image that we're using at runtime. This isn't
# ideal, but it isn't much different than people running Ubuntu locally in the
# previous WSL2 development environments.

# [Choice] Python version (use -bullseye variants on local arm64/Apple
# Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye,
# 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster,
# 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
#
# Note: this ARG is overwritten by the value in docker-compose.yml.
ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
#
# Note: this ARG is overwritten by the value in docker-compose.yml.
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then \
    su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && \
    nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your requirements rarely change, uncomment this section to add
# them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r \
#    /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

# Install psql
RUN sudo apt update && \
    sudo apt-get install -y postgresql-contrib
