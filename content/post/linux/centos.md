---
title: centos basic
author: "-"
date: 2012-01-25T01:22:34+00:00
url: centos
categories:
  - Linux
tags:
  - reprint
---
## centos basic

centos 7 minimal 安装之后 磁盘占用 1.4G

- yum repo

    curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo

## dhcp

    vim /etc/sysconfig/network-scripts/ifcfg-eth0

    bootproto=dhcp
    onboot=yes

## Linux centos livecd bin netinstall 各版本的区别
CentOS-5.5-x86_64-LiveCD.iso 光盘系统
  
CentOS-5.5-x86_64-bin-DVD 64位安装盘
  
CentOS-5.5-x86_64-netinstall 64位网络安装盘

LiveCD一般用来修复系统使用，有容量很小，不用安装，可以自启动等特性，可以直接使用光盘启动的系统。 bin DVD也具有同样的功能，但是体积较大，需要安装到硬盘使用。 netinstall和bin都可以用来安装系统，不同的是，netinstall根据你选择的软件列表从网上下载，然后进行系统安装； bin DVD本身包含了软件，不需要依赖于网络经行安装。

## centos, rpm

### centos, rpm 查看软件的版本号

rpm -qa | grep mysql

### RHEL/CentOS/Fedora 源 EPEL、Remi、RPMForge、RPMFusion

#### centos7, aliyun mirror

    curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo

<http://www.cnblogs.com/mawanglin2008/p/3532247.html>

RHEL/CentOS/Fedora各种源(EPEL、Remi、RPMForge、RPMFusion)配置

CentOS默认自带CentOS-Base.repo源,但官方源中去除了很多有版权争议的软件,而且安装的软件也不是最新的稳定版。Fedora自带的源中也找不到很多多媒体软件,如果需要安装,必需先添加其他源,如RPMFusion和RPMForge等第三方软件库。

下面GoFace来一一介绍各种第三方软件库,以下软件库适用于与RHEL完全兼容的linux发行版,如CentOS,Fedora,Scientific Linux。Scientific Linux大家可能有点陌生,它与CentOS类似,是RedHat Linux的克隆版,GoFace之前有过介绍: <http://blog.51osos.com/linux/scientific-linux/>

### EPEL源

EPEL, 即Extra Packages for Enterprise Linux,是由 Fedora 社区创建维护,为 RHEL 及衍生发行版如 CentOS、Scientific Linux 等提供高质量软件包的项目。EPEL中含有大量的软件,对官方标准源是一个很好的补充。

"EPEL (Extra Packages for Enterprise Linux ) is a Fedora Special Interest Group that creates, maintains, and manages a high quality set of additional packages for Enterprise Linux, including, but not limited to, Red Hat Enterprise Linux (RHEL), CentOS and Scientific Linux (SL)."

wiki:<http://fedoraproject.org/wiki/EPEL>

Fedora EPEL 下载: <http://mirrors.fedoraproject.org/publiclist/EPEL/>

EPEL 下载地址: <http://download.fedora.redhat.com/pub/epel/>

请针对不同的版本下载相应的包。

例如CentOS6.5添加阿里云的EPEL源

yum localinstall -nogpgcheck <http://mirrors.aliyun.com/epel/6/x86_64/epel-release-6-8.noarch.rpm>
  
CentOS 7.0添加阿里云的EPEL源

yum localinstall -nogpgcheck <http://mirrors.aliyun.com/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm>
  
### Remi源
  
Remi源大家或许很少听说,不过Remi源GoFace强烈推荐,尤其对于不想编译最新版的linux使用者,因为Remi源中的软件几乎都是最新稳定版。或许您会怀疑稳定不？放心吧,这些都是Linux骨灰级的玩家编译好放进源里的,他们对于系统环境和软件编译参数的熟悉程度毋庸置疑。

Remi下载地址: <http://rpms.famillecollet.com/>

您也需要针对不同的版本号下载。

