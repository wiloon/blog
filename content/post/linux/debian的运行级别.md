---
title: Debian的运行级别
author: "-"
date: 2011-12-11T03:39:39+00:00
url: /?p=1843
categories:
  - Linux
tags:
  - reprint
---
## Debian的运行级别
转自: <http://dagai.net/archives/569>

最近在看王旭的《debian标准教程》，讲的真的是很广，但很浅，就运行级别这一小段，让老夫琢磨了好几天，也就明白debian的运行级别与redhat系的那些不一样，在centos中，runlevel 5就是图形界面，3是文本界面，而在debian中，runlevel 2-5都是多用户状态，这几个级别一样的，怎么设置这些服务的状态呢，centos有ntsysv和chkconfig啊，王旭在书中也就提到了rcconf这个命令，弄了半天弄得莫名其妙，到处搜啊搜的，终于发现，原来debian下还有个比chkconfig更好用的sysv-rc-conf。
  
先说说debian的系统运行级别

可以运行runlevel查看系统的运行级别，runlevel命令显示上次的运行级别和当前的运行级别，第一个为"N"的时候表示没有上次的运行级别。
  
0 系统停机状态
  
1 单用户或系统维护状态
  
2-5 多用户状态
  
6 重新启动
  
至于S和s是给单用户模式来用的。
  
可以用init 加数字来切换系统的运行级别，默认系统下2-5这几个运行级别状态是一样的，切换运行级别根本不会有什么变动。
  
这时候可以运行rcconf来关闭服务，这个rcconf居然还没有，用aptitude install rcconf安装它，这个rcconf与centos下的ntsysv差不多，这里取消或选取某个服务，将同时改变2-5级别的状态。
  
那老夫想把这个debian的运行级别改成跟centos差不多咋搞？这时候就要请上sysv-rc-conf了，sysv-rc-conf默认也没装，装上它，运行sysv-rc-conf，界面很简单，横着列出了所有的级别，纵向列出了所有的服务，不是有那么多中括号嘛，用方向键移到相应服务的相应级别，按空间选中或取消，这样，老夫就移到gdm上，234级别都取消掉，只保留5的，然后改一下inittab文件，把默认运行级别由2改为3，这样就跟centos一样3是文本界面5是图形界面了。
  
sysv-r-conf可以按ctrl+n和ctrl+p下翻和上翻，也可以按-来停止某个服务或按=/+来启动某个服务，设置完按q退出即可。
  
至于怎么把程序加入到服务，update-rc.d。

下面是一些常见的系统服务: 
  
acpi-support 高级电源管理支持
  
acpid acpi 守护程序.这两个用于电源管理,非常重要
  
alsa 声音子系统
  
alsa-utils
  
anacron cron 的子系统,将系统关闭期间的计划任务,在下一次系统运行时执行。
  
apmd acpi 的扩展
  
atd 类似于 cron 的任务调度系统。建议关闭
  
binfmt-support 核心支持其他二进制的文件格式。建议开启
  
bluez-utiles 蓝牙设备支持，关掉没啥
  
bootlogd 启动日志。开启它
  
cron 任务调度系统,建议开启
  
cupsys 打印机子系统。
  
dbus 消息总线系统(message bus system)。非常重要
  
dns-clean 使用拨号连接时,清除 dns 信息。
  
evms 企业卷管理系统(Enterprise Volumn Management system)
  
fetchmail 邮件用户代理守护进程,用于收取邮件
  
gdm gnome 登录和桌面管理器。
  
gdomap
  
gpm 终端中的鼠标支持。
  
halt 不要乱搞哦，这个只有0级别才需要，关闭系统的。
  
hdparm 调整硬盘的脚本,配置文件为 /etc/hdparm.conf。
  
hibernate 系统休眠
  
hotkey-setup 笔记本功能键支持。支持类型包括: HP, Acer, ASUS, Sony,Dell, 和 IBM。
  
hotplug and hotplug-net 即插即用支持,比较复杂,建议不要动它。
  
hplip HP 打印机和图形子系统
  
ifrename 网络接口重命名脚本。如果您有十块网卡,您应该开启它
  
inetd 在文件 /etc/inetd.conf 中,注释掉所有你不需要的服务。如果该文件不包含任何服务,那关闭它是很安全的。
  
klogd 重要。
  
linux-restricted-modules-common 受限模块支持。
  
/lib/linux-restricted-modules/ 文件夹中的模块为受限模块。例如某些驱动程序,如果您没有使用受限模块,就不需要开启它。
  
lvm 逻辑卷管理系统支持。
  
makedev 创建设备文件,非常重要。
  
mdamd 磁盘阵列
  
module-init-tools 从/etc/modules 加载扩展模块,建议开启。
  
networking 网络支持。按 /etc/network/interfaces 文件预设激活网络,非常重要。
  
ntpdate 时间同步服务,建议关闭。
  
pcmcia pcmcia 设备支持。
  
powernowd 移动 CPU 节能支持
  
ppp and ppp-dns 拨号连接
  
readahead 预加载库文件。
  
reboot 别动它。
  
resolvconf 自动配置 DNS
  
rmnologin 清除 nologin
  
rsync rsync 守护程序
  
sendsigs 在重启和关机期间发送信号
  
single 激活单用户模式
  
ssh ssh 守护程序。建议开启
  
stop-bootlogd 在 2,3,4,5 运行级别中停止 bootlogd 服务
  
sudo 检查 sudo 状态。重要
  
sysklogd 系统日志
  
udev & udev-mab 用户空间 dev 文件系统(userspace dev filesystem)。重要
  
umountfs 卸载文件系统
  
urandom 随机数生成器
  
usplash 开机画面支持
  
vbesave 显卡 BIOS 配置工具。保存显卡的状态
  
xorg-common 设置 X 服务 ICE socket。
  
adjtimex 调整核心时钟的工具
  
dirmngr 证书列表管理工具,和 gnupg 一起工作。
  
hwtools irqs 优化工具
  
libpam-devperm 系统崩溃之后,用于修理设备文件许可的守护程序。
  
lm-sensors 板载传感器支持
  
mdadm-raid 磁盘陈列管理器
  
screen-cleanup 清除开机屏幕的脚本
  
xinetd 管理其他守护进程的一个 inetd 超级守护程序