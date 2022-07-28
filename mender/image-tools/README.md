# Mender Image Tools
## About
Mender does not distribute operating system images but instead provides tooling for generating custom distributions. There are several ways of doing this, including the [yocto](https://docs.mender.io/1.7/artifacts/yocto-project) tool. However, this project uses a more direct approach to producing a custom OS distribution.

Utilizing a tool called [mender-convert](https://github.com/mendersoftware/mender-convert.git), an existing Raspberry PI Raspbian image can be converted into a Mender compatible image. Furthermore, once "menderized", a tool called [artifact builder](./artifact-builder) can be used to directly manipulate this image filesystem enabling customization.

Customizing the image with direct manipulation is beneficial because it operates--in most cases--as if manipulation was being done directly on the machine. i.e. through a terminal session. The immediate impact of this is the ability to prototype modifications on a running system (i.e. ssh into a running raspberry pi) and then move these modifications into scripts which can be run to generate the custom distro.

## Stages
Generating a custom distro from a stock Raspbian image requires several steps. However, unless the base Raspbian image changes, only some of the steps are required to generate a new `deployment artifact`--the basic unit of update in the Mender universe.

The workflow (in order) is as follows:

### Base Image
##### Rerun Frequency:
* Raspbian base distribution changes

##### Purpose:
This step modifies the stock Raspberry PI Raspbian image by removing extra packages, adding required packages, and shrinking the image size.

This Base Image must be "menderized" (the next stage) in order to be used as a Mender client. However it can still be flashed on an SD card and used in a Raspberry PI.

### Menderized Image
##### Rerun Frequency:
* Base Image is modified
* Mender server URL changes
* (Potentially) `Mender-Convert` tool is updated

##### Purpose:
This stage converts an existing Raspberry PI Raspbian image into a **Menderized** image which can be used to perform OTA updates. This process is done using the [mender-convert](https://github.com/mendersoftware/mender-convert.git) utility. The Menderized image is configured with the correct `UBoot` settings, partition configuration, and a `data` partition for persisting data between updates.

### Patched Image
##### Rerun Frequency:
* Menderized Image is modified

##### Purpose:
The `Mender-Convert` tool makes a number of assumptions about device configuration which do not match all of the requirements of this project. This *patch* step provides a method for adjusting the Menderized image to allow for:

* correct filesystem structure (read-only FS)
* modified Mender config file

**Important**: The image produced at this stage--`.sdimg`--is what will be flashed to every Raspberry PI and will allow them to register with the Mender server and receive updates. 

### Deployment Artifact
##### Rerun Frequency:
* New functionality is added to deployment [scripts](./artifact-builder/raspbian-setup/scripts/)
* Updates to persistent data (WiFi config, SSH Keys, etc)
* Config file (`config.env`) is modified

##### Purpose:
Generates a deployment artifact which can be used to update systems via the Mender server application. The `mender-convert` process produces several files. The `.ext4` file produced by the process is an image which can be mounted. By mounting this image the filesystem can be directly modified with regular Linux commands (and thus scripted). Through this process, once this filesystem is modified a corresponding Mender artifact is produced (a `.mender` file).

Thus, it is this stage where the majority of updates will be produced.

## Building Images to Prepare for Mender Deployment
### Prerequisites

- **Ubuntu 19.04**
- 10 gigabytes of storage
- qemu
- docker.io

**NOTE**: When running these steps in a VM, restart the machine to prevent potential issues.

### Step 0: Install QEMU Cross-Architecture Support
**NOTE**: This step is only required to be run once.

QEMU is a tool allowing for architecture emulation. Running this section will allow the system to run non-native binaries. This is necessary because the most build stages attempt to operate AS IF they were running inside the Raspberry Pi system itself (using `chroot`):

```
sudo apt-get install qemu-user-static
git clone https://github.com/computermouth/qemu-static-conf.git
sudo mkdir -p /lib/binfmt.d
sudo cp qemu-static-conf/*.conf /lib/binfmt.d/
sudo systemctl restart systemd-binfmt.service
```

If the `systemctl` command above fails, it's probably because you're using WSL, which doesn't use `systemd`. Instead, start the emulator service with the init script:

```
sudo /etc/init.d/binfmt-support start
```

### Step 1: Building Base Image (Bootstrapping)

```
git clone https://www.github.com/bcgov/queue-management
cd queue-management/mender/image-tools
```
Download and unzip the latest [Raspbian Lite Image](https://downloads.raspberrypi.org/raspbian_lite_latest) and 
You will need to resize the ext4 partition.

Need to increase size of root filesystem of buster-lite
https://www.codepool.biz/resize-raspbian-image-qemu-windows.html

```
cp 2020-02-13-raspbian-buster-lite.img raspbian.img
truncate -s +1G raspbian.img
fdisk -l raspbian.img
```
** Get partition start sector  and write it down (532480)
```
fdisk raspbian.img
--> d, 2 (partion 2 has need deleted)
--> n, p, 2, 532480, enter for default end
--> (Remove the signature?) Yes
--> w (write)
sudo losetup -f and write down output (/dev/loop2)
sudo losetup -o $((532480*512)) /dev/loop2 raspbian.img
sudo e2fsck -f /dev/loop2
```
fix if errors
```
sudo resize2fs /dev/loop2
sudo losetup -d /dev/loop2
```

copy it into the `./mender/image-tools` directory.

**Note**: This step installs `chromium`. This will result in a large blue screen showing up and will require user input to continue. This is a good sign, do not be alarmed.

Then, run:
```
export RASPI_IMG=<raspberry pi image filename>
export ENV_FILE=<config.env>
bootstrap-builder/generate-image.sh ${RASPI_IMG} ${ENV_FILE}
```

**Note:** The builder will output your image in `output` named `smartboard-bootstrap-image.img` in the directory where you ran the command.

#### Example Output
```
...
Sending build context to Docker daemon  18.43kB
Step 1/5 : FROM ubuntu:18.04
 ---> 20bb25d32758
Step 2/5 : ARG MENDER_ARTIFACT_VERSION=2.3.0
 ---> Using cache
 ---> 4a912122a514
Step 3/5 : RUN apt-get update && apt-get install -y     simg2img img2simg     qemu-user-static
 ---> Using cache
 ---> 7bfbeabb89ad
Step 4/5 : COPY docker-entrypoint.sh /usr/local/bin/
 ---> Using cache
 ---> 9d23b0b17a84
Step 5/5 : ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
 ---> Using cache
 ---> 9bf9135969af
Successfully built 9bf9135969af
Successfully tagged bcgov/smartboard-prepare-raspbian:latest
Prepared Raspbian with base image:
    /Users/adam/Dropbox/Code/bcgov/queue-management/mender/image-tools/output/smartboard-bootstrap-image.img
Sending build context to Docker daemon  23.55kB
Step 1/5 : FROM ubuntu:18.04
 ---> 20bb25d32758
Step 2/5 : RUN apt-get update && apt-get install -y     parted util-linux
 ---> Using cache
 ---> 5df8281ff68f
Step 3/5 : COPY docker-entrypoint.sh /usr/local/bin/
 ---> b0b14e2c222c
Step 4/5 : COPY pishrink.sh /usr/local/bin/
 ---> a9b1f364a438
Step 5/5 : ENTRYPOINT ["docker-entrypoint.sh"]
 ---> Running in ee5b5fa817fb
Removing intermediate container ee5b5fa817fb
 ---> cf09cd5e6815
Successfully built cf09cd5e6815
Successfully tagged bcgov/smartboard-shrink-image:latest
Copying /image/smartboard-bootstrap-image.img to /output/smartboard-bootstrap-image.img.tmp...
Skipping autoexpanding process...
rootfs: 39646/110880 files (0.1% non-contiguous), 258346/443392 blocks
resize2fs 1.44.1 (24-Mar-2018)
resize2fs 1.44.1 (24-Mar-2018)
Resizing the filesystem on /dev/loop0 to 261385 (4k) blocks.
Begin pass 2 (max = 85373)
Relocating blocks             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 3 (max = 14)
Scanning inode table          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 4 (max = 2798)
Updating inode references     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
The filesystem on /dev/loop0 is now 261385 (4k) blocks long.

sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
Shrunk /output/2018-11-13-raspbian-stretch-lite.img.tmp from 1.8G to 1.1G
Shrunk Image:
    /Users/adam/Dropbox/Code/bcgov/queue-management/mender/image-tools/output/smartboard-bootstrap-image.img
```

#### Building Standalone Image (Optional)
It is possible to run the bootstrapping stage without shrinking the image. The image produced by this step can be useful for debugging and quick prototyping since it takes less time to generate than a fully bootstrapped image. Image shrinking takes time and can sometimes interact adversely with other modifications to the image.

```
export RASPI_IMG=<raspberry pi image filename>
export ENV_FILE=<config.env>
bootstrap-builder/prepare-raspbian/prepare-raspbian ${RASPI_IMG} ${ENV_FILE}
```

### Step 2: Menderizing the Image

**IMPORTANT**: This step needs to be run on a case sensitive filesystem, it's a known issue with `mender-convert`. At the time of writing this it would only work on actual Linux disks (i.e. in a VM or on actual hardware, doesn't work through Dockerization). More information on: [Mender Hub](https://hub.mender.io/t/raspberry-pi-3-model-b-b-raspbian/140/10)

First, download and build the `mender-convert` docker tool:

```
git clone https://github.com/mendersoftware/mender-convert.git
cd mender-convert
git checkout 2.0.x

./docker-build
```

Next create mender convert settings:

1. Update the mender convert config to your needs: nano configs/mender_convert_config

```
MENDER_COMPRESS_DISK_IMAGE=none
MENDER_BOOT_PART_SIZE_MB="256"
MENDER_DATA_PART_SIZE_MB="1000"
IMAGE_ROOTFS_SIZE="-1"
```
2. Set Environment Variable
```
export server-url=<your mender server>
```
3. Update config by running this script:
```
./scripts/bootstrap-rootfs-overlay-production-server.sh \
    --output-dir ${PWD}/rootfs_overlay_demo \
    --server-url ${server-url}
```
Next, to generate the **Menderized** image you will need to provide some information to the conversion tool:

1. `raw-disk-image` - the base Image (Built in **Step #1**), which must be copied into the `./mender-convert/input` directory

**Note**: copy the Raspberry PI Bootstrap image (from previous step) into `./mender-convert/input`.

```
export INPUT_DISK_IMAGE=<bootstrapped image file> 
export ARTIFACT_NAME=<artifact name>

cp ~/git/queue-management/mender/image-tools/output/smartboard-bootstrap-image.img input/

MENDER_ARTIFACT_NAME=SBCRPI3Base ./docker-mender-convert \
   --disk-image input/$INPUT_DISK_IMAGE \
   --config configs/raspberrypi3_config \
   --overlay rootfs_overlay_demo/

This step will produce 3 files:
* `.ext4` - the filesystem of the Menderized image. This file is used later to produce deployment artifacts **(i.e. store it somewhere safe)**
* `.img` - the modified OS which can be flashed to an SD card and run directly on the PI. **(i.e. store it somewhere safe)**
* `.mender` - a deployment artifact, the one produced by this stage will not be used for anything.
```
## Example Output:
```
1/9 Repartitioning raw disk image...
    Detected raw disk image with 2 partition(s).
    Calculating partitions' sizes of the Mender image.
    Adjust Mender disk image size to the total storage size (5000MB).
    Extracting boot partition from raw disk image.
    Storing data in boot.vfat.
    Extracting root filesystem partition from raw disk image.
    Storing data in rootfs.img.
    Creating blank Mender disk image:       
        image size: 5242880000 bytes       
        boot partition size: 46137344 bytes       
        root filesystem size: 2067791872 bytes       
        data partition size: 1048576000 bytes
    Changes in partition table applied.
2/9 Formatting repartitioned raw disk image...
    Creating MS-DOS filesystem for 'boot' partition.
    Creating ext4 filesystem for 'primary' partition.
    Creating ext4 filesystem for 'secondary' partition.
    Creating ext4 filesystem for 'data' partition.
3/9 Setting boot partition...
    Done.
4/9 Setting root filesystem partition...
    Done.
5/9 Setting file system table...
    Done.
6/9 Cleaning intermediate files...
    Partition mappings cleaned.
7/9 Installing Mender to Mender disk image...
    Downloading inventory & identity scripts.
    Installing files.
    Done.
8/9 Installing Bootloader to Mender disk image...
    Building U-Boot related files.
    Installing U-Boot related files.
    Done.
9/9 Creating Mender Artifact...
    Rootfs partition id not set - 'primary' will be used by default.
    Storing data in mender-raspberrypi3-smartboard-base-image-v1.ext4.
    Writing Mender artifact to: /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.mender
    Creating Mender Artifact succeeded.
````
Conversion complete!

The Mender disk image you can provision your device storage with is at:
```
    /mender-convert/output/ mender-raspberrypi3-smartboard-base-image-v1.sdimg\
```
The Mender root file system partition is at:
```
    /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.ext4\
```
The Mender Artifact you can upload to your Mender server to deploy to your devices is at:
```
    /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.mender
```
## Potential Failure:

Occasionally this stage will fail. 

Rerun after restarting Docker:
```
sudo systemctl restart docker
```

**IF** this fails, **RESTART THE COMPUTER** and try again.

### Step 3: Patching Mender Images
Once we've menderized our base image the files system and mender configuration will need to be updated to match our configuration.  Simply run this tool over the image generated by `mender-convert` and it will patch the needed areas.

Return to the `image-tools` directory and run:

```
MENDER_SDIMG=<location of previously produced .img>
mender-image-patcher/mender-image-patcher \
    ${MENDER_SDIMG}
```

**Note**: The above step modifies the `.img` in place. Store the output file somewhere reliable because it is now the core image for flashing SD cards to enable Mender updates on the PI.

### Step 3b: Flashing the Base
The patched `.img` produced above can now be flashed onto SD cards and put into Raspberry PIs.   

You can do this with `dd` or your favorite flashing tool:
```
MENDER_SDIMG=<location of previously produced .img>
dd if=${MENDER_SDIMG} of=/dev/<your-sd-card-device> bs=1m
```

### Step 4: Creating Artifacts
The Mederization step ([Step 2](#Step-2:-Menderizing-the-Image)) produces an `.ext4` file. This file is the basis for generating new deployment artifacts.

Creating an artifact takes 3 parameters:
1. Menderized Image (e.g. the `mender-raspberrypi3-smartboard-base.ext4`)
2. Name of output artifact (e.g. 'smartboard-base-v1') -- **Note**: this name will also be part of the artifact metadata and observable by Mender
3. Config.env file that contains all the configuration options. See `config.example.env` to see what this files should contain

```
# Build the artifact from the base image
MENDER_EXT4=<location of previously produced .ext4>
ARTIFACT_NAME=<name of artifact>
artifact-builder/build-artifact \
    ${MENDER_EXT4} \
    ${ARTIFACT_NAME} \
    config.env
```

This step outputs a new file--`.mender`--which can be uploaded to the Mender web application and deployed to clients running the SD image (produced in [step 3](#-Step-3:-Patching-Mender-Images)).