#! /bin/bash
# Runs all scripts in ./scripts folder
# This script should be run on a booted pi or a loaded container

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -ex

if [ ! -f $DIR/config.env ] ; then
	echo "ERROR: No config.env provided"
	exit -1
fi

set -a
source $DIR/config.env
set +a

export files=$DIR/files
export home_dir="/home/${username}"

for f in $DIR/scripts/*; do
  sudo -E bash -c "$f"
done
