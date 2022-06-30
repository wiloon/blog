---
title: Hostname, 主机名
author: "-"
date: 2011-11-26T01:18:08+00:00
url: hostname
categories:
  - Linux
tags:
  - reprint
---
## Hostname

### hostnamectl, 查看主机信息, 查看主机名, 查看机器名, 查 hostname

```bash
hostnamectl

# 设置主机名
sudo hostnamectl set-hostname rhel7

hostnamectl
  
hostnamectl status
  
hostnamectl -static
  
hostnamectl -transient
  
hostnamectl -pretty
  
sudo hostnamectl set-hostname new-host-name
```

## redhat 改主机名

/etc/sysconfig/network

NETWORKING=yes
NETWORKING_IPV6=no
HOSTNAME=YOURHOSTNAME

/etc/hosts

127.0.0.1               YOURHOSTNAME           localhost

```bash
# 在linux下查看主机名的命令
hostname
```

<http://soft.zdnet.com.cn/software_zone/2007/0831/481970.shtml>
  
1. 什么是主机名:

无论在局域网还是INTERNET上，每台主机都有一个IP地址，是为了区分此台主机和彼台主机，也就是说IP地址就是主机的门牌号。但IP地址不方便记忆，所以又有了域名。域名只是在公网 (INtERNET)中存在(以实验为目的的局域网域网实验性除外) ，每个域名都对应一个IP地址，但一个IP地址可有对应多个域名。域名类型 Linuxsir.org 这样的；

主机名是用于什么的呢？在一个局域网中，每台机器都有一个主机名，用于主机与主机之间的便于区分，就可以为每台机器设置主机名，以便于以容易记忆的方法来相互访问。比如我们在局域网中可以为根据每台机器的功用来为其命名。

主机名相关的配置文件: /etc/hosts;

主机名配置文件；
  
主机名的配置文件大多是/etc/hosts ；

hosts – The static table lookup for host name (主机名查询静态表) ；

由于 Linux 发行版本众多，与主机名相关的配置文件有时也有所不同。现在我们说说常见版本的主机名配置文件；

2.1 主机名配置文件 /etc/hosts解说；

Fedora/Redhat 或以Fedora/Redhat为基础打包的发行版，主机名配置文件是 /etc/hosts

Debian或以Debian为基础打包的发行版，主机名配置文件是 /etc/Hostname 和/etc/hosts

Slackware的主机名配置文件是 /etc/hosts

那我们来读读 /etc/hosts的内容，看这个文件是用来做什么的。hosts 配置文件是用来把主机名字映射到IP地址的方法，这种方法比较简单。但这种映射只是本地机的映射，也就是说每台机器都是独立的，所有的计算机都不能相互通过Hostname来访问。

注: 在debian 中还有一个/etc/Hostname的文件，这个文件就是直接把本地主机名写进去就行了，但要和 /etc/hosts中的本地主机名保持一致。

/etc/hosts 的内容一般有如下类似内容:

127.0.0.1 localhost.localdomain localhost

192.168.1.195 debian.localdomain debian

注:

一般情况下hosts的内容关于主机名(Hostname)的定义，每行为一个主机，每行由三部份组成，每个部份由空格隔开。其中#号开头的行做说明，不被系统解释。

第一部份: 网络IP地址；

第二部份: 主机名.域名，注意主机名和域名之间有个半角的点，比如 localhost.localdomain

第二部份: 主机名(主机名别名)  ，其实就是主机名；

当然每行也可以是两部份，就是主机IP地址和主机名；比如 192.168.1.195 debian

127.0.0.1 是回环地址，比如我们不想让局域网的其它机器看到我们测试的网络程序，就可以用回环地址来测试。

为什么需要定义域名呢？其实理解也简单，比如我们有三台主机，每台做不同的事，一台做MAIL服务器，一台做FTP服务器，一台做SMB服务器，所以我们就可以这样来设计Hostname；

127.0.0.1 localhost.localdomain localhost

192.168.1.2 ftp.localdomain ftp

192.168.1.3 mail.localdomain mail

192.168.1.4 smb.localdomin smb

把这上面这个配置文件的内容分别写入每台机器的/etc/hosts内容中，这样这三台局域网的机器就可以通过Hostname来访问了。

2.2 主机名(Hostname)和域名(Domain) 的区别；

主机名就机器本身的名字，域名是用来解析到IP的。但值得一说的是在局域网中，主机名也是可以解析到IP上的；比如我们前面所说举的例子；

2.3 局域网的机器，不能通过主机名互访的原因；

有的弟兄可能会说，我的Hostname彼此不能互访，其实这也问题也简单，我们前面已经提到了一个简单的解决办法。就是要让局域网中的所有主机都有一个通用的，并且包含所有主机的/etc/hosts文件；

另一个是做解决办法是做局域网DNS服务器，如果您的主机特别少，就用前面所说的简单方法就行；如何做DNS服务器，我将在以后的文档中专题介绍；不过我值得一提的是做任何服务器都是以效率优先的原则为基础。比如我们在局域网中两台机器，我们还有必要做DNS服务器吗？无论怎么解决，最终的都是用最有效率的办法解决问题；我们不能说明DNS多高级。如果DNS是为外网服务的，那就另说了，不做也得做。对不对？

1. 主机名修改工具 Hostname;

其实主机名的修改也有专用工具，就是Hostname ；我认为如果用这个工具来修改主机名，不如直接修改 /etc/hosts 来的方便；您可以查看 hosname –help或 man Hostname的帮助 。在这里我们只说简单的用法；

Hostname 工具是用来显示和设置系统主机名，看下面的洋文；

Hostname – show or set the system's host name

举例解说:

＊ 显示主机名:

