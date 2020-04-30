#! /bin/sh
export LIBRARY_PATH=/opt/rh/httpd24/root/usr/lib64
export X_SCLS=rh-python35 httpd24
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64::/opt/rh/httpd24/root/usr/lib64
export PATH=/opt/app-root/bin:/opt/rh/rh-python35/root/usr/bin::/opt/rh/httpd24/root/usr/bin:/opt/rh/httpd24/root/usr/sbin:/opt/app-root/src/.local/bin/:/opt/app-root/src/bin:/opt/app-root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

cd /opt/app-root/src
echo 'run send_appointment_reminder.py'
/opt/app-root/bin/python3 ./send_appointment_reminder.py