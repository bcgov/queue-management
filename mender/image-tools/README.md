# Building Images to Prepare for Mender Deployment

## Prerequisites

- **Ubuntu 18.04**
- 10 gigabytes of storage

## Step 1: Building Base Image (Bootstrapping)

The first image that needs to be built is the base raspbian image that will be "menderized". This image is a modified version of the released image from Raspbian. It has the majority of the application packaged into it in way that can be deployed directly, or run through "menderization" to be used in a mender deploy.

First download the raspbian image from: [Raspberry Pi Images](https://www.raspberrypi.org/downloads/raspbian/). Download the [Raspbian Lite Image](https://downloads.raspberrypi.org/raspbian_lite_latest).

To shrink and prime the image run:
```
bootstrap-builder/generate-image.sh 2018-11-13-raspbian-stretch-lite.img
```

### Expected Output
```
...
The filesystem on /dev/loop0 is now 239393 (4k) blocks long.

sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
sh: 1: udevadm: not found
Shrunk /output/2018-11-13-raspbian-stretch-lite.img from 1.8G to 984M
```

### Building Standalone Image

If you want to build an image that will run on it's own you need to just run the bootstrapping without running the shrinking too.

```
bootstrap-builder/prepare-raspbian/prepare-raspbian 2018-11-13-raspbian-stretch-lite.img config.env 
```

## Step 2: Menderizing the Image

The next step of the process involves turning the standard Raspbian image into **Menderized** image which can do OTA updates. To do this we will use the `mender-convert` utility.

### IMPORTANT:
This step needs to be run on a case sensitive filesystem, it's a known issue with `mender-convert` and they will hopefully have it dealt with soon. At the time of writing this would only work on actual Linux disks (IE in a VM or on actual hardware, doesn't work through Dockerization). More information on: (Mender Hub)[https://hub.mender.io/t/raspberry-pi-3-model-b-b-raspbian/140/10]

```
git clone https://github.com/mendersoftware/mender-convert.git
cd mender-convert
git checkout 2743366

./docker-build
```

To generate the **Menderized** image you will need to provide some information to the conversion tool:

1. Base Image (Built in **Step #1**)
2. URL Which will be Hosting Mender [https://mender.pathfinder.gov.bc.ca]
3. The service certificate the devices need to register with (use `server.crt` in this folder and store it in the `input` folder, which will be mounted in the docker image)
4. The total store needs to be more than double the size of the source image

### WARNING:
With the input image you need to have it in the same folder as the convert tool, or a sub-folder as it's volumed into the conversion tool via Docker and paths get mangled around. I suggest using the `input` folder, as that's the paradigm the tool has been using.

```
./docker-mender-convert from-raw-disk-image \
    --raw-disk-image "input/2018-11-13-raspbian-stretch-lite.img" \
    --artifact-name "smartboard-base-image-v1" \
    --device-type "raspberrypi3" \
    --mender-client "/mender" \
    --bootloader-toolchain "arm-linux-gnueabihf" \
    --server-url "https://mender.pathfinder.gov.bc.ca" \
    --storage-total-size-mb "5000" \
    --data-part-size-mb "1000"
```

Building for Demo server:
```
./docker-mender-convert from-raw-disk-image \
    --raw-disk-image "input/raspbian-lite-shrunk.img" \
    --artifact-name "smartboard-base" \
    --device-type "raspberrypi3" \
    --mender-client "/mender" \
    --bootloader-toolchain "arm-linux-gnueabihf" \
    --demo-host-ip 10.0.0.5 \
    --demo \
    --storage-total-size-mb "5000" \
    --data-part-size-mb "1000"
```

### Expected Output:
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

## Step 3: Patching Mender Images

Once we've menderized our base image the files system and mender configuration will need to be updated to match our configuration.  Simply run this tool over the image generated by `mender-convert` and it will patch the needed areas.

**NOTE:** You only need to patch the `.sdimg` the artifact will be patched automatically when it builds.

```
mender-image-patcher/mender-image-patcher \
    mender-raspberrypi3-smartboard-base-image-v1.sdimg
```

## Step 3b: Flashing the Base

Mender convert will produce 3 image files. Only two we are really concerned with.  The first named `mender-raspberrypi3-smartboard-base.sdimg` (`.sdimg` is the part we're interested in) is the file you will flash to an SD card. You can do this with `dd` or your favorite flashing tool.

```
dd if=mender-raspberrypi3-smartboard-base.sdimg /dev/your-sd-card-device bs=1m
```

## Step 4: Creating Artifacts

The other image you will be interested in is the `mender-raspberrypi3-smartboard-base.ext4`, it is the file that you will use to build artifacts on top of. The Menderized image is what is paired with your Mender Host, and creating the image is only required when you need to change the base image or change hosts.

Creating an artifact takes 3 parameters:
1. Menderized Image (the `mender-raspberrypi3-smartboard-base.ext4`)
2. Name of output artifact ('smartboard-base-v1')
3. Config.env file that contains all the configuration options. See `config.example.env` to see what this files should contain

Then you can run:

```
# Run this the first time to make sure the container is built
artifact-builder/docker-build

# Build the artifact from the base image
artifact-builder/build-artifact \
    mender-convert-output/mender-raspberrypi3-smartboard-base.ext4 \
    smartboard-base-v1 \
    config.env
```

Now you've created a new `smartboard-base-v1.mender` and you and upload this in the Mender web administration at: [https://mender.pathfinder.gov.bc.ca/]
