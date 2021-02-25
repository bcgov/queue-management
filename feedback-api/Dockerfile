FROM python:3.8.5-buster
#FROM python:.6-stretch

#RUN echo "deb http://ftp.debian.org/debian stretch main contrib" > /etc/apt/sources.list

# todo: Revert this entire pull request when libcairo2 >= 1.14.2 is available from the debian
#       jessie repo.  This is a temporary fix for https://github.com/Kozea/WeasyPrint/issues/233

# reconfigure Debian to allow installs from both stretch (testing) repo and jessie (stable) repo
# install all the dependencies except libcairo2 from jessie, then install libcairo2 from stretch

#RUN apt-get -y update \
#    && apt-get install -y \
#        fonts-font-awesome \
#        libffi-dev \
#        libgdk-pixbuf2.0-0 \
#        python-dev \
#        python-lxml \
#        shared-mime-info \
#    && apt-get install -y ttf-mscorefonts-installer \
#                        libpango1.0-0 \
#                        libcairo2 \
#                        libpangocairo-1.0-0 \
#    && apt-get -y clean




RUN apt-get -y update && apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info


COPY . /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt
RUN python3 setup.py install


EXPOSE 5001

ENV NUM_WORKERS=3
ENV TIMEOUT=120

#CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--timeout", "$TIMEOUT", "--workers", "$NUM_WORKERS", "wsgi:app"]
CMD gunicorn --bind 0.0.0.0:5001 --timeout $TIMEOUT --workers $NUM_WORKERS  wsgi:application
