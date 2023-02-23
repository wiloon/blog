---
title: Linux /etc/init.d /etc/rc.local
author: "-"
date: 2015-05-02T23:46:21+00:00
url: /?p=7575
categories:
  - Inbox
tags:
  - Linux

---
## Linux /etc/init.d /etc/rc.local
<http://blog.csdn.net/acs713/article/details/7322082>

本文英语版本来自: <http://www.ghacks.net/2009/04/04/get-to-know-linux-the-etcinitd-directory/>

以下内容是作者自己的翻译版本，如需转载到CSDN外其他网站，请注明本文链接。

一、关于/etc/init.d

如果你使用过linux系统，那么你一定听说过init.d目录。这个目录到底是干嘛的呢？它归根结底只做了一件事情，但这件事情非同小可，是为整个系统做的，因此它非常重要。init.d目录包含许多系统各种服务的启动和停止脚本。它控制着所有从acpid到x11-common的各种事务。当然，init.d远远没有这么简单。 (译者注: acpid 是linux操作系统新型电源管理标准 ；X11也叫做X Window系统，X Window系统 (X11或X)是一种位图显示的 视窗系统 。它是在 Unix 和 类Unix 操作系统 ，以及 OpenVMS 上建立图形用户界面 的标准工具包和协议，并可用于几乎已有的现代操作系统) 。

当你查看/etc目录时，你会发现许多rc#.d 形式存在的目录 (这里#代表一个指定的初始化级别，范围是0~6) 。在这些目录之下，包含了许多对进程进行控制的脚本。这些脚本要么以"K"开头，要么以"S"开头。以K开头的脚本运行在以S开头的脚本之前。这些脚本放置的地方，将决定这些脚本什么时候开始运行。在这些目录之间，系统服务一起合作，就像运行状况良好的机器一样。然而，有时候你希望能在不使用kill 或killall 命令的情况下，能干净的启动或杀死一个进程。这就是/etc/init.d能够派上用场的地方了！

如果你在使用Fedora系统，你可以找到这个目录: /etc/rc.d/init.d。实际上无论init.d放在什么地方，它都发挥着相同的作用。

为了能够使用init.d目录下的脚本，你需要有root权限或sudo权限。每个脚本都将被作为一个命令运行，该命令的结构大致如下所示:

/etc/init.d/command 选项

comand是实际运行的命令，选项可以有如下几种:

start
  
stop
  
reload
  
restart
  
force-reload
  
大多数的情况下，你会使用start,stop,restart选项。例如，如果你想关闭网络，你可以使用如下形式的命令:

/etc/init.d/networking stop

又比如，你改变了网络设置，并且需要重启网络。你可以使用如下命令:

/etc/init.d/networking restart

init.d目录下常用初始化脚本有:

networking
  
samba
  
apache2
  
ftpd
  
sshd
  
dovecot
  
MySQL
  
当然，你可能有其他更多常用的脚本，这个取决于你安装了什么linux操作系统。

二、关于/etc/rc.local

rc.local也是我经常使用的一个脚本。该脚本是在系统初始化级别脚本运行之后再执行的，因此可以安全地在里面添加你想在系统启动之后执行的脚本。常见的情况是你可以再里面添加nfs挂载/mount脚本。此外，你也可以在里面添加一些调试用的脚本命令。例如，我就碰到过这种情况: samba服务总是无法正常运行，而检查发现，samba是在系统启动过程中就该启动执行的，也就是说，samba守护程序配置保证了这种功能本应该正确执行。碰到这种类似情况，一般我也懒得花大量时间去查为什么，我只需要简单的在/etc/rc.local脚本里加上这么一行:

/etc/init.d/samba start

这样就成功的解决了samba服务异常的问题。

三、总结

Linux是灵活的。正因为它的灵活性，我们总是可以找到许多不同的办法来解决同一个问题。启动系统服务的例子就是一个很好的佐证。有了/etc/init.d目录下的脚本，再加上/etc/rc.local这个利器，你可以放心的确保你的服务可以完美的启动和运行。
