#FROM python:3.8.5-buster
FROM docker-remote.artifacts.developer.gov.bc.ca/python:3.8.5-buster

# ========================================================================================================
# Install go-crond (from https://github.com/BCDevOps/go-crond)
#  - Adds some additional logging enhancements on top of the upstream project;
#    https://github.com/webdevops/go-crond
#
# CRON Jobs in OpenShift:
# - https://blog.danman.eu/cron-jobs-in-openshift/
#
# --------------------------------------------------------------------------------------------------------
ARG SOURCE_REPO=BCDevOps
ARG GOCROND_VERSION=0.6.2
RUN curl https://github.com/$SOURCE_REPO/go-crond/releases/download/$GOCROND_VERSION/go-crond-64-linux -s -L -o /usr/local/bin/go-crond
RUN chmod ug+x /usr/local/bin/go-crond
# ========================================================================================================

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
# Set scripts as executable (make files and python files do not have to be marked)
# Make /etc/passwd writable for the root group so an entry can be created for an OpenShift assigned user account.
RUN chown -R $user:root $HOME \
    && chmod -R ug+rw $HOME \
    && chmod ug+x $HOME/*.sh \
    && chmod g+rw /etc/passwd \
    && chmod g-w $HOME/cron/crontab

USER $user
ENTRYPOINT ["bash", "docker-entrypoint.sh"]