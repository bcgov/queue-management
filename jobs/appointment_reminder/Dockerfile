FROM artifacts.developer.gov.bc.ca/docker-remote/python:3.14-slim

# Update package list and upgrade nghttp2
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl git nghttp2 && \
    apt-get upgrade -y nghttp2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install go-crond
ARG SOURCE_REPO=BCDevOps
ARG GOCROND_VERSION=0.6.2
RUN curl https://github.com/$SOURCE_REPO/go-crond/releases/download/$GOCROND_VERSION/go-crond-64-linux -s -L -o /usr/local/bin/go-crond
RUN chmod ug+x /usr/local/bin/go-crond

# Add a job user
ARG uid=1001
ARG user=theq
RUN useradd -U -ms /bin/bash -u $uid $user \
    && usermod -a -G root $user

ENV HOME=/appointment_reminder

RUN mkdir $HOME && chmod 755 $HOME

WORKDIR $HOME

# Install the requirements
COPY ./requirements.txt .
COPY . .

RUN pip install --upgrade pip --user
RUN pip install --no-cache-dir -r requirements.txt

# Set ownership and permissions
# Make /etc/passwd writable for the root group so an entry can be created for an OpenShift assigned user account.
RUN chown -R $user:root $HOME \
    && chmod -R ug+rw $HOME \
    && chmod ug+x $HOME/*.sh \
    && chmod g+rw /etc/passwd \
    && chmod g-w $HOME/cron/crontab

USER $user
ENTRYPOINT ["bash", "docker-entrypoint.sh"]