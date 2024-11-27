---
title: visualbox share folder
author: "-"
date: 2018-09-30T03:02:56+00:00
url: /?p=12714
categories:
  - Inbox
tags:
  - reprint
---
## visualbox share folder
https://www.jianshu.com/p/21df1811133f

1.Windows创建一个共享文件
  
保存好目录,我的是D:\ virtualbox_share

2.打开共享文件夹选项

3.配置共享文件夹

选择固定分配,共享文件夹选择Windows的共享目录,我的是D:\ virtualbox_share。

共享文件夹名称,是你Ubuntu的共享文件夹名称,我的是virtualbox_share。

自动挂载,不要打钩,重点！

4.挂载: 
  
新建Ubuntu共享文件夹: mkdir/mnt/share

挂载命

sudo mount -t vboxsf [你的windows共享目录] [Ubuntu共享目录]

我是的: 

sudo mount -t vboxsfvirtualbox_share /mnt/share/

完成后,进入cd /mnt/share会看到你Windows共享的目录

5.实现开机自动挂载: 
  
在sudo gedit /etc/fstab文件末添加一项: 

<共享名称> < Ubuntu共享目录> vboxsf defaults 0 0

我的是: 

virtualbox_share /mnt/share/ vboxsf defaults 0 0

网上说的填入

sharing /mnt/sharevboxsf defaults 0 0是错的,会导致开机时候不能进入桌面的！前面应该填入的是<共享名称>！

最后可参考askubuntu.com/questions/252853/how-to-mount-a-virtualbox-shared-folder-at-startup,还是google搜索出来的解决方法靠谱

作者: Janny238
  
链接: https://www.jianshu.com/p/21df1811133f
  
來源: 简书
  
简书著作权归作者所有,任何形式的转载都请联系作者获得授权并注明出处。