---
title: Add ISO image to apt sources.list
author: wiloon
type: post
date: 2013-11-01T13:59:58+00:00
url: /?p=5885
categories:
  - Uncategorized

---
## <span style="font-size: 13px;"><a href="http://linuxconfig.org/add-iso-image-to-apt-sourceslist">http://linuxconfig.org/add-iso-image-to-apt-sourceslist</a></span>

Here is a way how to include Debian/Ubuntu ISO image into your /etc/apt/sources.list file. This kind of hack can prove handy in terms of reducing package download during the installation or if you do not have CD/DVD drive available ( or is broken ) on your system.
  
Let&#8217;s assume that we have a Debian ISO image downloaded at the location: /mnt/storage/iSO/debian-i386-DVD-1.iso. As a first step we need to create a mount point to where this ISO image will be mounted to:

mkdir /mnt/debian-dvd

Now we need to add a /etc/fstab entry so the ISO image will be mounted every time we boot the system. Open up /etc/fstab and add a following line:

/mnt/storage/iSO/debian-i386-DVD-1.iso /mnt/debian-dvd/ udf,iso9660 loop 0 0

Once done we can include this local repository into /etc/apt/sources.list. Open up /etc/apt/sources.list file and add:

**NOTE: **change wheezy with your version.

deb file:/mnt/debian-dvd/ wheezy main contrib

All done. What remains is to mount the actual image:

# mount /mnt/debian-dvd/

and update apt&#8217;s depository:

# apt-get update