---
title: citrix
author: "-"
date: 2012-11-25T08:15:17+00:00
url: citrix
categories:
  - reprint
tags:
  - reprint
---

# citrix

install, uninstall, and update

```bash
dpkg --list | grep -i icaclient

```

download

https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html

## for ubuntu 24.04

Support for Ubuntu 2404
To support Citrix Workspace app for Linux on Ubuntu 2404, backporting the webkit2gtk library is required. Follow the steps below to backport the library based on your architecture:

For x64 architecture:

Add the following packages for jammy:

sudo apt-add-repository deb http://us.archive.ubuntu.com/ubuntu jammy main

sudo apt-add-repository deb http://us.archive.ubuntu.com/ubuntu jammy-updates main

sudo apt-add-repository deb http://us.archive.ubuntu.com/ubuntu jammy-security main

Install the library:

sudo apt install libwebkit2gtk-4.0-dev

Post successful installation of the library libwebkit2gtk-4.0-dev, remove the the repositories:

sudo apt-add-repository -r deb http://us.archive.ubuntu.com/ubuntu jammy main

For arm64 architecture:

Add the following packages for jammy:

sudo apt-add-repository deb [arch=arm64] http://us.archive.ubuntu.com/ubuntu jammy main

sudo apt-add-repository deb [arch=arm64] http://us.archive.ubuntu.com/ubuntu jammy-updates main

sudo apt-add-repository deb [arch=arm64] http://us.archive.ubuntu.com/ubuntu jammy-security main

Install the library:

sudo apt install libwebkit2gtk-4.0-dev

Post successful installation of the library libwebkit2gtk-4.0-dev, remove the the repositories:

sudo apt-add-repository -r deb [arch=arm64] http://us.archive.ubuntu.com/ubuntu jammy main


```bash
# sudo apt install -f ./icaclient_<version>._amd64.deb
sudo apt install -f ./icaclient_25.05.0.44_amd64.deb
```