#! /bin/bash
#
# Any commands here will only run on the first boot of an image.
# Anything that needs to actually be run on the device before the 
# drive is locked should be placed here.
#
# NOTE: Mender State scripts also have "ArtifactCommit" scripts
# that will happen after an artifact is deployed, however
# the scripts here will run after the first flash of the box

if [ -e /root/.first-boot-finished ] ; then
	exit 0
fi

mount / -o remount,rw

ssh-keygen -A

ufw default deny incoming 
ufw default allow outgoing
ufw allow 443
ufw allow `cat /var/sshd_port`
ufw allow ntp 
ufw --force enable

systemctl daemon-reload

touch /root/.first-boot-finished

mount / -o remount,ro
