---
title: Grub2配置详解(转)
author: "-"
date: 2011-11-26T09:14:14+00:00
url: /?p=1640
categories:
  - Linux
tags:
  - reprint
---
## Grub2配置详解(转)

grub.cfg 默认为只读，要修改前先设为可写
  
sudo chmod +w /boot/grub/grub.cfg

set default=0
  
# 默认为0
  
insmod jpeg
  
# 添加jpg支持，如要使用png或tga文件做背景，加上 insmod png或insmod tga
  
insmod ext2
  
# 除了用作启动的分区外，其他分区格式可在menu底下再添加
  
set root=(hd0,7)
  
# 设定root分区
  
search -no-floppy -fs-uuid -set f255285a-5ad4-4eb8-93f5-4f767190d3b3
  
# 设定uuid=\****的分区为root，和上句重复，可删除
  
# 以下为终端配置
  
if loadfont /usr/share/grub/unicode.pf2 ; then
  
# 设置终端字体，unicode.pf2支持中文显示
  
set gfxmode=640x480
  
# 设置分辨率，默认为 640x480，可用800x600，1024x768，建议跟你想设定的图片大小一致
  
insmod gfxterm
  
# 插入模块 gfxterm，支持中文显 示，它还支持 24 位图像
  
insmod vbe
  
# 插入 vbe 模块，GRUB 2 引入很多模块的东西，要使用它，需要在这里加入
  
if terminal_output gfxterm ; then true ; else
  
# For backward compatibility with versions of terminal.mod that don't
  
# understand terminal_output
  
terminal gfxterm
  
# 设置 GRUB 2 终端为 gfxterm
  
fi
  
fi
  
set timeout=10
  
background_image (hd0,7)/boot/images/1.jpg
  
# 设置背景图片
  
### END /etc/grub.d/00_header

### BEGIN /etc/grub.d/05_debian_theme ###
  
set menu_color_normal=white/black
  
set menu_color_highlight=cyan/black
  
# 这两行为 Debian 下的菜单颜色设置，如果默认的话，你会发现背景完全被蓝色挡住了，你需要修改 blue 为 black，这样背景就会出现
  
### END /etc/grub.d/05_debian_theme ###

# 10_linux 为自动添加的当前root分区linux引导项
  
### BEGIN /etc/grub.d/10_linux ###
  
# 菜单项，要包括 menuentry 双引号" " 和大括号 { }才完整，否则不显示菜单
  
menuentry "Ubuntu, Linux 2.6.31-9-386" {
  
insmod ext2
  
set root=(hd0,7)
  
search -no-floppy -fs-uuid -set f255285a-5ad4-4eb8-93f5-4f767190d3b3
  
# 这句与set root=(hd0,7)重复，可删除
  
linux /boot/vmlinuz-2.6.31-9-386 root=UUID=f255285a-5ad4-4eb8-93f5-4f767190d3b3 ro quite splash
  
# 不喜欢看到一长串的， roo=UUID=\***可用root=/dev/sda7代替
  
initrd /boot/initrd.img-2.6.31-9-386
  
}
  
### END /etc/grub.d/10_linux ###

### BEGIN /etc/grub.d/20_memtest86+ ###
  
menuentry "Memory test (memtest86+)" {
  
linux16 /boot/memtest86+.bin
  
}
  
### END /etc/grub.d/20_memtest86+ ###

# 自动添加存在于其他分区的系统引导项
  
### BEGIN /etc/grub.d/30_os-prober ###
  
# windows 启动菜单
  
menuentry "Windows Vista (loader) (on /dev/sda1)" {
  
insmod ntfs
  
# windows格式为ntfs，或为fat32改为 insmod fat
  
set root=(hd0,1)
  
search -no-floppy -fs-uuid -set ece067d2e067a196
  
# 可删除
  
# grub2比较先进的地方就是如果发现windows启动是通过ntldr 引导的，定为2000/xp/2003，会在这加上 drivemap -s (hd0) ${root} ，作用相当于grub的map，可正常启动非第一硬盘的xp/2003系统。
  
chainloader +1
  
}
  
