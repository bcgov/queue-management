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

- **Ubuntu 18.04**
- 10 gigabytes of storage

### Step 1: Building Base Image (Bootstrapping)
First, download the latest [Raspbian Lite Image](https://downloads.raspberrypi.org/raspbian_lite_latest) and copy it into the `./mender/image-tools` directory.

Then, run:
```
RASPI_IMG=<raspberry pi image filename>
bootstrap-builder/generate-image.sh ${RASPI_IMG}
```

**Note**: This process modifies the input file (Raspbian image) in place.

#### Example Output
```
...
The filesystem on /dev/loop0 is now 239393 (4k) blocks long.

sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
Shrunk /output/2018-11-13-raspbian-stretch-lite.img from 1.8G to 984M
```

#### Building Standalone Image (Optional)
It is possible to run the bootstrapping stage without shrinking the image. The image produced by this step can be useful for debugging and quick prototyping since it takes less time to generate than a fully bootstrapped image. Image shrinking takes time and can sometimes interact adversely with other modifications to the image.

```
RASPI_IMG=<raspberry pi image filename>
bootstrap-builder/prepare-raspbian/prepare-raspbian ${RASPI_IMG} config.env 
```

### Step 2: Menderizing the Image

**IMPORTANT**: This step needs to be run on a case sensitive filesystem, it's a known issue with `mender-convert`. At the time of writing this it would only work on actual Linux disks (i.e. in a VM or on actual hardware, doesn't work through Dockerization). More information on: [Mender Hub](https://hub.mender.io/t/raspberry-pi-3-model-b-b-raspbian/140/10)

First, download and build the `mender-convert` docker tool:

```
git clone https://github.com/mendersoftware/mender-convert.git
cd mender-convert
git checkout 2743366

./docker-build
```

Next, to generate the **Menderized** image you will need to provide some information to the conversion tool:

1. `raw-disk-image` - the base Image (Built in **Step #1**), which must be copied into the `./mender-convert/input` directory
2. `artifact-name` - the name of the output image, also stored as metadata within the image itself to be read by Mender
3. `server-url` - URL Which will be Hosting Mender - e.g. [https://mender.pathfinder.gov.bc.ca]
4. `storage-total-size-mb` - total Image size (Mb) - The total store needs to be more than double the size of the base Image
5. `data-part-size-mb` - total size of persistent data partition

```
RASPI_IMG=<raspberry pi image filename>
ARTIFACT_NAME=<artifact name>
SERVER_URL=<https://your.mender.application.com>
./docker-mender-convert from-raw-disk-image \
    --raw-disk-image "input/${RASPI_IMG}" \
    --artifact-name "${ARTIFACT_NAME}" \
    --device-type "raspberrypi3" \
    --mender-client "/mender" \
    --bootloader-toolchain "arm-linux-gnueabihf" \
    --server-url "${SERVER_URL}" \
    --storage-total-size-mb "5000" \
    --data-part-size-mb "1000"
```

This step will produce 3 files:
* `.ext4` - the filesystem of the Menderized image. This file is used later to produce deployment artifacts **(i.e. store it somewhere safe)**
* `.sdimg` - the modified OS which can be flashed to an SD card and run directly on the PI. **(i.e. store it somewhere safe)**
* `.mender` - a deployment artifact, the one produced by this stage will not be used for anything.

#### Example Output
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
Conversion complete!
The Mender disk image you can provision your device storage with is at:         
    /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.sdimg
The Mender root file system partition is at:
    /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.ext4
The Mender Artifact you can upload to your Mender server to deploy to your devices is at:         
    /mender-convert/output/mender-raspberrypi3-smartboard-base-image-v1.mender
```

### Step 3: Patching Mender Images
Once we've menderized our base image the files system and mender configuration will need to be updated to match our configuration.  Simply run this tool over the image generated by `mender-convert` and it will patch the needed areas.

Return to the `image-tools` directory and run:

```
MENDER_SDIMG=<location of previously produced .sdimg>
mender-image-patcher/mender-image-patcher \
    ${MENDER_SDIMG}
```

**Note**: The above step modifies the `.sdimg` in place. Store the output file somewhere reliable because it is now the core image for flashing SD cards to enable Mender updates on the PI.

### Step 3b: Flashing the Base
The patched `.sdimg` produced above can now be flashed onto SD cards and put into Raspberry PIs.   

You can do this with `dd` or your favorite flashing tool:
```
MENDER_SDIMG=<location of previously produced .sdimg>
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