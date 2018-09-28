#!/bin/bash
./wait-for-it.sh mysql_db:3306
echo "Database mysql_db ready..."

# RESULT="mysqlshow --user=root --password=root queue_management | grep -v Wildcard | grep -o myDatabase"
if ! mysql --user=root --password=root --execute='USE queue_management'; then
    mysql --host="mysql_db" --user="root" --password="root" --execute="CREATE DATABASE queue_management;"
    python3 manage.py db upgrade
    mysql --host="mysql_db" --user="root" --password="root" --database="queue_management" --execute="source ./00-PopulateAllDemo.sql"
fi

gunicorn wsgi --bind=0.0.0.0:5000 --access-logfile=- --config gunicorn_config.py