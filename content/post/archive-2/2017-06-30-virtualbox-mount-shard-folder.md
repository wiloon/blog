---
title: virtualbox mount shard folder
author: w1100n
type: post
date: 2017-06-30T06:48:08+00:00
url: /?p=10726
categories:
  - Uncategorized

---
https://wiki.archlinux.org/index.php/VirtualBox#Shared\_Folders\_as\_Arch\_Linux_Guest

```bash
  
#manual
  
mount -t vboxsf xxx /mnt/xxx/

#mount on boot
  
#edit /etc/fstab
  
sharedFolderName /path/to/mntPtOnGuestMachine vboxsf uid=user,gid=group,rw,dmode=700,fmode=600,comment=systemd.automount 0 0
  
```