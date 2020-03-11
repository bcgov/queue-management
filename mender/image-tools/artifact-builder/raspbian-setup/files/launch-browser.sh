#!/bin/bash

until timedatectl status | grep -q "synchronized: yes";
do
  sleep 1;
done


sudo systemctl stop splashscreen

xsetroot -solid white
xsetbg -onroot -shrink -fullscreen -smooth -background white /var/flaskapp/web-service/static/splash.png

# disable DPMS (Energy Star) features.
xset -dpms
# disable screen saver
xset s off
# don't blank the video device
xset s noblank
# disable mouse pointer
unclutter &
# run window manager
matchbox-window-manager -use_cursor no -use_titlebar no  &

sleep 2

# Start up browser, and keep it alive if it crashes / terminates for some reason.
while true ; do
	# Launch a splash screen first and let the webservice tell us when it's safe
	# to try load the smart board. This ensures that the network is up
	# before hitting the smartboard

	chromium-browser \
		--ignore-blacklist \
		--disable-features=TranslateUI \
		--disable-infobars  --disable-translate \
		--bwsi --disable-logging \
		--disable-infobars \
		--disable-session-crashed-bubble \
		--noerrdialogs \
		--start-fullscreen \
		--disk-cache-size=0 \
		--disable-quic \
		--enable-fast-unload \
		--enable-tcp-fast-open \
		--enable-native-gpu-memory-buffers \
		--enable-gpu-rasterization \
		--enable-zero-copy \
		--kiosk "http://localhost/splash.html"

	sleep 1
	# Clean out any lingering processes if the browser has died

	killall -HUP chromium-browser
	sleep 2
done 
