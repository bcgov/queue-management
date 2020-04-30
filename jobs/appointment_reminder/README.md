## Create a build so that it creates an image

Run the script in tools namespace

`
oc process -f send-appointment-reminder-build.json |oc create -f -
`

## Tag the image for TEST and PROD migration
Run the script in tools namespace

`oc tag send-appointment-reminder:latest update-stale-payment:test`

`oc tag send-appointment-reminder:latest update-stale-payment:prod`

## Run the Job
Now switch to DEV namepace

`oc project l4ygcl-dev`

Run the cron in DEV namespace

### DEV
`oc process -f send-appointment-reminder.yaml -p ENV_TAG=latest -p TAG_NAME=dev | oc create -f -`

### TEST
`oc process -f send-appointment-reminder.yaml -p ENV_TAG=test -p TAG_NAME=test | oc create -f -`

### PROD
`oc process -f send-appointment-reminder.yaml -p ENV_TAG=prod -p TAG_NAME=prod | oc create -f -`

## Find the job running

`oc get jobs`

## Delete Jobs if needed

`oc delete cronjob/send-appointment-reminder`


## How to check logs in Kibana

`kubernetes.pod_name like "send-appointment-reminder" AND kubernetes.namespace_name:"servicebc-cfms-dev"`