---
title: 'archlinux  downgrading'
author: wiloon
type: post
date: 2018-06-19T08:46:56+00:00
url: /?p=12328
categories:
  - Uncategorized

---
https://wiki.archlinux.org/index.php/Arch\_Linux\_Archive

replacing your /etc/pacman.d/mirrorlist with the following content:

## 

## Arch Linux repository mirrorlist

## Generated on 2042-01-01

##
  
Server=https://archive.archlinux.org/repos/2014/03/30/$repo/os/$arch
  
Then update the database and force downgrade:

# pacman -Syyuu