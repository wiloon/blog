---
title: Termux
author: "-"
date: 2018-03-18T11:23:53+00:00
url: /?p=11999
categories:
  - Inbox
tags:
  - reprint
---
## Termux

[https://www.jianshu.com/p/5c8678cef499](https://www.jianshu.com/p/5c8678cef499)

神器Termux的使用日常

写在前面:
  
现代桌面操作系统都自带终端程序,其强大的功能性和图形化的易用性相辅相成,使得系统操作更加高效。特别是Linux系列衍生系统的终端,得益于系统自带的丰富的功能指令,熟悉之后更是如鱼得水。随着手持智能设备的普及和性能的不断提升,如今的手持终端,如手机、平板等的硬件标准已达到了初级桌面计算机的硬件标准,甚至有过之而无不及,如果能在这些设备上使用Linux下类似的终端程序无疑是对运维作业的一大补充。

Android作为现代智能设备操作系统,在市场占有率上有压倒性的优势,况其与Linux系统有着不言自明的亲缘关系,在Android上使用终端也算是返璞归真了。另外,低门槛、低成本、受众广的实践特性也是本文选择Android的主要原因。

  1. Termux 终端
  
    Android是一个单用户图形化系统,功能主要以应用的形式呈现给用户,因此在系统上我们无法直接获取终端,更是无法直接调用系统自带的丰富指令。使用ADB是一个曲线救国的方法,打开USB调试后开发者可以在桌面系统的终端中触发Android系统自带指令,使用方法大概如下: 

adb shell env # 查看Android的环境变量
  
这种方法需要一台电脑的配合,为了实现全天候、无差别的终端体验,你首先需要一个终端模拟器来保证随时随地地使用终端。Android平台我们推荐Termux终端模拟器。

Termux is an Android terminal emulator and Linux environment app that works directly with no rooting or setup required. A minimal base system is installed automatically - additional packages are available using the APT package manager.

> > Homepage
> > Termux on Google Play

Termux

Termux终端有很多优秀的特性,这里要说两点:

Termux有针对手机输入优化的键盘显示,长按KEYBOARD选项可打开该功能
  
Termux维护着适合Android的库,并自带包管理器apt
  
因此,在Android上使用Termux终端和在Linux上使用终端一样方便。
  
安装完Termux后你有以下几个步骤需要完成:

到手机设置中开启 Termux 的存储权限,否则在Termux终端无法访问内部存储
  
修改Termux的源地址  (特别是国内用户)
  
和Linux类似,Termux有自己的软件源,安装Termux后默认的软件源是Termux官网,即 [http://termux.net](http://termux.net),可打开源列表查看。

### 如何查看

export EDITOR=vi
  
apt edit-sources
  
源列表的一般格式为:

The main termux repository

deb [arch=all,你的平台架构] [http://termux.net](http://termux.net) stable main
  
上面的指令中我们指定 vi 作为默认文本编辑器,vi指令是Termux自带的,你也可以指定其他文本编辑器,但需要先安装。默认的源服务器在国内是无法访问的,除非使用梯子,也就是说刚开始你可能只能使用vi编辑器,而且不能安装任何软件,毕竟 apt updage && apt upgrade都不能成功执行,换言之没有梯子默认情况下你无法获取资源列表。
  
国内用户建议使用清华维护的源服务器: [http://mirrors.tuna.tsinghua.edu.cn/termux](http://mirrors.tuna.tsinghua.edu.cn/termux)

## 国内用户建议使用的源列表内容

The main termux repository

deb [arch=all,你的平台架构] [http://termux.net](http://termux.net) stable main

deb [arch=all,你的平台架构] [http://mirrors.tuna.tsinghua.edu.cn/termux](http://mirrors.tuna.tsinghua.edu.cn/termux) stable main
  
默认情况下内容是使用http协议传输的,我们可以为apt添加安全传输支持,这样就可以使用https安全传输协议。

apt install apt-transport-https
  
这时再次修改源服务器的传输协议为https并更新即可。
  
安装Termux后我们不仅可以在手机上使用/system/bin下的命令,还能下载新的指令使用。

  1. Termux之SSH
  
    运维从访问远程服务器开始,这怎么离得开ssh命令。Termux不自带ssh命令,需先安装才能使用。我们可以 apt install openssh 安装openssh到终端。安装的openssh包括客户端ssh和服务端sshd,也就是说我们既可以使用ssh访问远程设备,也可以在本机上开启ssh服务以方便其他设备远程访问本机。默认情况下,安装openssh不开启服务端,有需要的童鞋可自行开启。

Termux终端中使用ssh访问远程服务器与Linux终端中使用ssh别无二致。但要使用ssh访问Android设备就不同了,Termux终端中sshd服务不支持密码验证,也就是说用户不能期望通过ssh user@server然后输入用户密码的方式从别的终端访问Android设备。Termux终端中sshd只支持密钥验证。

SSH验证的基本原理
  
SSH的英文全称为Secure Shell,是IETF (Internet Engineering Task Force) 的Network Working Group所制定的一族协议,其目的是要在非安全网络上提供安全的远程登录和其他安全网络服务。用于在主机之间建立起安全连接, 并加密传输内容, 以达到安全的远程访问, 操作以及数据传输的目的.

SSH协议目前有SSH1和SSH2两个主流版本,SSH2协议兼容SSH1,强烈建议使用SSH2版本。目前实现SSH1和SSH2协议的主要软件有OpenSSH 和SSH Communications Security Corporation公司的SSH Communications 软件。前者是OpenBSD组织开发的一款免费的SSH软件,后者是商业软件,因此在linux、FreeBSD、OpenBSD 、NetBSD等免费类UNIX系统种,通常都使用OpenSSH作为SSH协议的实现软件。

SSH主要有两个特点: 1. 安全性 2. 传输速度快。与FTP、POP 和 Telnet 等传统网络服务使用明文传输数据、命令和口令不同,SSH可以对所有传输的数据进行加密,能够防止 DNS 欺骗和 IP 欺骗。

SSH支持两种认证方式: 密码认证和密钥认证。两种认证方式的基本过程如下:
  
密码认证:

客户端向服务端发起登录请求, 服务端将自己的公钥返回给客户端
  
客户端输入登录口令, 口令经服务端公钥加密后发送到服务端
  
服务端接收到加密口令后使用私钥解密,如果密码正确则登录成功
  
这里第一步 (即服务端返回公钥) 就是我们日常使用ssh过程中看到的类似下面内容的过程:

The authenticity of host 'host (12.18.429.21)' can't be established.
  
RSA key fingerprint is 98:2e:d7:e0:de:9f:ac:67:28:c2:42:2d:37:16:58:4d.
  
Are you sure you want to continue connecting (yes/no)?
  
大概意思是说欲链接的主机无法验证真实性,只知道其公钥指纹,询问是否继续建立连接。98:2e:d7:e0:de:9f:ac:67:28:c2:42:2d:37:16:58:4d就是主机的公钥指纹,一个128位的01编码。公钥指纹是公钥的摘要,要知道公钥是一个长度为1024及以上的01编码,人为辨别公钥难度极大,因此采用摘要算法得到公钥的摘要,对比摘要要比对比公钥容易得多。
  
密码认证本质上是安全的,但如果有人假冒服务端就能骗取登录口令,因此密码认证无法避免遭受中间人攻击,何况每次登录都要输入口令,安全性就进一步降低了。唯一能保证密码认证方式安全的途径就是: 远程主机必须在自己的网站上贴出公钥指纹,以便用户自行核对。

密钥认证:
  
密钥认证的方式要比密码认证的方式来得更加安全,用户不仅不需要每次都输入登录口令,而且还可以选择对密钥进行加密以防止因密钥泄露而导致的安全隐患。密钥认证的一般过程如下:

客户端发起密钥连接请求,并上传身份信息
  
服务端收到请求后,在可信列表中查询客户端,若无此客户端则断开连接,否则发送一串随机问询码,该问询码使用此客户端公钥加密处理
  
客户端收到加密问询码后,使用私钥解密出问询码再用通信session对问询码加密并传送给服务端
  
服务端解密问询码并判定客户端身份安全与否,安全则建立连接
  
因此,密钥认证首要要将客户端的公钥放置在服务端的授权登录列表中。密钥认证一般不需要密码,但客户端可在生成密钥时指定密钥加密密码,这样在与服务端建立连接时需要输入加密密码来解密私钥,防止因私钥泄露带来的安全问题。

SSH通过Termux登录Android设备
  
Openssh包含SSHD服务,因此Android设备上,通过Termux安装openssh后可以开启ssh服务,ssh服务的配置文件默认在$PREFIX/etc/ssh/sshd_config 中。值得注意的是Termux终端中sshd服务不支持密码认证,也就是说用户想要通过ssh连接上Android设备,只能通过密钥认证方式先将设备公钥放置在Android设备的sshd服务的授权登录列表中,然后通过私钥校验的方式登录。具体来说:

将设备公钥添加都授权登录列表中

cat id_rsa.pub >> $HOME/.ssh/authorized_keys

开启ssh服务

sshd
  
出于安全考虑,Android设备Termux终端中sshd服务默认运行在 8022端口,而不是常规22端口,用户可以在 sshd_config 中指定sshd服务监听的端口号。其他设备上可通过 ssh username@ip -p port的方式登录Android设备。

  1. Termux之Aria2
  
    Termux开通了ssh服务后就可以通过ssh连接到Android设备的Termux终端进行一系列操作,要知道使用传统键盘敲命令行的体验可是Android键盘不能 比拟的,即使你安装了黑客键盘。
  
    下面介绍另一个非常有用的命令行工具 - Aria2。Aria2是一个轻量级的命令行下载程序,类似wget但支持更多的通信协议,功能更加强大。>>前往Aria2主页
  
    Termux资源库中有aria2安装包,我们可以像在Linux上一样通过apt install aria2轻松在Android设备上安装aria2,当然这种方式安装的aria2运行在Termux终端环境下,不能独立运行。用户可选择从Google Play下载封装了aria2的应用程序来代替命令行安装。此外用户还可以下载aria2的Android编译版放置在Termux环境中或系统环境中 (应该需要root 权限) 来使设备支持aria2。>>前往Github下载预编译版
  
    Aria2的使用方法在上一篇文章 "使用Aria2完成下载任务" 中已经进行说明,这里不再赘述。本节主要补充一个更适合Android上使用aria2的GUI界面,毕竟文章 "使用Aria2完成下载任务" 中介绍的两个主流GUI界面都是基于WEB开发的,在小屏的Android设备上使用起来还是有诸多不便。本节的主角是 Transdroid。

什么是Transdroid
  
Transdroid 是国外某大神开发的Torrent下载管理软件 (当然是Android版) ,软件以简洁友好据称,主要帮助用户在Android设备上管理PC或服务器上的下载任务。

当前下载列表

当前任务下载状态
  
Transdroid只是一个下载管理器,不是一个下载器,真正负责下载任务的是你的PC或服务器上的uTorrent,Transmission, rTorrent, Vuze, Deluge, BitTorrent 6, qBittorrent等专用于下载的客户端。使用Transdroid进行下载任务管理只需两步:

客户端开启web管理API
  
Transdroid 通过API获取下载器的任务信息,并能够在Transdroid上实现新增、暂停、删除下载任务的基本操作
  
关于Transdroid的配置方法和其他具体信息可参考:

Transdroid官网: [https://www.transdroid.org/](https://www.transdroid.org/)
  
Transdroid on Github: [https://github.com/erickok/transdroid](https://github.com/erickok/transdroid)
  
自行搜索其他相关信息

使用Transdroid管理Aria2
  
Transdroid支持的下载器有很多,包括Aria2。按文章 "使用Aria2完成下载任务"的步骤配置并启动aria2命令后即可使用Transdroid连接aria2进行管理,设置方法和使用WebUI大同小异。只需要注意配置Transdroid时使用正确的ip和端口即可。

如果aria2运行在其他设备,如PC或服务器上 (下文称"下载机") ,需在Transdroid中正确填写PC或服务器的IP,并确保防火墙允许其他设备从aria2运行的端口访问aria2下载机。局域网内,一般防火墙设置得当则Android设备能无障碍访问下载机的下载任务信息。如果想随时随地通过Android设备管理下载机上的下载任务,你还需要为你的局域网设置端口映射,参考 Setting up µTorrent - Allow access from anywhere

在本节中主要是介绍在Android设备上使用Aria2进行下载,并使用Transdroid进行下载管理,因此Transdroid和Aria2运行在一个设备上,不存在防火墙和端口映射的问题,直接在Transdroid中设置好即可。Aria2+Transdroid完全能够代替其他手机版下载软件,并且表现完美。唯一的问题是aria2依托于Termux终端环境,终端关闭,Aria2下载服务也就关闭了。因此,要在Android中使用Aria2获得友好下载体验,要同时打开Termux终端运行aria2服务和Transdroid下载管理程序。

关于结合Aria2和Transdroid的尝试还可参见: [https://github.com/UKeyboard/aria2](https://github.com/UKeyboard/aria2)
