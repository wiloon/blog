---
title: archlinux chrominum flash
author: "-"
date: 2015-06-28T07:11:42+00:00
url: /?p=7955
categories:
  - Uncategorized

---
## archlinux chrominum flash
install Yaourt

添加Yaourt源至您的 `/etc/pacman.conf`:

```bash
  
[archlinuxcn]
  
#The Chinese Arch Linux communities packages.
  
SigLevel = Optional TrustedOnly
  
Server = http://repo.archlinuxcn.org/$arch
  
```

install yaourt

```bash
pacman -Syu yaourt```

install flash plugin 


```bash
yaourt -S chromium-pepper-flash```

Enable the plugin in chrome://plugins.

https://wiki.archlinux.org/index.php/Yaourt_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.89.E8.A3.85

http://forum.antergos.com/topic/450/psa-chrome-chromium-npapi-deprecation-april-2014/3

https://wiki.archlinux.org/index.php/Chromium#Flash_Player_plugin