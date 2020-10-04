This is to allow Reminders a day prior to the appointment for citizens


## Create a build so that it creates an image

Run the script in tools namespace

`
oc process -f crond-send-appointment-reminder-build.json |oc create -f -
`

## Create config map for cron details in workspace:

name: send-appointment-reminder-crond-${imagetag}-cron-configuration
Key: crontab
Data: 

00 23 * * * default cd /appointment_reminder && ./run.sh
# An empty line is required at the end of this file for a valid cron file.


## Create a deployment in workspace

### DEV
`oc process -f cond-send-appointment-reminder-deploy.json --p IMAGE_NAMESPACE=servicebc-cfms-tools -p TAG_NAME=dev | oc create -f -`

## Tag the image for Dev
Run the script in tools namespace

`oc tag send-appointment-reminder-crond:latest send-appointment-reminder-crond:dev`

## Execute job manually

in cron pod Terminal, ./run.sh