# 查找到其他分区上的linux系统并自动添加
  
menuentry "Ubuntu karmic (development branch) (9.10) (on /dev/sda3)" {
  
insmod ext2
  
set root=(hd0,3)
  
search -no-floppy -fs-uuid -set 4d893970-0685-44ed-86b3-1de45b2db84a
  
linux /boot/vmlinuz-2.6.31-9-generic root=/dev/sda3
  
initrd /boot/initrd.img-2.6.31-9-generic
  
}
  
# 若存在macos会自动在这里添加。
  
### END /etc/grub.d/30_os-prober ###
  
# 以下为手动添加的菜单项
  
### BEGIN /etc/grub.d/40_custom ###
  
menuentry "CDLinux"{
  
set root=(hd0,8)
  
linux /CDlinux/bzImage root=/dev/ram0 vga=791 CDL_LANG=zh_CN.UTF-8
  
initrd /CDlinux/initrd
  
}
  
### END /etc/grub.d/40_custom ###

# 手动添加时，硬盘编号从0开始(hd0)，主分区编号从1开始(hd0,1)，逻辑分区从5开始(hd0,5)

二、grub2终端部分命令介绍
  
在出现选择菜单时，按C进入终端命令行模式，按E进入当前菜单项编辑模式 (和grub一样) ，编辑中按Ctrl + C退出，按Ctrl + X 以编辑内容启动。

1. help
  
查看命令用法，显示所有可用命令
  
help search
  
search 命令用法
  
2. ls
  
列出当前的所有设备。如 (hd0) (hd0,1) (hd0,5) (hd1) (hd1,1) (hd1,2) .......
  
ls -l
  
详细列出当前的所有设备。对于分区，会显示其label及uuid。
  
ls /
  
列出当前设为root的分区下的文件
  
ls (hd1,1)/
  
列出(hd1,1)分区下文件
  
3. search
  
search -f /ntldr
  
列出根目录里包含ntldr文件的分区，返回为分区号
  
search -l LINUX
  
搜索label是LINUX的分区。
  
search -set -f /ntldr
  
搜索根目录包含ntldr文件的分区并设为root，注意如果多外分区含有ntldr文件，set 失去作用。
  
4. loopback
  
loopback命令可用于建立回放设备，如
  
loopback lo0 (hd1,1)/abc.iso

可以使用lo0设备来访问abc.iso里的内容，比如说，可以从abc.iso里的软盘映像中启动
  
loopback lo0 (hd1,1)/aa.iso
  
linux (lo0)/memdisk
  
initrd (lo0)/abc.img

要删除某一回放设备，可以使用-d参数:
  
loopback -d lo0
  
5. set
  
使用set可以设置变量的值
  
set root=
  
set timeout=
  
需要调用变量的值时，使用${AA}，如set root=(hd1,1)
  
则${root}=(hd1,1)
  
6. pager
  
分页显示。
  
set pager=1
  
满页时暂停，按space继续
  
set pager=0
  
取消分页
  
7. linux
  
linux取代grub中的kernel

三、
  
单linux系统或
  
硬盘安装时iso放在C盘，umount /isodevice引起的误认为单系统
  
不能出现菜单项的几种处理方法。
  
1. 开机自检后时按几下shift键，可调出菜单项
  
2. sudo update-grub
  
重建grub.cfg，会发现新的系统而改写grub.cfg，一般能出现菜单项。
  
3.如第二种方法不能解决，直接修改grub.cfg
  
把在### BEGIN /etc/grub.d/30_os-prober中的这一段
  
if keystatus; then
  
if keystatus -shift; then
  
set timeout=-1
  
else
  
set timeout=0
  
fi
  
else
  
if sleep$verbose -interruptible 3 ; then
  
set timeout=0
  
fi
  
fi
  
删除或修改三处set timeout=<大于0>

四、双硬盘双系统 Grub Loading时间过长的解决方案

grub2的boot.img设定root的uuid从第一分区开始搜索分区的/boot/grub下的模块并加载， 如果linux分区处于第二硬盘甚至第三硬盘，会导致搜索时间过长而，出现菜单时间会长达10多秒。
  
