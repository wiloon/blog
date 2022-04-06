---
title: VirtualBox 共享文件夹
author: "-"
date: 2013-07-30T03:24:15+00:00
url: /?p=5745
categories:
  - Uncategorized

tags:
  - reprint
---
## VirtualBox 共享文件夹
http://blkstone.github.io/2016/08/05/virtualbox-shared-folder/

前提是已经安装过增强功能。

步骤
  
设置宿主机共享文件夹
  
重启完成后点击"设备(Devices)" -> 共享文档夹(Shared Folders)菜单,添加一个共享文档夹,选项固定和临时是指该文档夹是否是持久的。共享名能够任取一个自己喜欢的,比如"gongxiang",尽量使用英文名称。

挂载共享文件夹
  
重新进入虚拟Ubuntu,在命令行终端下输入: 

sudo mkdir /mnt/shared
  
sudo mount -t vboxsf gongxiang /mnt/shared
  
其中"gongxiang"是之前创建的共享文档夹的名字。OK,现在Ubuntu和主机能够互传文档了。

假如您不想每一次都手动挂载,能够在/etc/fstab中添加一项

gongxiang /mnt/shared vboxsf rw,gid=username,uid=username,auto 0 0
  
以上的 vboxsf 是群组名称 username 是你的 用户名 就是 /home/下的文件夹名称
  
/mnt/shared 是挂载目录

取消挂载
  
sudo umount -f /mnt/shared
  
注意: 
  
共享文档夹的名称千万不要和挂载点的名称相同。

参考资料
  
[1] Virtualbox虚拟机Ubuntu共享文件夹设置自动挂载