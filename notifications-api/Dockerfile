FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
 && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN python3 -m pip install --no-cache-dir -r requirements.txt setuptools && \
    python3 setup.py install

EXPOSE 5001

ENV NUM_WORKERS=3
ENV TIMEOUT=120

#CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--timeout", "$TIMEOUT", "--workers", "$NUM_WORKERS", "wsgi:app"]
CMD gunicorn --bind 0.0.0.0:5001 --timeout $TIMEOUT --workers $NUM_WORKERS wsgi:application