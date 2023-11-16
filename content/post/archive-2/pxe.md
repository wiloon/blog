---
title: PXE
author: "-"
date: 2018-03-18T07:37:02+00:00
url: /?p=11995
categories:
  - Inbox
tags:
  - reprint
---
## PXE

[http://blog.csdn.net/nirendao/article/details/76012939](http://blog.csdn.net/nirendao/article/details/76012939)

PXE启动原理以及与普通Linux启动的对比
  
原创 2017年07月24日 11:28:36 标签: PXE /boot /Linux 1011
  
关于PXE部署的详细配置的文章已经有不少了,这篇文章主要讲一下PXE启动的原理以及PXE启动和普通Linux启动的对比。

一、PXE启动原理:

原理图如下:

DHCP的用途是: 提供client network参数和TFTP服务器的地址,最初的bootstrap程序 (即DHCP或BootP等) 和所需的程序。
  
首先,PXE client端 (BIOS里面的PXE固件) 广播一个DHCPDISCOVER的包,它询问所需的网络配置以及网络启动的参数。标准DHCP服务器 (非PXE enabled) 将回复一个普通的DHCPOFFER包,其中包含网络信息 (如IP地址) ,但并不能提供PXE相关参数,因此PXE Client并不能启动。而PXE enabled的DHCP服务器所回复的DHCPOFFER包里则包含PXE相关信息。
  
在解析一个PXE enabled的DHCP服务器返回的DHCPOFFER包后,PXE client就能够设置自己的IP地址、IP Mask等等,并且指向网络上的启动资源,比如TFTP服务器上的vmlinuz文件和initrd文件。
  
然后PXE client就通过TFTP下载这些启动资源到自己的内存中；如果是UEFI Secure Boot (而不是Legacy的BIOS) 则还会检验一下这些启动资源。下载完成后就会用这些资源来启动了。
  
这些启动资源其实就是最小的操作系统 (比如WindowsPE,又比如一个basic Linux kernel+initrd) 。这个最小操作系统在装载了网络驱动和TCP/IP协议栈之后,就会开始boot或者install完整的操作系统了。而这个boot或install的过程,就不再通过TFTP来做,而是通过更加健壮的网络传输协议 (如HTTP、CIFS、iSCSI或NFS) 来做。而boot或者install所用到的实体,比如磁盘或者CD-ROM,是位于远端的,因此需要通过网络传输协议来做。

二、PXE启动过程和普通的Linux系统启动过程的对比:

1. 内核引导之前的不同:
  
    普通的从硬盘启动Linux系统最初是BIOS将MBR加载入内存,然后将控制权交给MBR中的bootloader程序 (如GRUB) ,bootloader程序经过几个stage的加载后,最后将vmlinuz加载入内存,开始内核引导；
  
    而PXE的启动过程在内核引导之前,是由BIOS中的PXE固件开启NBP程序 (比如DHCP的网络通信) ,然后下载vmlinuz和initrd,之后再进入内核启动过程。

2. 内核引导之后的不同:
  
    vmlinuz和initrd运行得差不多了之后,普通的硬盘Linux启动就从本地硬盘加载/sbin/init并运行为1号进程,以及启动系统服务等等,而PXE的启动在内核引导完成之后,仍然会通过网络的方式 (但不是TFTP协议,而是其他更加健壮的协议如NFS、iSCSI等) ,加载真正的完整操作系统,如/sbin/init应该就是位于网络远端的硬盘上。

以iSCSI为例,网络远端的硬盘以iSCSI协议挂载到了当前机器,就好像是本地磁盘一样。这就是PXE+iSCSI的启动方式了。

参考文献:
  
1. [https://en.wikipedia.org/wiki/Preboot_Execution_Environment](https://en.wikipedia.org/wiki/Preboot_Execution_Environment)

1. [http://blog.csdn.net/nirendao/article/details/75949536](http://blog.csdn.net/nirendao/article/details/75949536)

2.

        Diskless iSCSI boot with PXE HOWTO