[root@Linuxsir01 ~]# Hostname

Linuxsir01

此主机的主机名是Linuxsir01，不加参数是用来显示当前操作的主机的主机名；

＊ 临时设置主机名:

我们可以用 Hostname 后接主机名，这样就可以设置当前操作的主机的主机名，比如我们想把主机名设置为Linuxsir02；

[root@Linuxsir01 ~]# Hostname Linuxsir02

[root@Linuxsir01 ~]# Hostname 注: 显示主机名

Linuxsir02

通过Hostname 工具来设置主机名只是临时的，下次重启系统时，此主机名将不会存在；所以您想修改主机名，想一直有效的，还是用前面所说修改主机名配置文件 /etc/hosts；

＊ 显示主机IP:

显示当前主机名的IP，可以用-i参数；

[root@Linuxsir01 ~]# Hostname -i

192.168.1.3

本文未尽事宜
有时我们在登入桌面时，会提示找不到Hostname ，这时您要做的是修改/etc/hosts，为您的机器添加一个主机名；先用 ifconfig -a 来查看主机的IP地址，然后把你主机的IP地址，指定主机名。

hosts文件是Linux系统中一个负责IP地址与域名快速解析的文件，以ASCII格式保存在"/etc"目录下，文件名为"hosts" (不同的linux版本，这个配置文件也可能不同。比如Debian的对应文件是/etc/hostname) 。hosts文件包含了IP地址和主机名之间的映射，还包括主机名的别名。在没有域名服务器的情况下，系统上的所有网络程序都通过查询该文件来解析对应于某个主机名的IP地址，否则就需要使用DNS服务程序来解决。通常可以将常用的域名和IP地址映射加入到hosts文件中，实现快速方便的访问。

1. 配置文件
这个文件可以配置主机ip及对应的主机名，对于服务器类型的linux系统其作用还是不可忽略的。在局域网或是INTERNET上，每台主机都有一个IP地址，它区分开每台主机，并可以根据ip进行通讯。但IP地址不方便记忆，所以又有了域名。在一个局域网中，每台机器都有一个主机名，用于区分主机，便于相互访问。

Linux主机名的相关配置文件就是/etc/hosts;这个文件告诉本主机哪些域名对应那些ip，那些主机名对应哪些ip:

比如文件中有这样的定义

192.168.1.100 linumu100 test100
  
假设192.168.1.100是一台网站服务器，在网页中输入<http://linumu100或http://test100就会打开192.168.1.100>的网页。

通常情况下这个文件首先记录了本机的ip和主机名:

127.0.0.1 localhost.localdomain localhost
  
配置文件格式说明
一般/etc/hosts 的内容一般有如下类似内容:

127.0.0.1 localhost.localdomain localhost192.168.1.100 linmu100.com linmu100192.168.1.120 ftpserver ftp120
  
一般情况下hosts文件的每行为一个主机，每行由三部份组成，每个部份由空格隔开。其中#号开头的行做说明，不被系统解释。

hosts文件的格式如下:

IP地址 主机名/域名
  
第一部份: 网络IP地址；

第二部份: 主机名或域名；

第三部份: 主机名别名；

当然每行也可以是两部份，即主机IP地址和主机名；比如 192.168.1.100 linmu100。

这里可以稍微解释一下主机名(hostname)和域名(Domain) 的区别: 主机名通常在局域网内使用，通过hosts文件，主机名就被解析到对应ip；域名通常在internet上使用，但如果本机不想使用internet上的域名解析，这时就可以更改hosts文件，加入自己的域名解析。

1. /hosts文件可以帮助解决哪些问题

4.1 远程登录linux主机过慢问题

有时客户端想远程登录一台linux主机，但每次登录输入密码后都会等很长一段时间才会进入，这是因为linux主机在返回信息时需要解析ip，如果在linux主机的hosts文件事先加入客户端的ip地址，这时再从客户端远程登录linux就会变很快。

注: 这里所说的远程登录不仅仅是ssh，还可能是MySQL远程登录，或是文件共享的查询等。

4.2 双机互连

当两台主机只是双机互连时，这时两台主机都需要设置自己的ip，同时在对方的hosts文件里加入自己的ip和主机名。

主机名修改工具hostname;

其实主机名的修改也有专用工具，就是hostname

hostname – show or set the system's host name

显示主机名:

hostname

linmu100

此主机的主机名是linmu100，不加参数是用来显示当前主机的主机名；

临时设置主机名:

hostname test100

hostname 注: 显示主机名

test100

通过hostname 工具来设置主机名只是临时的，下次重启系统时，此主机名将不会存在；

显示主机IP:

hostname -i

192.168.1.100

Ubuntu 改主机名

1.启用root用户

运行命令 sudo passwd root 为root用户设置密码

2.以root用户身份登录

1) 编辑文件/etc/hosts

该文件每行由三部份组成，每个部份由空格隔开

第一部份: 网络IP地址；

第二部份: 主机名或域名；

第三部份: 主机名别名；

当然每行也可以是两部份，即主机IP地址和主机名；比如 192.168.1.100 linmu100。

将

127.0.1.1 xxxxx

替换为

127.0.1.1 newhostname
编辑 /etc/hostname文件 删除该文件的所有内容，添加newhostname

运行一下命令 hostname newhostname

3.退出root用户 改用一般用户登录即可

注:

其中 xxxxx为原来的主机名 newhostname为你想修改的主机名

RHEL

[root@yanyan ~]# vi /etc/sysconfig/network

NETWORKING=yes

HOSTNAME=hui 将这里的HOSTNAME该为新的主机名
  
保存后重启即可
  
这样做后只是修改了主机名
  
如果要解析ip还需要修改/etc/hosts文件
