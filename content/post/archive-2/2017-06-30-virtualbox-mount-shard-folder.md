---
title: virtualbox mount shard folder
author: "-"
type: post
date: 2017-06-30T06:48:08+00:00
url: /?p=10726
categories:
  - Uncategorized

---
# virtualbox mount shard folder
https://wiki.archlinux.org/index.php/VirtualBox#Shared_Folders_as_Arch_Linux_Guest

```bash
  
#manual
  
mount -t vboxsf xxx /mnt/xxx/

#mount on boot
  
#edit /etc/fstab
  
sharedFolderName /path/to/mntPtOnGuestMachine vboxsf uid=user,gid=group,rw,dmode=700,fmode=600,comment=systemd.automount 0 0
  
```