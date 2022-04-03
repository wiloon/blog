---
title: apt-get, apt basic command
author: "-"
date: 2012-02-26T03:18:38+00:00
url: /?p=2447
categories:
  - Linux

tags:
  - reprint
---
## apt-get, apt basic command
### 列出软件包安装了哪些文件
    
    dpkg -L package

### 列出已安装的软件包
  apt list --installed

## apt 查询软件包
  apt-cache search keyword

### list versions in cache
  apt-cache madison  package_name_0
  sudo apt-get autoremove
  sudo apt-get --purge remove
  sudo dpkg --remove --force-remove-reinstreq tspc
  sudo apt-get autoclean
  sudo apt-get clean
  sudo apt-get -f install
### remove 
  apt-get remove packagename

### answer yes
    apt-get -y install [packagename]

### /etc/apt/sources.list
#### debian 10
    deb http://mirrors.163.com/debian/ buster main non-free contrib
    deb http://mirrors.163.com/debian/ buster-updates main non-free contrib
    deb http://mirrors.163.com/debian/ buster-backports main non-free contrib
    deb-src http://mirrors.163.com/debian/ buster main non-free contrib
    deb-src http://mirrors.163.com/debian/ buster-updates main non-free contrib
    deb-src http://mirrors.163.com/debian/ buster-backports main non-free contrib
    deb http://mirrors.163.com/debian-security/ buster/updates main non-free contrib
    deb-src http://mirrors.163.com/debian-security/ buster/updates main non-free contrib

apt-get是一条linux命令，适用于deb包管理式的操作系统，主要用于自动从互联网的软件仓库中搜索、安装、升级、卸载软件或操作系统。apt-get命令一般需要root权限执行，所以一般跟着sudo命令:

在修改/etc/apt/sources.list或/etc/apt/preferences之後运行该命令。此外您需要定期运行这一命令以确保您的软件包列表是最新的。

apt-get update
  
安装一个新软件包 (参见下文的aptitude) 

apt-get upgrade

apt-get install packagename
  
卸载一个已安装的软件包 (保留配置文档) 


  
在软件包列表中搜索字符串

apt-get -purge remove packagename

卸载一个已安装的软件包 (删除配置文档) 

dpkg -force-all -purge packagename

有些软件很难卸载，而且还阻止了别的软件的应用，就能够用这个，但是有点冒险。

apt-get autoclean apt

会把已装或已卸的软件都备份在硬盘上，所以假如需要空间的话，能够让这个命令来删除您已删掉的软件

apt-get clean
  
这个命令会把安装的软件的备份也删除，但是这样不会影响软件的使用。

apt-get upgrade

更新任何已安装的软件包

apt-get dist-upgrade

将系统升级到新版本

dpkg -l package-name-pattern

列出任何和模式相匹配的软件包。假如您不知道软件包的全名，您能够使用"_package-name-pattern_"。

aptitude

周详查看已安装或可用的软件包。和apt-get类似，aptitude能够通过命令行方式调用，但仅限于某些命令——最常见的有安装和卸载命令。由于

aptitude比apt-get了解更多信息，能够说他更适合用来进行安装和卸载。

apt-cache showpkg pkg

显示软件包信息。

apt-cache dumpavail

打印可用软件包列表。

apt-cache show pkg

显示软件包记录，类似于dpkg –print-avail。

apt-cache pkgname

打印软件包列表中任何软件包的名称。

dpkg -S file

这个文档属于哪个已安装软件包。



apt-file search filename

查找包含特定文档的软件包 (不一定是已安装的) ，这些文档的文档名中含有指定的字符串。apt-file是个单独的软件包。您必须先使用apt-get install来安装他，然後运行apt-file update。假如apt-file search filename输出的内容太多，您能够尝试使用apt-file search filename | grep -w filename (只显示指定字符串作为完整的单词出现在其中的那些文档名) 或类似方法，例如: apt-file search filename | grep /bin/ (只显示位于诸如/bin或/usr/bin这些文档夹中的文档，假如您要查找的是某个特定的执行文档的话，这样做是有帮助的) 。

＊ apt-get autoclean

定期运行这个命令来清除那些已卸载的软件包的.deb文档。通过这种方式，您能够释放大量的磁盘空间。假如您的需求十分迫切，能够使用apt-get clean以释放更多空间。这个命令会将已安装软件包裹的.deb文档一并删除。大多数情况下您不会再用到这些.debs文档，因此假如您为磁盘空间不足而感到焦头烂额，这个办法也许值得一试。

apt-get update时卡在 waiting for headers

apt-get update时卡在 waiting for headers，等了好久，最后报出Hash Sum mismatch的错误
  
解决方法: 

```bash
rm -rf /var/lib/apt/lists/*
apt-get update
```

https://stackoverflow.com/questions/27455626/how-to-remove-an-incomplete-package-by-using-apt-get
  
https://blog.csdn.net/zc123456zzc/article/details/47153913

### debian packages
>https://www.debian.org/distrib/packages
