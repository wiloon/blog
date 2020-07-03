---
title: qemu-img create
author: wiloon
type: post
date: 2011-12-03T06:22:54+00:00
url: /?p=1676
bot_views:
  - 2
categories:
  - Linux
  - VM

---
To set up your own guest OS image, you first need to create a blank disc image. QEMU has the `qemu-img` command for creating and manipulating disc images, and supports a variety of formats. If you don't tell it what format to use, it will use raw files. The "native" format for QEMU is qcow2, and this format offers some flexibility. Here we'll create a 3GB qcow2 image to install Windows XP on:

qemu-img create -f qcow2 winxp.img 3G