---
title: linux remote desktop server, xrdp
author: "-"
date: 2012-01-31T08:19:29+00:00
url: /?p=2199
categories:
  - Linux

tags:
  - reprint
---
## linux remote desktop server, xrdp

```bash
yay -S xrdp
yay -S xorgxrdp
vim ~/.xinitrc
# content
exec startxfce4

```

### remove

yay -R xorgxrdp-devel-git
yay -R xrdp
Install xrdp on CentOS 7 / RHEL 7
  
By Raj Last updated Mar 29, 2018

88

Share
  
xrdp is an Open Source Remote desktop Protocol server, which allows you to RDP to your Linux server from Windows machine; it is capable of accepting connections from rdesktop, freerdp, and remote desktop clients.

This post will help you to setup xrdp server on CentOS 7 / RHEL 7.

Prerequisites
  
1. First, install Gnome GUI on CentOS 7 / RHEL 7

1. xrdp is available in EPEL repository, so Install and configure EPEL repository.

rpm -Uvh <https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm>
  
Install xrdp on CentOS 7
  
Use YUM command to install xrdp package on CentOS 7 / RHEL 7.
  e: 1:xrdp-0.9.5-1.el7.x86_64
  
-> Running transaction check
  
-> Package xorgxrdp.x86_64 0:0.2.5-3.el7 will be installed
  
-> Finished Dependency Resolution

### install tigervnc

# Package Arch Version Repository Size

Installing:

tigervnc-server x86_64 1.8.0-2.el7_4 updates 213 k

xrdp x86_64 1:0.9.5-1.el7 epel 413 k
  
Installing for dependencies:

xorgxrdp x86_64 0.2.5-3.el7 epel 61 k

# Transaction Summary

Install 2 Packages (+1 Dependent package)

Total download size: 688 k
  
Installed size: 2.7 M
  
Downloading packages:
  
warning: /var/cache/yum/x86_64/7/epel/packages/xrdp-0.9.5-1.el7.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID 352c64e5: NOKEY
  
Public key for xrdp-0.9.5-1.el7.x86_64.rpm is not installed
  
(1/3): xrdp-0.9.5-1.el7.x86_64.rpm | 413 kB 00:00:01
  
(2/3): tigervnc-server-1.8.0-2.el7_4.x86_64.rpm | 213 kB 00:00:01

## (3/3): xorgxrdp-0.2.5-3.el7.x86_64.rpm | 61 kB 00:00:01

Total 409 kB/s | 688 kB 00:00:01
  
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
  
Importing GPG key 0x352C64E5:

Userid : "Fedora EPEL (7) [&#x65;&#x70;&#x65;&#x6c;&#x40;&#x66;&#x65;&#100;&#111;&#114;&#97;&#112;&#114;&#111;&#106;&#101;&#99;&#116;&#46;&#111;&#114;&#103;][1]"

Fingerprint: 91e9 7d7c 4a5e 96f1 7f3e 888f 6a2f aea2 352c 64e5

Package : epel-release-7-11.noarch (installed)

From : /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
  
Running transaction check
  
Running transaction test
  
Transaction test succeeded
  
Running transaction
  
Warning: RPMDB altered outside of yum.

Installing : xorgxrdp-0.2.5-3.el7.x86_64 1/3

Installing : 1:xrdp-0.9.5-1.el7.x86_64 2/3

Installing : tigervnc-server-1.8.0-2.el7_4.x86_64 3/3

Verifying : xorgxrdp-0.2.5-3.el7.x86_64 1/3

Verifying : tigervnc-server-1.8.0-2.el7_4.x86_64 2/3

Verifying : 1:xrdp-0.9.5-1.el7.x86_64 3/3

Installed:

tigervnc-server.x86_64 0:1.8.0-2.el7_4 xrdp.x86_64 1:0.9.5-1.el7

Dependency Installed:

xorgxrdp.x86_64 0:0.2.5-3.el7

Complete!
  
