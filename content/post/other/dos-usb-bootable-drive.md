---
title: FreeDOS USB Bootable Drive
author: "-"
date: 2012-04-02T12:39:34+00:00
url: /?p=2728
categories:
  - Linux
tags:
  - reprint
---
## FreeDOS USB Bootable Drive
http://www.aselabs.com/articles.php?id=243

Author
  
Aron Schatz
  
Posted
  
March 3, 2008
  
Views
  
61988

We all use flash drives instead of the older floppy disk standard of last century. The problem with USB is that it isn't made to boot like a floppy disk. Motherboards now support booting from USB drives made to look like hard drives. This guide is a step by step process running on Ubuntu.
  
Tags Guides USB DOS Boot
  
Page 1: USB Boot

Intro:
  
Flash drives are really ubiquitous. If you look around your computer desk, you will probably find a few USB mass storage devices near your work area. They are a boon for taking documents from one computer to the next and are fast and simple to use. They replaced the floppy that the ZIP disk could not supplant. The one area that USB flash drives are lacking is the ability to boot. Even though many computer motherboards support USB booting, it is difficult to get the right combination. Using this guide, you will be able to make a bootable USB "hard drive."

Hard Drive:
  
There are a few ways to boot USB devices today. The first way (and the one we will be using in this guide) is to make the USB flash drive look like a regular hard drive. Most flash drives are already setup this way. What does a regular hard drive "look" like? It has a master boot record as well as individual partitions on the drive each with their own boot sector. The other type of bootable USB is known as the supperfloppy type. This makes a flash drive act as one huge floppy disk. A floppy disk is the partition. There is no master boot record. There is only a boot sector. If you have a flash drive formated this way, it won't show any partitions in Linux. Instead it will look like /dev/sdb whereas a normal drive with a partition would be /dev/sdb1. Motherboard support is getting better for booting USB, but some of my motherboards still refuse to boot using this guide. Once I find a way to do the super-floppy method, I will make an additional guide. If you know how to do this, please email me.

Why DOS?:
  
