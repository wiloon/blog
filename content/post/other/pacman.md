---
title: pacman
author: "-"
date: 2022-08-22 15:53:48
url: pacman
categories:
  - Linux
tags:
  - Arch Linux
  - remix
---
## pacman

## 参数, options

```bash
-Q 查询 pacman 数据库
-o <file> 查看某个文件属于哪个包
--needed 已经是最新版本的包，不会再重新安装
```

### 在仓库里搜索有关 foo 的包

```bash
pacman -Ss foo
```

### error: signature from xxx is invalid

```bash
pacman -Sy archlinux-keyring
```

```bash
# pacman 的 help
pacman -h

# -Q 的 help
pacman -Q -h
pacman -Q                # 列出已经安装的软件包
pacman -Q  boost-libs    #Display version
pacman -Ql boost-libs    #Display file list provided by local package

# 查看文件/命令属于哪个包, Check if the file is owned by any package, 查看命令由哪个包提供.
pacman -Qo /etc/profile

# 检查包对应的文件有没有缺失, #Check the local package database
pacman -Qk filesystem

# 打印详细信息,比如 文件 是否有修改 修改时间, 大小 , md5
pacman -Qkk filesystem

# 安装下载的 gvim 包，或新编译的 gvim 包
pacman -U /var/cache/pacman/pkg/gvim-8.2.4106-1-x86_64.pkg.tar.zst
```

## downgrade 降级软件包

去 archive 时手动下载 <https://archive.archlinux.org/packages/>, 然后 pacman -U 安装

### archlinux downgrade, 回退软件包到某一天

```bash
vim /etc/pacman.d/mirrorlist

# content
SigLevel = PackageRequired
Server = https://archive.archlinux.org/repos/2022/11/04/$repo/os/$arch

pacman -Syyuu
```

### 忽略/排除升级软件包, 不升级指定的包
  
如果由于某种原因，你不希望升级某个软件包，可以加入内容如下:
  
```bash
IgnorePkg = linux
```

### (invalid or corrupted package (PGP signature)), signature from xxx is unknown trust

error: unzip: signature from "Jonas Witschel <diabonas@gmx.de>" is unknown trust
:: File /var/cache/pacman/pkg/unzip-6.0-16-x86_64.pkg.tar.zst is corrupted (invalid or corrupted package (PGP signature)).

<https://bbs.archlinux.org/viewtopic.php?id=128682>

```bash
pacman -Sy archlinux-keyring
```

#### trust all

```bash
vim /etc/pacman.conf
# content
SigLevel = Optional TrustAll
```

#### refresh keys

```bash
# 查看key的状态, 提示是 expired
pacman-key --list-sigs Witschel

# 更新 keys
pacman-key --refresh-keys
# 查看Master组的key的状态
pacman-key --list-sigs Master
# 提示 undefined，所以用对应的ID删除再重新导入即可

pacman-key --delete 91FFE0700E80619CEB73235CA88E23E377514E00
pacman-key --populate archlinux
```

### downgrade one package

```bash
yay -S downgrade
sudo downgrade cmake
#输入要降级到的版本前面的数字并回车。
```

### pacman mirror list

```bash
vim  /etc/pacman.d/mirrorlist

# /etc/pacman.d/mirrorlist
Server = http://mirrors.163.com/archlinux/$repo/os/$arch
Server = http://mirrors.aliyun.com/archlinux/$repo/os/$arch
Server = http://mirrors.neusoft.edu.cn/archlinux/
Server = http://mirrors.lug.mtu.edu/archlinux/
Server = http://mirrors.kernel.org/archlinux/$repo/os/$arch
```

#### 按名字找包

```bash
pacman -Sl |grep jdk
```

### Enabling multilib

To enable multilib repository, uncomment the [multilib] section in /etc/pacman.conf:

```bash
/etc/pacman.conf
[multilib]
Include = /etc/pacman.d/mirrorlist
```

```bash
# for downgrade
#Server=https://archive.archlinux.org/repos/2018/06/17/$repo/os/$arch
```

### --noconfirm, yes

```bash
--noconfirm
# Bypass any and all "Are you sure?" messages. It's not a good idea to do this unless you want to run pacman from a script.
```

### archlinux key could not be looked up remotely

```bash
sudo pacman -S archlinux-keyring && sudo pacman -Syu

# 要删除软件包，但是不删除依赖这个软件包的其他程序: 
pacman -Rdd package_name

```

### unable to lock database

出现这个提示一般有两种情况

- 有 .lck 文件
- 磁盘满了

```bash
sudo rm /var/lib/pacman/db.lck
```

## 查看软件包依赖

### pactree, 查看 packageName 依赖了哪些软件包

```bash
# pactree 在 pacman-contrib 包里
pacman -S pacman-contrib
pactree <packageName>
```

### pactree，查看 packageName 被哪些软件包依赖了

```bash
pactree -r <packageName>
```

## 升级系统中所有已安装的包
  
pacman -Su

## 升级系统和同步仓库数据
  
pacman -Syu

## 忽略/排除指定包
  
pacman -Su -ignore postgresql -ignore libpqxx

