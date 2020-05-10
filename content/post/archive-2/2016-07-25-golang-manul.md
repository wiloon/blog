---
title: golang manul
author: wiloon
type: post
date: 2016-07-25T15:37:44+00:00
url: /?p=9153
categories:
  - Uncategorized

---
[shell]

git clone &#8211;branch pkg-archlinux git://github.com/kovetskiy/manul /tmp/manul
  
cd /tmp/manul
  
makepkg
  
pacman -U *.xz

[/shell]