对双 (多) 硬盘的情况建议把grub安装在ubuntu所在硬盘的mbr上，/boot分区或 / 分区 尽量靠前，并设该硬盘为启动盘，会大大缩短启动时间。

五、grub2几种修复方法

1. 双系统重装windows造成grub2被改写的修复
  
方法一 grub4dos0.4.4
  
在Windows启动项上加上grub4dos启动 (不多说了，看置顶贴) ，重启选择进入grub，在命令行下输入(/boot单独分区的去掉 /boot)
  
代码:

grub>find -set-root /boot/grub/core.img
  
grub>kernel /boot/grub/core.img
  
grub>boot

进入grub2菜单，进入系统后再执行
  
代码:

sudo grub-install /dev/sd？

方法二 进入Livecd 后修复 (感谢billbear)
  
引用:
  
sudo -i
  
mount 你的根分区 /mnt
  
mount 你的/boot 分区 /mnt/boot #如果有的话
  
# 挂载你其他的分区，如果有的话
  
# 重建grub到sda的mbr
  
grub-install -root-directory=/mnt /dev/sda

2. 由于root分区uuid改变造成的不能正常启动，只能进入grub rescue模式的修复

代码:
  
grub rescue>set
  
grub rescue>prefix=(hd？,？)/grub
  
grub rescue>root=hd？,？
  
grub rescue>set root=hd？,？
  
grub rescue>set prefix=(hd？,？)/boot/grub
  
grub rescue>set
  
grub rescue>root=hd？,？
  
grub rescue>prefix=(hd？,？)/boot/grub
  
grub rescue>insmod /boot/grub/normal.mod
  
grub rescue>normal

这时就可以调出 /boot/grub/grub.cfg，修改相应uuid，
  
改到命令行下
  
grub>insmod /boot/grub/linux.mod
  
grub>set root=hd？,？
  
grub>linux /boot/vmlinuz-\*** root=/dev/sd？？
  
grub>initrd /boot/initrg.img-\****
  
进入系统
  
hd？,？ 是grub文件所在分区 sda？ 是/分区。

3. grub模块和配置文件grub.cfg受损无法启动时修复

Livcd启动进入试用
  
引用:
  
sudo -i
  
mount 你的根分区 /mnt
  
mount 你的/boot 分区 /mnt/boot #如果有的话
  
# 挂载你其他的分区，如果有的话

# 重建grub到sda的mbr
  
grub-install -root-directory=/mnt /dev/sda

# 重建grub.cfg
  
mount -bind /proc /mnt/proc
  
mount -bind /dev /mnt/dev
  
mount -bind /sys /mnt/sys
  
chroot /mnt update-grub
  
umount /mnt/sys
  
umount /mnt/dev
  
umount /mnt/proc

六、 一些补充说明

1. chainloader
  
grub2将支持 chainloader /file 的用法。
  
目前支持的文件只有 grub2 的 boot.img 和 grub4dos 的grldr 和 grub.exe。希望正式版能支持 ntldr bootmgr peldr 等文件。

2. drivemap
  
drivemap 兼容 grub 的 map，主要用于只能从 (hd0) 引导启动的系统如 win2000 xp 2003，可以象 map 用法一样如:

menuentry "Windows XP" {
  
insmod ntfs
  
drivemap (hd0) (hd1)
  
drivemap (hd1) (hd0)
  
set root=(hd1,1)
  
chainloader +1
  
}

实际上 drivemap 有了更方便的用法:
  
menuentry "Windows XP" {
  
insmod ntfs
  
set root=(hd1,1)
  
drivemap -s (hd0) ${root}
  
chainloader +1
  
}

3. grub2 引导软盘img镜像启动
  
比如要加载(hd1,1)根目录下的 a.img 镜像，先把 memdisk 从 memdisk.gz 中解压出来，用法是:
  
linux (hd1,1)/memdisk #镜像文件超过2.88M要加上 c=\* h=\* s=*
  
initrd (hd1,1)/a.img
  
boot

现在有bug，加载memdisk会自动重启，beta2还没修正。