whoneeds package-name

sudo pacman -S pacman-contrib

pacman -Sy abc #和源同步后安装名为abc的包
  
pacman -S abc #从本地数据库中得到abc的信息，下载安装abc包
  
pacman -Sf abc #强制安装包abc
  
pacman -Si abc #从数据库中搜索包abc的信息

pacman -Qe # 列出已经安装的软件包， 只列出不被其它包依赖的
pacman -Qet # 列出已经安装的软件包， 只列出不被其它包依赖的,不包含可选依赖。
  
pacman -Q abc # 检查某一个软件包是否已经安装
  
pacman -Qi abc #列出已安装的包abc的详细信息
  
pacman -Ql abc # 列出abc软件包的所有文件
  
pacman -Qo /path/to/abc # 列出abc文件所属的软件包
  
pacman -Syu #同步源，并更新系统
  
pacman -Sy #仅同步源
  
pacman -Su #更新系统
  
pacman -R abc #删除abc包
  
pacman -Rd abc #强制删除被依赖的包
  
pacman -Rc abc #删除abc包和依赖abc的包
  
pacman -Rsc abc #删除abc包和abc依赖的包
  
pacman -Sc #清理/var/cache/pacman/pkg目录下的旧包
  
pacman -Scc #清除所有下载的包和数据库
  
pacman -Sd abc #忽略依赖性问题，安装包abc
  
pacman -Su –ignore foo #升级时不升级包foo
  
pacman -Sg abc #查询abc这个包组包含的软件包

## 限速
  
由于办公室装修，临时借宿到另一个兄弟公司干活。不过这兄弟可不够厚道，分配给我们的网络做了非常不人道的限制，每个网卡限速20k，于是乎瞬间回退到小猫时代。在这样的环境下，如果有时需要安装一些东西，就会由于pacman把带宽全部抢占而导致网页打不开、MSN断线等一系列严重后果。

不过还好，虽然pacman并没有提供限速的功能，但是它提供了比较灵活的接口来使用其他下载程序。我使用的是wget，只要在/etc/pacman.conf中将XferCommand设置为如下配置即可实现限速10k的目的了。

XferCommand = /usr/bin/wget –passive-ftp –limit-rate=10k -c -O %o %u

查询包数据库
  
Pacman 可以在包数据库中查询软件包，查询位置包含了包的名字和描述:

Pacman 包管理器是 ArchLinux 的一大亮点。它汲取了其他 Linux 版本软件管理的优点，譬如Debian的APT机制、Redhat的Yum机制、 Suse的Yast等，对于安装软件提供了无与伦比的方便。另外由于ArchLinux是一个针对i686架构优化的发行版，因此对于软件的效率提高也有一定的帮助。pacman可以说是ArchLinux的基础，因为ArchLinux默认安装非常少的软件，其他软件都是使用pacman通过网络来安装的。它将一个简单的二进制包格式和易用的构建系统结合了起来。Pacman使得简单的管理与自定义软件包成为了可能，而不论他们来自于官方的Arch软件库或是用户自己创建的。Pacman可以通过和主服务器同步包列表来进行系统更新，这使得注重安全的系统管理员的维护工作成为轻而易举的事情。

下面是偶总结的Pacman命令参数:

安装软件包

安装或者升级单个软件包，或者一列软件包 (包含依赖包)， 使用如下命令:

pacman -S package_name1 package_name2
  
有时候在不同的软件仓库中，一个软件包有多个版本 (比如extra和testing) 。你可以选择一个来安装:

编辑/etc/pacman.d/mirrorlist，重新选择一个源。再pacman -Suy更新系统，或pacman -Syy更新软件库。

pacman -S extra/package_name
  
pacman -S testing/package_name
  
删除软件包
  
删除单个软件包，保留其全部已经安装的依赖关系

pacman -R package_name
  
删除指定软件包，及其所有没有被其他已安装软件包使用的依赖关系:

pacman -Rs package_name
  
缺省的，pacman会备份被删除程序的配置文件，将它们加上*.pacsave扩展名。如果你在删除软件包时要同时删除相应的配置文件 (这种行为在基于Debian的系统中称为清除purging) ，你可是使用命令:

pacman -Rn package_name
  
当然，它也可以加上-s参数来删除当前无用的依赖。这样的话，真正删除一个软件包、它的配置文件以及所有不再需要的依赖的命令如下:

pacman -Rsn package_name
  
注意！Pacman不会删除软件包安装后才创建的配置文件。你可以从你的home文件夹中手动删除它们。

pacman -Ss package
  
要查询已安装的软件包:

pacman -Qs package
  
一旦你得到了软件包的完整名字，你可以获取关于它的更为详尽的信息:

pacman -Si package
  
pacman -Qi package
  
要获取已安装软件包所包含文件的列表:

pacman -Ql package
  
要罗列所有不再作为依赖的软件包(孤立orphans):

pacman -Qdt
  
Pacman使用-Q参数来查询本地软件包数据库。参见:

pacman -Q –help
  
…而使用-S参数来查询远程同步的数据库。参见:

pacman -S –help
  
