#!/bin/sh
set -e

ROOTFS_OUTPUT_FILE_NAME=$1
ARTIFACT_NAME=$2
DEVICE_TYPE=$3

mkdir /root_system

mount /root_images/$ROOTFS_OUTPUT_FILE_NAME /root_system
mkdir -p /root_system/root/setup-scripts/

cp -R /setup-scripts /root_system/root/

if [ -f /root_system/usr/bin/qemu-arm-static ]; then
  echo "WARNING: /usr/bin/qemu-arm-static already exists in image. Using this but may be of incompatible version."
  QEMU_STATIC_COPIED=false
else
  # trick to make chroot into ARM image work
  cp /usr/bin/qemu-arm-static /root_system/usr/bin
  QEMU_STATIC_COPIED=true
fi

echo "Entering emulated shell in device image. All commands are run as the root user of the device image."
echo "Make changes (e.g. apt update, apt upgrade, wget ...) and press Ctrl-D when done."

rm -f /root_system/etc/resolv.conf
cp /etc/resolv.conf /root_system/etc/resolv.conf

# Using bash for command completion support and other conveniences
chroot /root_system /bin/bash -c "/root/setup-scripts/setup.sh"

# Mender Artifact name must also be present inside
echo artifact_name=$ARTIFACT_NAME > /root_system/etc/mender/artifact_info

if [ "$QEMU_STATIC_COPIED" = true ]; then
  rm /root_system/usr/bin/qemu-arm-static
fi

rm -rf /root_system/root/setup-scripts/

umount /root_system

echo "Creating Mender Artifact. This may take a few minutes..."
mender-artifact write rootfs-image -t $DEVICE_TYPE -n $ARTIFACT_NAME -f /root_images/$ROOTFS_OUTPUT_FILE_NAME -o /root_images/$ARTIFACT_NAME.mender -s /setup-scripts/state-scripts
#mender-artifact write rootfs-image -t $DEVICE_TYPE -n $ARTIFACT_NAME -u /root_images/$ROOTFS_OUTPUT_FILE_NAME -o /root_images/$ARTIFACT_NAME.mender -s /setup-scripts/state-scripts

sync
echo "completed Creating Artificat"
