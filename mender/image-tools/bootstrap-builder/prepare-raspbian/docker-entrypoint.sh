#! /bin/bash
# 
# This tool is a modified version of Steven Bjornson's LinuxFSMount:
# https://github.com/sabjorn/LinuxFSMount/
#

set -e

IMG_NAME=/image/$1

# These variables will only populate if the .img is for Raspbian
FS_INFO=$(fdisk -l ${IMG_NAME} | grep ${IMG_NAME}2)
SECTOR_SIZE=$(fdisk -l ${IMG_NAME} | grep "Units: sectors of" | cut -d " " -f8)
SECTOR_SIZE="${SECTOR_SIZE:-0}"
SECTORS_START=$(echo ${FS_INFO} | cut -d " " -f2)
SECTORS_START="${SECTORS_START:-0}"
SECTORS_END=$(echo ${FS_INFO} | cut -d " " -f3)
SECTORS_END="${SECTORS_END:-0}"
SECTORS_TOTAL=$(echo ${FS_INFO} | cut -d " " -f4)

mkdir /root_system

# offset=0 for everything but RPI
mount -o loop,offset=$((${SECTORS_START} * ${SECTOR_SIZE})) $IMG_NAME /root_system

if [ -f /root_system/usr/bin/qemu-arm-static ]; then
  echo "WARNING: /usr/bin/qemu-arm-static already exists in image. Using this but may be of incompatible version."
  QEMU_STATIC_COPIED=false
else
  # trick to make chroot into ARM image work
  cp /usr/bin/qemu-arm-static /root_system/usr/bin
  QEMU_STATIC_COPIED=true
fi

cp -R /scripts /root_system/root/
chroot /root_system /bin/bash -c "cd /root/scripts ; ./01-*.sh "
rm -rf /root_system/root/scripts

if [ -e /setup-scripts/setup.sh ] ; then
  cp -R /setup-scripts /root_system/root/
  chroot /root_system /bin/bash -c "/root/setup-scripts/setup.sh"
  rm -rf /root_system/root/setup-scripts
fi

if [ "$QEMU_STATIC_COPIED" = true ]; then
  rm /root_system/usr/bin/qemu-arm-static
fi
