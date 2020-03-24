#!/bin/bash

sudo systemctl stop splashscreen

xsetroot -solid white
xsetbg -onroot -shrink -fullscreen -smooth -background white /var/flaskapp/web-service/static/splash.png

until timedatectl status | grep -q "synchronized: yes";
do
  sleep 1;
done

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
	# --check-for-update-interval=31536000
		# --ignore-blacklist --ignore-gpu-blacklist \
		# --disable-translate --disable-features=TranslateUI \
		# --disable-infobars --disable-session-crashed-bubble \
		# --disable-logging --noerrdialogs --start-fullscreen \
		# --disk-cache-size=0 --use-gl=egl --gles --disable-quic \
		# --enable-fast-unload --enable-checker-imaging --enable-tcp-fast-open \
		# --check-for-update-interval=0 --disable-background-networking \
		# --enable-native-gpu-memory-buffers --enable-gpu-rasterization --enable-zero-copy \
	chromium-browser \
		--disable-logging --noerrdialogs --start-fullscreen \
		--show-component-extension-options \
		--ignore-gpu-blacklist --ignore-blacklist \
		--disable-background-networking \
		--use-gl=egl --enable-remote-extensions \
		--enable-native-gpu-memory-buffers \
		--disable-quic --enable-tcp-fast-open \
		--disable-gpu-compositing --force-gpu-rasterization \
		--enable-zero-copy --disable-pings --media-router=0 \
		--disable-bundled-ppapi-flash --proxy-auto-detect \
		--check-for-update-interval=0 --disable-background-networking \
		--kiosk "http://localhost/splash.html"

	sleep 1
	# Clean out any lingering processes if the browser has died

	pkill -f -- "chromium-browser"
	sleep 2
done 
 
