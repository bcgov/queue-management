FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GUNICORN_PROCESSES=3 \
    GUNICORN_THREADS=1 \
    GUNICORN_TIMEOUT=120 \
    WSGI_PORT=8080

WORKDIR /opt/app-root/src

# Build tools needed if a Python dependency has no prebuilt wheel.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .

# Installs the src/api package. Dependencies were installed above.
RUN pip install --no-deps . && \
    chgrp -R 0 /opt/app-root/src && \
    chmod -R g=u /opt/app-root/src

# OpenShift can replace this with an arbitrary permitted UID.
USER 1001

EXPOSE 8080

CMD ["gunicorn", "wsgi:application", \
     "--bind", "0.0.0.0:8080", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--no-control-socket", \
     "--config=gunicorn_config.py"]