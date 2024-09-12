#! /bin/bash
#
# This file generates all system wide information for this smartboard
# at boot time and stores them in /var/smartboard
#
# Inputs: ${fallback_video_timeout} is imported in via the artifact building process
#

mkdir -p /var/smartboard/

# Get Ethernet mac address
IFACE=e*
read LOCALMAC </sys/class/net/$IFACE/address

# Set address correctly based on MAC Address
while read mac tzpi smartboard_id location remainder
do
    if [[ $LOCALMAC == $mac ]]; then
	        TZPI=$tzpi;
            SMARTBOARD_ID=$smartboard_id;
            LOCATION=$location
    fi
done < /uboot/sites.txt

# Check if SMARTBOARD_ID is empty and default to 999 if necessary
if [[ -z "$SMARTBOARD_ID" ]]; then
    SMARTBOARD_ID=999
fi

ln -snf "/usr/share/zoneinfo/${TZPI}" /var/localtime

cp /uboot/smartboard-base-url.txt /var/smartboard/base-url

smartboard_base_url=`cat /uboot/smartboard-base-url.txt | tr -d '\n'`


# Leave the test URL with it's zone in the config so the 
# application knows what to load
echo $SMARTBOARD_ID > /var/smartboard/id
echo $TZPI > /var/smartboard/timezone
echo $LOCATION > /var/smartboard/location
echo "${smartboard_base_url}/smartboard/${SMARTBOARD_ID}?tz=${TZPI}&localvideo=1" > /var/smartboard/url
echo "${smartboard_base_url}/static/videos/manifest.json" > /var/smartboard/manifest-url
echo "${fallback_video_timeout}" > /var/smartboard/fallback-video-timeout