[&#47;&#101;&#x70;&#x65;&#108;&#64;f&#x65;&#x64;&#111;&#114;a&#x70;&#x72;&#111;&#106;&#x65;&#x63;&#116;&#46;&#111;&#x72;&#x67;][2]
  
Once xrdp is installed, start the xrdp service using the following command.

systemctl start xrdp
  
xrdp should now be listening on 3389. You can confirm this by using netstat command.

netstat -antup | grep xrdp
  
Output:

tcp 0 0 0.0.0.0:3389 0.0.0.0:* LISTEN 1508/xrdp
  
tcp 0 0 127.0.0.1:3350 0.0.0.0:* LISTEN 1507/xrdp-sesman
  
READ: netstat command not found on CentOS 7 / RHEL 7 – Quick Fix

By default, xrdp service won't start automatically after a system reboot. Run the following command in the terminal to enable the service at system startup.

systemctl enable xrdp
  
Firewall
  
Configure the firewall to allow RDP connection from external machines. The following command will add the exception for RDP port (3389).

firewall-cmd -permanent -add-port=3389/tcp
  
firewall-cmd -reload
  
SELinux
  
Configure SELinux

chcon -type=bin_t /usr/sbin/xrdp
  
chcon -type=bin_t /usr/sbin/xrdp-sesman
  
Test xrdp Remote Connectivity
  
Now take RDP from any windows machine using Remote Desktop Connection. Enter the ip address of Linux server in the computer field and then click on connect.

Install xrdp on CentOS 7 - Enter IP Address in Remote Desktop Connecton Window
  
Install xrdp on CentOS 7 – Enter IP Address in Remote Desktop Connection Window
  
You may need to ignore the warning of RDP certificate name mismatch.

Install xrdp on CentOS 7 - Accept the Certificate
  
Install xrdp on CentOS 7 – Accept the Certificate
  
You would be asked to enter the username and password. You can either use root or any user that you have it on the system. Make sure you use module "Xvnc".

Install xrdp on CentOS 7 - xrdp Login Page
  
Install xrdp on CentOS 7 – xrdp Login Page
  
If you click ok, you will see the processing. In less than a half minute, you will get a desktop.

Install xrdp on CentOS 7 - xrdp CentOS Desktop
  
Install xrdp on CentOS 7 – xrdp CentOS Desktop
  
That's All. You have successfully configured xRDP on CentOS 7 / RHEL 7.

来源: Linux社区 作者: Finans

一般情况下我们用ssh客户端远程登陆Linux系统，至于图形界面下的linux远程登陆工具，我们一般都会想到vnc，但它的安全性不够，在这里，我将介绍XRDP的安装配置方法。

xrdp安装配置方法

1. 如果是debian系发行版，可以设置好源后直接apt-get install xrdp
  
如果是RedHat系发行版，可以到这里下载安装包
  
xrdp依赖于pam和openssl-del，编译前需要先安装pam-devel和openssl-devel这两个包 (不同发行版的包名称有一点不同)
  
如果是RedHat系，设置好源直接yum install pam-devel openssl-devel

2. 下载好xrdp的安装包后，用tar -xvvzf 解压
  
进入解压出来的目录用root帐号执行make ，然后执行make install

3. xrdp需要vncserver，所以还要安装vncserver

4. 准备好后，可以通过解压出来的目录下的instfiles目录下的xrdp-control.sh脚本启动xrdp
  
xrdp-control.sh start
  
可以把此脚本添加到/etc/rc.d/init.d/中，让它开机自动运行。

5. 启动好xrdp，就可以通过客户端的rdp client 连接到服务器上，win下可以用mstsc，linux下可以用rdesktop或者krdp。
  
module 选择为: sesman-Xvnc

6. xrdp的配置文档在/etc/xrdp目录下的xrdp.ini和sesman.ini

xrdp.ini 关键部分在globals

[globals]
  
bitmap_cache=yes 位图缓存
  
bitmap_compression=yes 位图压缩
  
port=3389 监听端口
  
crypt_level=low 加密程度 (low为40位，high为128位，medium为双40位)
  
channel_code=1 不知道是什么

sesman.ini

[Globals]
  
ListenAddress=127.0.0.1 监听ip地址(默认即可)
  
ListenPort=3350 监听端口(默认即可)
  
EnableUserWindowManager=1 1为开启,可让用户自定义自己的启动脚本
  
UserWindowManager=startwm.sh
  
DefaultWindowManager=startwm.sh

[Security]
  
AllowRootLogin=1 允许root登陆
  
MaxLoginRetry=4 最大重试次数
  
TerminalServerUsers=tSUSErs 允许连接的用户组(如果不存在则默认全部用户允许连接)
  
TerminalServerAdmins=tsadmins 允许连接的超级用户(如果不存在则默认全部用户允许连接)

[Sessions]
  
MaxSessions=10 最大会话数
  
KillDisconnected=0 是否立即关闭断开的连接(如果为1,则断开连接后会自动注销)
  
IdleTimeLimit=0 空闲会话时间限制(0为没有限制)
  
DisconnectedTimeLimit=0 断开连接的存活时间(0为没有限制)

[Logging]
  
LogFile=./sesman.log 登陆日志文件
  
LogLevel=DEBUG 登陆日志记录等级(级别分别为,core,error,warn,info,debug)
  
EnableSyslog=0 是否开启日志
  
SyslogLevel=DEBUG 系统日志记录等级

装好后，我们就可以直接从win系统下利用mstsc直接进行登陆，相当方便，如果是linux，可以用rdesktop。

 [1]: &#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#x3a;&#x65;&#x70;&#x65;&#x6c;&#x40;&#x66;&#x65;&#100;&#111;&#114;&#97;&#112;&#114;&#111;&#106;&#101;&#99;&#116;&#46;&#111;&#114;&#103;
 [2]: &#x6d;&#x61;&#105;&#108;&#x74;&#x6f;&#58;&#47;&#101;&#x70;&#x65;&#108;&#64;f&#x65;&#x64;&#111;&#114;a&#x70;&#x72;&#111;&#106;&#x65;&#x63;&#116;&#46;&#111;&#x72;&#x67;