You may be asking why I'm going to boot into DOS. The simple reason is that most computers don't come with a floppy drive and many motherboard manufactures still require DOS to flash their boards. While it is true that some boards have a flashing utility in the BIOS, others (such as Intel's) require you to boot into DOS. Using DOS is the safest way to flash a motherboard. I wouldn't trust using Windows or even Linux (if such flashing programs were made). Too much stuff is running in the background to cause trouble.

System Setup:
  
This guide will demonstrate how to make a DOS USB boot drive using FreeDOS. We are going to use Ubuntu 7.10 which you can download for free at http://www.ubuntu.com. You can use the Live CD to follow this guide if you are still using Windows. The only software that you will need to install is the package called "dosemu" which is very simple to install from Synaptic or the console.

Open up Applications -> Accessories - > Terminal.

That prompt you see will look something like this...

```bash
  
aronschatz@asetest2:~$
  
```

And that is how you will enter commands in.

```bash
  
aronschatz@asetest2:~$ sudo apt-get install dosemu
  
```

The above command will install dosemu as well as the FreeDOS component automatically. Now you are set to follow the guide. The other thing you need to worry about is where the USB flash drive shows up in /dev. Mine was mounted as /dev/sdb, but yours may be completely different. This guide uses /dev/sdb as the flash drive.

The flash drive will be completely erased so be sure to back up the contents before proceeding with this guide.

Step 1: Prepare the drive
  
The first step will wipe the MBR of the drive as well as the partition table information on it. dd is a dangerous command if you don't know what you are doing. If you make a mistake, you can wipe your regular hard drive out.

```bash
  
aronschatz@asetest2:~$ sudo dd if=/dev/zero of=/dev/sdb bs=512 count=1
  
1+0 records in
  
1+0 records out
  
512 bytes (512 B) copied, 0.00124495 seconds, 411 kB/s
  
aronschatz@asetest2:~$
  
```

Now you are finished preparing the drive and can continue.

Step 2: Partition the drive
  
This will be the pictorial step. The basic layout is to use cfdisk to create a single bootable partition of FAT16 and write the information to the drive.

note: umount the usb drive firstly.

```bash
  
aronschatz@asetest2:~$ sudo cfdisk /dev/sdb
  
```

The flash drive is ready to be partitioned. We want to add a "New" partition.
  
You are adding a new "Primary" partition. Then it will ask for the size and such, just accept the defaults and press enter until you get to the main screen.
  
You want to mark the partition as "Bootable."
  
Now you need to change the "Type" of the partition to a FAT16. It would be 06 for FAT16.
  
Once you are back to the make screen, you need to "Write" the changes to the disk and accept any prompts that come up. Then you can "Quit" cfdisk and return which will show this...

```bash
  
Disk has been changed.

WARNING: If you have created or modified any
  
DOS 6.x partitions, please see the cfdisk manual
  
page for additional information.
  
aronschatz@asetest2:~$
  
```

**Step 3: Format the partition**
  
With the partition made in the previous step, you know need to put a filesystem on it. The command mkdosfs is pretty easy to figure out.

  
    Code
  
  
    ```bash
 aronschatz@asetest2:~$ sudo mkdosfs -I /dev/sdb1
 mkdosfs 2.11 (12 Mar 2005)
 aronschatz@asetest2:~$
 ```
  
  
    Step 4: Edit .dosemurc 
 You need to make the USB flash drive show up in dosemu. To do this, you need to make a file called ".dosemurc" in your home directory. The easiest way is to use gedit and save the file. You can use any text editor of your choice.
  

```bash
  
aronschatz@asetest2:~$ sudo emacs /root/.dosemurc
  
```

The file should look like this...

```bash
  
$_hdimage = "drives/* /tmp /dev/sdb1"
  
```

Basically that means to parse the directories in ./drives/ and then use /dev/sdb1. It will make everything into a fixed disk. Save and close the file.

**Step 5: sys the drive**

You need to start the emulator for dos. If the command brings up errors such as below, you need to unmount the flash drive.

#### Code

```bash
  
aronschatz@asetest2:~$ sudo dosemu
  
In file included from built-in global.conf:677
  
from built-in global.conf:634
  
from built-in global.conf:648
  
Error in : (line 648)You specified '/dev/sdb1' for read-write Direct Partition Access,
  
it is currently mounted read-write on '/media/disk' !!!1 error(s) detected while parsing the configuration-file
  
aronschatz@asetest2:~$
  
```

Here we see the problem. The flash drive is mounted. This command will unmount the drive.

```bash
  
aronschatz@asetest2:~$ sudo umount /dev/sdb1
  
```

Now try to start dosemu again...

```bash
  
aronschatz@asetest2:~$ sudo dosemu
  
```

This command should bring up another prompt that is basically FreeDOS. In this new window, type the series of commands...

  
    Code
  
  
    ```bash
 C:> z:
 Z:> sys f:
 FreeDOS System Installer v3.2, Aug 18 2006Processing boot sector...
 Reading old bootsector from drive F:
 FAT type: FAT16
 Old boot sector values: sectors/track: 62, heads: 4, hidden: 62
 Default and new boot sector values: sectors/track: 62, heads: 4, hidden: 62
 Root dir entries = 512
 FAT starts at sector (62 + 1)
 Root directory starts at sector (PREVIOUS + 245 * 2)
 Boot sector kernel name set to KERNEL SYS
 Boot sector load segment set to 60h
 writing new bootsector to drive F:Copying KERNEL.SYS...
 45341 Bytes transferred
 Copying COMMAND.COM...
 66945 Bytes transferred
 System transferred.
 Z:>exitemu
 ```
  
  
    First you type "Z:" to get into the Z drive which holds all the FreeDOS tools and binaries. Then the command "sys f:" tells it to make the F: drive a system drive by copying kernerl.sys and command.com. Once that is completed, "exitemu" exits out of the dosemu program.
  
  
  
  
    Step 6: install mbr
 ```bash
 #install-mbr -v -p [boot partition #] /dev/<usb device>
 # Note: no partition, root device only
 sudo install-mbr -v -p 1 /dev/sdb
 ```
  
  
    Step 7: smartdrv.exe, himemx.exe, JEMM386.EXE
 download freefos iso from http://www.freedos.org/, and extract HIMEMX.EXE, JEMM386.EXE to the usb drive
 Create file CONFIG.SYS on /dev/sdb1 , add two lines:
 DEVICE=HIMEMX.EXE
 DEVICE=JEMM386.EXE
  
  
    download and copy smartdrv.exe to /dev/sdb1
  
  
    Step 8: Copy your own utilities to the drive and boot
  
  
    Now the drive is usable for booting. You can now copy files onto the FAT16 partition. This is a pure DOS boot, so you can include any sort of DOS utilities. Once you are finished loading the drive up, restart the computer and force the BIOS to boot off the USB flash drive. With any luck, you will see a FreeDOS screen telling you to input the date and time. Just press enter and you now have a working DOS system off of your flash drive.
  
  
    Conclusion:
  
  
    With a working DOS USB flash drive, you can perform a number of useful tasks including flashing ROMs and using other DOS utilities. FreeDOS is an example of free and open source software. When using bootdisks that contain MS-DOS, you are not licensed to use it since you didn't pay for it. Stay tuned to find out why I needed a DOS USB bootable drive in the first place. Buy a flash drive!
  
  
    http://wiki.gentoo.org/wiki/Bootable_DOS_USB_stick
 http://www.dosemu.org/docs/README/1.2/config.html
 https://jeremy.visser.name/2007/09/create-a-bootable-freedos-usb-flash-drive-in-linux/
 http://www.ilikelinux.com/tips-and-howtos/creating-a-knoppix-or-freedos-usb-stick-in-linux
  
