---
title: 'archlinux  downgrading'
author: "-"
date: 2018-06-19T08:46:56+00:00
url: /?p=12328
categories:
  - Inbox
tags:
  - reprint
---
## 'archlinux  downgrading'
https://wiki.archlinux.org/index.php/Arch_Linux_Archive

replacing your /etc/pacman.d/mirrorlist with the following content:

## 

## Arch Linux repository mirrorlist

## Generated on 2042-01-01

##
  
Server=https://archive.archlinux.org/repos/2014/03/30/$repo/os/$arch
  
Then update the database and force downgrade:

# pacman -Syyuu