详情可参见pacman man。

其它用法
  
Pacman是个非常广泛的包管理工具，这里只是它的一些其它主要特性。

下载包而不安装它:
  
pacman -Sw package_name
  
安装一个'本地'包 (不从源里) :
  
pacman -U /path/to/package/package_name-version.pkg.tar.gz
  
安装一个'远程'包 (不从源里) :
  
pacman -U <http://url/package_name-version.pkg.tar.gz>
  
清理当前未被安装软件包的缓存(/var/cache/pacman/pkg):
  
pacman -Sc
  
完全清理包缓存:
  
pacman -Scc
  
Warning: 关于pacman -Scc，仅在你确定不需要做任何软件包降级工作时才这样做。pacman -Scc会从缓存中删除所有软件包。
  
要删除孤立软件包 (递归的，要小心):
  
pacman -Rs $(pacman -Qtdq)
  
重新安装你系统中所有的软件包 (仓库中已有的) :
  
pacman -S $(pacman -Qq | grep -v "$(pacman -Qmq)")
  
获取本地软件包和它们大小的一个已排序清单列表:
  
LANG=C pacman -Qi | sed -n '/^Name[^:]*: (.*)/{s//1 /;x};/^Installed[^:]*: (.*)/{s//1/;H;x;s/n//;p}' | sort -nk2
  
要了解更详细的参数开关可以pacman –help或者man pacman。

配置
  
Pacman的配置文件位于/etc/pacman.conf。关于配置文件的进一步信息可以用man pacman.conf查看。

常用选项
  
常用选项都在[options]段。阅读man手册或者查看缺省的pacman.conf可以获得有关信息和用途。
  
多软件包可以用空格隔开，也可是用 glob 模式。如果只打算忽略一次升级，可以使用 -ignore 选项。

忽略了的软件包可通过 pacman -S 升级。

和软件包一样，你也可以象这样跳过升级某个软件包组:

IgnoreGroup = gnome
  
附注:
  
ArchLinux的版本库里面包括:
  
core-核心软件包
  
extra-其他常用软件
  
community-社区软件包，譬如MySQL等。
  
testing-正在测试阶段，还没有正式加入源的软件包。通常软件版本比较新，但是不是非常稳定
  
release-已经发布的软件包
  
unstable-非正式的软件包，可能包括以前版本的软件或者测试软件

因为Pacman的软件都是从源里面更新，因此在/etc/pacman.d里面配置这些软件源的地址。
  
在/etc/pacman.d目录里面分别有上面几种软件类型对应的文件名，可以自己手工配置这些软件源的地址。

<http://jsome.net/blog/2010/01/18/tips-for-pacman>
  
<http://blog.chinaunix.net/uid-20728322-id-2454942.html>

### pacman, installing foo breaks dependency 'bar' required by xxx

```bash
installing xorgproto (2019.2-2) breaks dependency 'dmxproto' required by libdmx
installing xorgproto (2019.2-2) breaks dependency 'xf86dgaproto' required by libxxf86dga
```

```bash
sudo pacman -Rdd libdmx libxxf86dga && sudo pacman -Syu
```

## error: oniguruma: signature from is marginal trust

```bash
sudo pacman -Sy archlinux-keyring
```

## 'archlinux  downgrading'

<https://wiki.archlinux.org/index.php/Arch_Linux_Archive>

replacing your /etc/pacman.d/mirrorlist with the following content:

## Arch Linux repository mirrorlist

## Generated on 2042-01-01
  
Server=<https://archive.archlinux.org/repos/2014/03/30/>$repo/os/$arch
  
Then update the database and force downgrade:

pacman -Syyuu

<https://www.geniusxiaoshuai.com/exp/93.html>

## 一个切换 mirror 的脚本

```bash
#!/bin/bash

printf "1. China\n2. Japan\nSelect mirror (leave blank for China):"

read -r locationId

if [ "" == "$locationId" ];then
  locationId="1"
fi

if [ "1" == "$locationId" ];then
  echo "Chinese mirror"

  sudo bash -c 'cat > /etc/pacman.d/mirrorlist << EOF
Server = http://mirrors.163.com/archlinux/\$repo/os/\$arch
Server = https://mirrors.aliyun.com/archlinux/\$repo/os/\$arch
Server = http://mirrors.neusoft.edu.cn/archlinux/
Server = http://mirrors.lug.mtu.edu/archlinux/
Server = http://mirrors.kernel.org/archlinux/\$repo/os/\$arch
EOF'

else

  sudo bash -c 'cat > /etc/pacman.d/mirrorlist << EOF
Server = http://mirrors.cat.net/archlinux/\$repo/os/\$arch
Server = https://mirrors.cat.net/archlinux/\$repo/os/\$arch
Server = http://ftp.tsukuba.wide.ad.jp/Linux/archlinux/\$repo/os/\$arch
Server = http://ftp.jaist.ac.jp/pub/Linux/ArchLinux/\$repo/os/\$arch
Server = https://ftp.jaist.ac.jp/pub/Linux/ArchLinux/\$repo/os/\$arch
EOF'

fi
```
