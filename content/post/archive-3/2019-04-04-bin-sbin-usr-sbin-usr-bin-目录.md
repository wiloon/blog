---
title: /bin,/sbin,/usr/sbin,/usr/bin 目录
author: "-"
type: post
date: 2019-04-04T08:45:08+00:00
url: /?p=14090
categories:
  - Uncategorized

---
https://blog.csdn.net/kkdelta/article/details/7708250

/bin,/sbin,/usr/sbin,/usr/bin 目录
       
这些目录都是存放命令的，首先区别下/sbin和/bin：

    从命令功能来看，/sbin 下的命令属于基本的系统命令，如shutdown，reboot，用于启动系统，修复系统，/bin下存放一些普通的基本命令，如ls,chmod等，这些命令在Linux系统里的配置文件脚本里经常用到。
    
    从用户权限的角度看，/sbin目录下的命令通常只有管理员才可以运行，/bin下的命令管理员和一般的用户都可以使用。
    
    从可运行时间角度看，/sbin,/bin能够在挂载其他文件系统前就可以使用。
    

而/usr/bin,/usr/sbin与/sbin /bin目录的区别在于：

    /bin,/sbin目录是在系统启动后挂载到根文件系统中的，所以/sbin,/bin目录必须和根文件系统在同一分区；
    
    /usr/bin,usr/sbin可以和根文件系统不在一个分区。
    
    /usr/sbin存放的一些非必须的系统命令；/usr/bin存放一些用户命令，如led(控制LED灯的)。
    
    转下一位网友的解读，个人认为诠释得很到位：
    
    /bin是系统的一些指令。bin为binary的简写主要放置一些系统的必备执行档例如:cat、cp、chmod df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar等。
    /sbin一般是指超级用户指令。主要放置一些系统管理的必备程式例如:cfdisk、dhcpcd、dump、e2fsck、fdisk、halt、ifconfig、ifup、 ifdown、init、insmod、lilo、lsmod、mke2fs、modprobe、quotacheck、reboot、rmmod、 runlevel、shutdown等。
    /usr/bin　是你在后期安装的一些软件的运行脚本。主要放置一些应用软体工具的必备执行档例如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome*、 gzip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、 newaliases、nslookup passwd、quota、smb*、wget等。
    
    /usr/sbin   放置一些用户安装的系统管理的必备程式例如:dhcpd、httpd、imap、in.*d、inetd、lpd、named、netconfig、nmbd、samba、sendmail、squid、swap、tcpd、tcpdump等。
    如果新装的系统，运行一些很正常的诸如：shutdown，fdisk的命令时，悍然提示：bash:command not found。那么
    首先就要考虑root 的$PATH里是否已经包含了这些环境变量。
    可以查看PATH，如果是：PATH=$PATH:$HOME/bin则需要添加成如下：
    PATH=$PATH:$HOME/bin:/sbin:/usr/bin:/usr/sbin