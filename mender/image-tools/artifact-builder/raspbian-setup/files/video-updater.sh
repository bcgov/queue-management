#! /bin/bash

/root/load-smartboard-data.sh

BASE_URL=`cat /var/smartboard/base-url`
SMARTBOARD_ID=`cat /var/smartboard/id`
TIMEOUT=${video_cache_timeout}

mkdir -p /data/videos
ln -nsf /data/videos /var/flaskapp/web-service/static/videos

while true ; do
	wget --no-check-certificate -q -O /tmp/manifest.json "`cat /var/smartboard/manifest-url`"
	if [ $? -gt 0 ] ; then
		echo "Network down, video caching skipped"

		sleep 5
	else
		# We have the manifest check if there is a new video
		cat /tmp/manifest.json | jq -r "if has(\"${SMARTBOARD_ID}\") then .[\"${SMARTBOARD_ID}\"] else .[\"default\"] end" > /tmp/manifest.local.json
		UPDATED=`cat /tmp/manifest.local.json | jq -r '.["updated"]'`
		URL=`cat /tmp/manifest.local.json | jq -r '.["url"]'`

		if [[ ! -e /data/videos/video.mp4 || ! -e /data/videos/updated ||
			"$UPDATED" != `cat /data/videos/updated` || "$URL" != `cat /data/videos/url` ]]
		then
			wget --no-check-certificate  -O "/data/videos/video.mp4.tmp" "$BASE_URL$URL"
			# Once a new video is downloaded the browser needs to be restarted
			killall chromium-browser

			mv /data/videos/video.mp4.tmp /data/videos/video.mp4
			echo $UPDATED > /data/videos/updated
			echo $URL > /data/videos/url
		fi

		sleep $TIMEOUT
	fi
done
