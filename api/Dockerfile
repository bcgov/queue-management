FROM ubuntu:18.04

# Open up required ports
EXPOSE 5000 8088

# Install packages
RUN apt-get update -q
RUN apt-get install -yqq python3 \
python3-pip \
libmysqlclient-dev \
mysql-client \
python-dev \
python3-dev \
python3-venv \
wget \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install dumb-init
RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN dpkg -i dumb-init_*.deb

# Setup environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /opt/queue-management-api
WORKDIR /opt/queue-management-api

RUN python3 -m venv env
RUN /bin/bash -c "source env/bin/activate"
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./init.sh"]