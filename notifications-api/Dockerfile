FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GUNICORN_PROCESSES=3 \
    GUNICORN_THREADS=1 \
    GUNICORN_TIMEOUT=120

WORKDIR /opt/app-root/src

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .

# Required because the application package is under src/api.
# Dependencies were already installed from requirements.txt.
RUN pip install --no-deps .

EXPOSE 5001

CMD ["gunicorn", "wsgi:application", \
     "--bind", "0.0.0.0:5001", \
     "--access-logfile=-", \
     "--no-control-socket", \
     "--config=gunicorn_config.py"]