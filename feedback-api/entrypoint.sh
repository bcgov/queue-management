#!/bin/sh

echo "Waiting for postgres..."

gunicorn -b 0.0.0.0:5000 wsgi:application
