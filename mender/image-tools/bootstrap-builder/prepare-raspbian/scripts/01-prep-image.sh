#! /bin/bash

set -ex

if [ -e /var.base ] ; then
	echo "Prune skipped as image has already been pruned."
	exit 0
fi

# We need to back up init_resize as it's used by Mender
cp /usr/lib/raspi-config/init_resize.sh /root/

apt-get remove -y build-essential samba-common libasound2 libasound2-data \
	alsa-utils binutils manpages manpages-dev man-db cpp gcc-6 firmware-atheros \
	firmware-libertas firmware-misc-nonfree firmware-realtek gdb plymouth libplymouth4 \
	libraspberrypi-doc perl-modules-5.24 iso-codes libc6-dev

apt-get -y --purge autoremove
apt-get clean

rm -rf /var/cache/man
rm -rf /usr/share/man

# Restore init_resize
mkdir -p /usr/lib/raspi-config/
cp /root/init_resize.sh /usr/lib/raspi-config/
