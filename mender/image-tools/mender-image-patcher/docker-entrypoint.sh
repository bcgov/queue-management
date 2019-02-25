#! /bin/bash
# 
# This tool is a modified version of Steven Bjornson's LinuxFSMount:
# https://github.com/sabjorn/LinuxFSMount/
#

set -ex

IMG_NAME=/image/$1

echo $IMG_NAME

mount_partition() {
	SECTION=$1
	MOUNT_POINT=$2

	set -f
	# These variables will only populate if the .img is for Raspbian
	FS_INFO=$(fdisk -l ${IMG_NAME} | grep ${IMG_NAME}${SECTION} | sed 's/[*]\+/ /g')
	SECTOR_SIZE=$(fdisk -l ${IMG_NAME} | grep "Units: sectors of" | cut -d " " -f8)
	SECTOR_SIZE="${SECTOR_SIZE:-0}"
	SECTORS_START=$(echo ${FS_INFO} | cut -d " " -f2)
	SECTORS_START="${SECTORS_START:-0}"
	set +f

	mkdir -p $MOUNT_POINT
	mount -o loop,offset=$((${SECTORS_START} * ${SECTOR_SIZE})) $IMG_NAME $MOUNT_POINT
}

mkdir /root_system

mount_partition "2" /root_system

export SERVER_URL=`cat /root_system/etc/mender/mender.conf | jq -r '.["ServerURL"]'`

envsubst '${SERVER_URL}' < /setup-scripts/files/mender.conf > /root_system/etc/mender/mender.conf
cp /setup-scripts/files/fstab.mender /root_system/etc/fstab
cp /setup-scripts/files/mender-device-identity /root_system/usr/share/mender/identity
chmod +x /root_system/usr/share/mender/identity/mender-device-identity

ln -snf /data/mender /root_system/var.base/lib/mender

cp /root_system/uboot/sites.txt /root/
cp /root_system/uboot/smartboard-base-url.txt /root/

umount /root_system

mount_partition "1" /uboot
/setup-scripts/state-scripts/ArtifactReboot_Enter_01_hardward_config

cp /root/sites.txt /uboot/
cp /root/smartboard-base-url.txt /uboot/

umount /uboot
