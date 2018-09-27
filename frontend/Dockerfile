FROM ubuntu:18.04

# Open up required ports
EXPOSE 8080

RUN apt-get update -q
RUN apt-get install -yqq nodejs npm wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install dumb-init
RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN dpkg -i dumb-init_*.deb

COPY . /opt/queue-management-frontend
WORKDIR /opt/queue-management-frontend

RUN npm install

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["npm", "start", "localhost"]
