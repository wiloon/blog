---
title: hyperv arch
author: wiloon
type: post
date: 2019-04-01T06:53:10+00:00
url: /?p=14064
categories:
  - Uncategorized

---
https://wiki.archlinux.org/index.php/Hyper-V

Internal switch
  
Xorg
  
xf86-video-fbdev

```bash/boot/loader/entries/arch.conf
title Arch Linux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options video=hyperv_fb:1920x1080 root=PARTUUID=xxxx-xxxx rw
```

Enhanced Session Mod
  
Xrdp

~/.xinitrc
   
exec startxfce4

git clone https://github.com/Microsoft/linux-vm-tools
  
cd linux-vm-tools/arch
  
./makepkg.sh
  
./install-config.sh

Set-VM -VMName **Your\_Arch\_Machine** -EnhancedSessionTransportType HvSocket

### network

在虚拟机栏中右键点击虚拟机>设置>添加硬件
  
选择&#8221;网络适配器&#8221;
  
点击添加按钮
  
添加 Default switch.
  
Default switch默认会做nat,添加 后虚拟机可以正常访问网络.但Default switch的ip/网段每次重启会变,如果 需要 固定ip,需要另外手动新建一个交换机sw0
  
Hyper-V 管理器>右侧操作栏>虚拟交换机管理器
  
在windows中打开网络适配器设置,手动设置sw的
  
ip为 192.168.80.1
  
网关可以不填
  
dns: 192.168.1.xxx

#### linux里

手动测试sw0的ip : 192.168.80.2
  
Gateway 不要设置, 两个网卡 对应default switch的设置默认网关,sw0不设置
  
DNS: 192.168.1.xxx

### 问题

遇到过一次虚拟机不能访问外网, 确认linux网络 配置没有问题, 重启windows解决了.