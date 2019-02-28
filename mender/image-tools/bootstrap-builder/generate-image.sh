#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "$#" -ne 2 ]; then
  echo "ERROR: Need to provide source image and config.env."
  exit 1
fi

INPUT_IMAGE=$1
INPUT_NAME=$(basename $1)

CONFIG_ENV=$2

$DIR/prepare-raspbian/prepare-raspbian $INPUT_IMAGE $CONFIG_ENV
$DIR/shrink-image/shrink-image output/smartboard-bootstrap-image.img

