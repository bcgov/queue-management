function start_cron_jobs() {
  echo "Starting go-crond as a background task ..."
  CRON_CMD="go-crond --allow-unprivileged --include=cron/"
  exec ${CRON_CMD}
}

start_cron_jobs
