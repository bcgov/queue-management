#! /bin/sh
set -e
set -u

# py-spy needs sudo as we're spying on other processes.
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# Get earliest PID, main process, and we can use --subprocessses arg.
MAIN_PROCESS=$(pgrep -f gunicorn |  head -n 1)

if [ -z "$MAIN_PROCESS" ]; then
      echo "gunicorn is not running, unable to profile."
      exit 1
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --command=*)
      command="${1#*=}"
      ;;
    *)
      echo "Invalid args: $@"
      exit 1
  esac
  shift
done

if [[ "$command" == "record" ]]; then
    py-spy record -o output/profile-${MAIN_PROCESS}.svg --subprocesses --pid ${MAIN_PROCESS}
elif [[ "$command" == "top" ]]; then
    py-spy top --subprocesses --pid ${MAIN_PROCESS}
else
    echo "Invalid --command argument.  You provided: $command"
fi