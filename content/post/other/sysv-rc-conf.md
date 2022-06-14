---
title: sysv-rc-conf
author: "-"
date: 2012-05-26T01:22:58+00:00
url: /?p=3225
categories:
  - Linux
tags:
  - reprint
---
## sysv-rc-conf

      sysv-rc-conf是一个强大的服务管理程序，群众的意见是sysv-rc-conf比chkconfig好用。
  


  
    Ubuntu运行级别
  
  
    Linux 系统任何时候都运行在一个指定的运行级上，并且不同的运行级的程序和服务都不同，所要完成的工作和要达到的目的都不同，系统可以在这些运行级之间进行切换，以完成不同的工作。
  
  
    Ubuntu 的系统运行级别: 
  
  
    0 系统停机状态
  
  
  
    1 单用户或系统维护状态
  
  
  
    2~5 多用户状态
  
  
  
    6 重新启动
  
  
    查看当前运行级别,执行命令: 
  
  
    runlevel
  
  
  
     ( runlevel 显示上次的运行级别和当前的运行级别，"N"表示没有上次的运行级别。) 
  
  
    切换运行级别，执行命令: 
  
  
    init [0123456Ss]
  
  
  
     ( 即在 init 命令后跟一个参数，此参数是要切换到的运行级的运行级代号，如: 用 init 0 命令关机；用 init 6 命令重新启动。) 
  
  
  
  
    三、Linux 系统主要启动步骤:
  
  
    1. 读取 MBR 的信息,启动 Boot Manager
  
  
    Windows 使用 NTLDR 作为 Boot Manager,如果您的系统中安装多个
  
  
  
    版本的 Windows,您就需要在 NTLDR 中选择您要进入的系统。
  
  
  
    Linux 通常使用功能强大,配置灵活的 GRUB 作为 Boot Manager。
  
  
    2. 加载系统内核,启动 init 进程
  
  
    init 进程是 Linux 的根进程,所有的系统进程都是它的子进程。
  
  
    3. 进程读取
  
  
    init 进程读取 /etc/inittab 文件中的信息,并进入预设的运行级别,
  
  
  
    按顺序运行该运行级别对应文件夹下的脚本。脚本通常以 start 参数启
  
  
  
    动,并指向一个系统中的程序。
  
  
  
    通常情况下, /etc/rcS.d/ 目录下的启动脚本首先被执行,然后是
  
  
  
    /etc/rcN.d/ 目录。例如您设定的运行级别为 3,那么它对应的启动
  
  
  
    目录为 /etc/rc3.d/ 。
  
  
    4. 根据对应脚本启动服务器
  
  
    根据 /etc/rcS.d/ 文件夹中对应的脚本启动 Xwindow 服务器 xorg
  
  
  
    Xwindow 为 Linux 下的图形用户界面系统。
  
  
    5. 启动登录管理器,等待用户登录
  
  
    Ubuntu 系统默认使用 GDM 作为登录管理器,您在登录管理器界面中
  
  
  
    输入用户名和密码后,便可以登录系统。(您可以在 /etc/rc3.d/
  
  
  
    文件夹中找到一个名为 S13gdm 的链接)
  
  
  
  
    四、安装sysv-rc-conf
  
  
    sudo apt-get install sysv-rc-conf
  
  
  
  
    五、使用sysv-rc-conf
  
  
    sudo sysv-rc-conf
  
  
  
    操作界面十分简洁，你可以用鼠标点击，也可以用键盘方向键定位，用空格键选择，用Ctrl+N翻下一页，用Ctrl+P翻上一页，用Q退出。其中，"X"表示开启该服务。
  
  
  
  
    六 、部分服务优化推荐及介绍
  
  
    acpi-support 这个是关于电源支持的默认是1,2,3,4,5下启动，我认为你可以把它调整到s级别。
  
  
  
    acpid acpi的守护程序，默认是2－5开启，我认为可以不用管。
  
  
  
    alsa alsa声音子系统，应该不用开启它。
  
  
  
    alsa-utils 这个服务似乎取代了alsa，所以开启这个就可以了，我在S级别开启它。
  
  
  
    anacron 这是一个用于执行到时间没有执行的程序的服务，我认为它无所谓，所以关了它，这个可以随便。
  
  
  
    apmd 也是一种电源管理，我认为电脑如果不是很老，它就没有开启的必要了。
  
  
  
    atd 和anacron类似，我把它关了。
  
  
  
    bluez-utiles 传说中的蓝牙服务，然后遗憾我没有，所以关了。
  
  
  
    bootlogd 似乎使用来写log的，安全期间开着他也许比较好。
  
  
  
    cron 指定时间运行程序的服务，所以开着比较好的。
  
  
  
    cupsys 打印机服务，所以如果你有，就开启吧。
  
  
  
    dbus 消息总线系统，非常重要，一定要开。
  
  
  
    dns-clean 拨号连接用的，如果不用，就关了它。
  
  
  
    evms 企业卷管理系统，由于我并不明白什么叫做企业卷，所以我关了它。
  
  
  
    fetchmail 用于邮件守护，我关了它。
  
  
  
    gdm gnome桌面管理器，我关了它，然后用startx启动gnome。
  
  
  
    halt 关机用的，不要更改
  
  
  
    hdparm 这个我刚才有讲，如果没有ide硬盘也就不用开启它了。
  
  
  
    hotkey-setup 这个是给某些品牌笔记本设计的热键映射，台式机用户请关了它
  
  
  
    hotplug 这个是用于热插拔的，我已经测试过了，在某些电脑上关闭它会使声卡无效，请在S级别开启它。
  
  
  
    hplip hp打印机专用的，应该可以关了它。
  
  
  
    ifrename 网络接口重命名，好像没用，关了。
  
  
  
    ifupdown 这个使用来打开网络的，开着它。
  
  
  
    ifupdown-clean 同上。
  
  
  
    klogd linux守护程序，接受来自内核和发送信息到syslogd的记录，并记录为一个文件，所以请开着它。
  
  
  
    linux-restricted-modules-common 这个使用来使用受限制的模块的，你可以从/lib/linux-restricted-modules下查看，如果没有什么，你可以关掉它。
  
  
  
    lvm 逻辑卷管理器，如果你没有请关了它。
  
  
  
    makedev 用来创建设备到/dev/请不要动他。
  
  
  
    mdamd 管理raid用，如果你没有请关闭它。
  
  
  
    module-init-tools 从/etc/modules 加在扩展模块的，这个一般开着。
  
  
  
    networking 增加网络接口和配置dns用，将它开启。
  
  
  
    ntp-server 与ubuntu时间服务器进行同步的，关了。
  
  
  
    pcmcia 激活pcmica设备，遗憾我有生以来都没有见过这样的设备，关了它。
  
  
  
    powernowd 用于管理cpu的客户端程序，如果有变频功能，比如amd的quite' cool 那么就开启它吧。
  
  
  
    ppp 拨号用的，我关了它。
  
  
  
    ppp-dns 一样，也关了。
  
  
  
    readahead 预加载服务，让我想起了win的预读，当然他们不同，它会使启动变慢3－4妙，所以我关了它。
  
  
  
    reboot 重启用的，不要动。
  
  
  
    rmnologin 如果发现nologin，就去除它，在笔记本上不用开启。
  
  
  
    rsync rsync协议守护，请视情况而定。
  
  
  
    screen-cleanup 一个清除开机屏幕的脚本，随便。
  
  
  
    sendsigs 重启和关机时向所有进程发送消息。所以不要管它。
  
  
  
    single 激活但用户模式，不用管它。
  
  
  
    stop-bootlogd 从2,3,4,5级别停止bootlogd,不用管它。
  
  
  
    sudo 这个不用说吧，不用管它。
  
  
  
    sysklogd 用于记录系统日志信息，不用管它。
  
  
  
    udev 用户空间dev文件系统，不用管它。
  
  
  
    udev-mab 同上。
  
  
  
    umountfs 用来卸载文件卷的，不用管它。
  
  
  
    urandom 生成随即数的，不知道怎么用，不用管它。
  
  
  
    usplash 那个漂亮的启动画面，但是我关了它，它也存在，所以想关他需要把内核起动参数中的splash一句删掉。
  
  
  
    vbesave 显卡bios配置工具，不用管它。
  
  xorg-common 设置x服务ice socket。不用管它。

  <http://baike.baidu.com/view/2521377.htm?fromTaglist>
