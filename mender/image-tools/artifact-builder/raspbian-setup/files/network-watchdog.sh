#! /bin/bash

/root/load-smartboard-data.sh

NETWORK_DOWN=0
TIMEOUT=5

# How many times to retry before a reboot
RETRIES=$((${network_reboot_timeout} / $TIMEOUT))

while true ; do
	wget --no-check-certificate -q -O /dev/null "`cat /var/smartboard/url`"
	if [ $? -gt 0 ] ; then
		NETWORK_DOWN=$((NETWORK_DOWN + 1))
		echo "Network down, attempt number: ${NETWORK_DOWN}"

		systemctl restart systemd-networkd
		touch /var/network-down
	else
		NETWORK_DOWN=0

		if [ -e /var/network-down ] ; then
			rm /var/network-down
		fi
	fi

	if [ $NETWORK_DOWN -gt $RETRIES ] ; then
		reboot
	fi

	# We check every 5 seconds for network connection
	sleep $TIMEOUT
done