例如CentOS 6.5添加官方的Remi源

yum localinstall -nogpgcheck <http://rpms.famillecollet.com/enterprise/remi-release-6.rpm>
  
例如CentOS 7添加官方的Remi源

yum localinstall -nogpgcheck <http://rpms.famillecollet.com/enterprise/remi-release-7.rpm>
  
RPMForge源

RPMForge是CentOS系统下的软件仓库,拥有4000多种的软件包,被CentOS社区认为是最安全也是最稳定的一个软件仓库。

RPMForge官方网站: <http://repoforge.org/>

RPMForge下载地址:

32位: <http://apt.sw.be/redhat/el6/en/i386/rpmforge/RPMS/>

64位: <http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/>

例如CentOS6.5添加官方的RPMForge源

yum localinstall -nogpgcheck <http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm>
  
CentOS 7.0添加官方的RPMForge源

yum localinstall -nogpgcheck <http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm>
  
RPMFusion源

如果您现在正在使用Fedora 15,对RPMFusion一定不陌生吧,各种音频软件如MPlayer在标准源中是没有的,一般先安装RPMFusion源,之后就可以放便地yum install各种需要的软件啦。

CentOS官方说RPMFusion软件库里面的软件稳定性不如rpmforge。

RPMFusion官网: <http://rpmfusion.org/>

例如CentOS6.5添加阿里云的RPMFusion源

yum localinstall -nogpgcheck <http://mirrors.aliyun.com/rpmfusion/free/el/updates/6/x86_64/rpmfusion-free-release-6-1.noarch.rpm>
  
yum localinstall -nogpgcheck <http://mirrors.aliyun.com/rpmfusion/nonfree/el/updates/6/x86_64/rpmfusion-nonfree-release-6-1.noarch.rpm>
  
或者添加CentOS6.5官方的RPMFusion源

yum localinstall -nogpgcheck <http://download1.rpmfusion.org/free/el/updates/6/i386/rpmfusion-free-release-6-1.noarch.rpm>
  
yum localinstall -nogpgcheck <http://download1.rpmfusion.org/nonfree/el/updates/6/i386/rpmfusion-nonfree-release-6-1.noarch.rpm>
  
注意: 在安装RPMFusion源之前需要先安装 epel-release

yum localinstall <http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm>
  
其他版本请详见: <http://rpmfusion.org/Configuration>

如何使用各种源
  
以上源对CentOS等系统完全兼容,但各软件库之间并不能保证完全兼容没有冲突。如果您需要使用以上源,您需要安装yum-priorities插件。安装yum-priorities插件后,您可以给各个源设置优先级priority。一般设置官方标准源优先级为1,最高,第三方推荐>10

priority=N  (N为1到99的正整数,数值越小越优先)

[base], [addons], [updates], [extras] … priority=1
  
[CentOSplus],[contrib] … priority=2
  
其他第三的软件源为: priority=N  (推荐N>10)

# vi CentOS-Base.repo

[base]

name=CentOS-$releasever - Base

mirrorlist=<http://mirrorlist.centos.org/?release>=$releasever&arch=$basearch&repo=os

# baseurl=<http://mirror.centos.org/centos/>$releasever/os/$basearch/

gpgcheck=1

gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6

priority=1

# released updates

……

# wget <http://download.fedora.redhat.com/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm>

# wget <http://rpms.famillecollet.com/enterprise/remi-release-6.rpm>

[root@orcl1 yum.repos.d]# ls

CentOS-Base.repo CentOS-Media.repo epel-testing.repo

CentOS-Debuginfo.repo epel.repo remi.repo
  
vi remi.repo 将[remi] 中的 enabled=0 改成 enabled=1 来启用 remi 源

[root@orcl1 yum.repos.d]# rpm –import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

[root@orcl1 yum.repos.d]# rpm –import /etc/pki/rpm-gpg/RPM-GPG-KEY-remi
  
在remi.repo中和epel.repo中添加priority设置即可使用。
