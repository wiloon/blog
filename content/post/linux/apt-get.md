---
title: apt-get, apt basic command
author: "-"
date: 2012-02-26T03:18:38+00:00
url: apt
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

<https://stackoverflow.com/questions/27455626/how-to-remove-an-incomplete-package-by-using-apt-get>
  
<https://blog.csdn.net/zc123456zzc/article/details/47153913>

### debian packages

><https://www.debian.org/distrib/packages>

## apt, apt-get, aptitude
Ubuntu(Debian)的aptitude与apt-get的区别和联系
      最近在使用Puppet快速部署Openstack，看到一些没见过的工具，例如aptitude，在Ubuntu上有强大的apt-get为什么还要用这个呢。本文转自: http://hi.baidu.com/52safe/blog/item/c17891ff02201653d6887d96.html

起初GNU/Linux系统中只有.tar.gz。用户 必须自己编译他们想使用的每一个程序。在Debian出现之後，人们认为有必要在系统 中添加一种机 制用来管理 安装在计算机上的软件包。人们将这套系统称为dpkg。至此着名的‘package’首次在GNU/Linux上出现。不久之後红帽子也开始着 手建立自己的包管理系统 ‘rpm’。

GNU/Linux的创造者们很快又陷入了新的窘境。他们希望通过一种快捷、实用而且高效的方式来安装软件包。这些软件包可以自动处理相互之间 的依赖关系，并且在升级过程中维护他们的配置文件 。Debian又一次充当了开路先锋的角色。她首创了APT (Advanced Packaging Tool) 。这一工具後来被Conectiva 移植到红帽子系统中用于对rpm包的管理。在其他一些发行版中我们也能看到她的身影。

“同时，apt是一个很完整和先进的软件包管理程序，使用它可以让你，又简单，又准确的找到你要的的软件包， 并且安装或卸载都很简洁。 它还可以让你的所有软件都更新到最新状态，而且也可以用来对ubuntu 进行升级。”

“apt是需要用命令 来操作的软件，不过现在也出现了很多有图形的软件，比如Synaptic, Kynaptic 和 Adept。”

命令

下面将要介绍的所有命令都需要sudo！使用时请将“packagename”和“string”替换成您想要安装或者查找的程序。

* apt-get update——在修改/etc/apt/sources.list或者/etc/apt/preferences之後运行该命令。此外您需要定期运行这一命令以确保您的软件包列表是最新的。

* apt-get install packagename——安装一个新软件包 (参见下文的aptitude ) 

* apt-get remove packagename——卸载一个已安装的软件包 (保留配置文件) 

* apt-get –purge remove packagename——卸载一个已安装的软件包 (删除配置文件) 

* dpkg –force-all –purge packagename 有些软件很难卸载，而且还阻止了别的软件的应用 ，就可以用这个，不过有点冒险。

* apt-get autoclean apt会把已装或已卸的软件都备份在硬盘上，所以如果需要空间 的话，可以让这个命令来删除你已经删掉的软件

* apt-get clean 这个命令会把安装的软件的备份也删除，不过这样不会影响软件的使用的。

* apt-get upgrade——更新所有已安装的软件包

* apt-get dist-upgrade——将系统升级到新版本

* apt-cache search string——在软件包列表中搜索字符串

* dpkg -l package-name-pattern——列出所有与模式相匹配的软件包。如果您不知道软件包的全名，您可以使用“*package-name-pattern*”。

* aptitude——详细查看已安装或可用的软件包。与apt-get类似，aptitude可以通过命令行方式调用，但仅限于某些命令——最常见的有安装和卸载命令。由于aptitude比apt-get了解更多信息，可以说它更适合用来进行安装和卸载。

* apt-cache showpkg pkgs——显示软件包信息。

* apt-cache dumpavail——打印可用软件包列表。

* apt-cache show pkgs——显示软件包记录，类似于dpkg –print-avail。

* apt-cache pkgnames——打印软件包列表中所有软件包的名称。

* dpkg -S file——这个文件属于哪个已安装软件包。

* dpkg -L package——列出软件包中的所有文件。

* apt-file search filename——查找包含特定文件的软件包 (不一定是已安装的) ，这些文件的文件名中含有指定的字符串。apt-file是一个独立的软件包。您必须先使用apt-get install来安装它，然後运行apt-file update。如果apt-file search filename输出的内容太多，您可以尝试使用apt-file search filename | grep -w filename (只显示指定字符串作为完整的单词出现在其中的那些文件名) 或者类似方法，例如: apt-file search filename | grep /bin/ (只显示位于诸如/bin或/usr/bin这些文件夹中的文件，如果您要查找的是某个特定的执行文件的话，这样做是有帮助的) 。

＊ apt-get autoclean——定期运行这个命令来清除那些已经卸载的软件包的.deb文件。通过这种方式，您可以释放大量的磁盘空间。如果您的需求十分迫切，可以使用apt-get clean以释放更多空间。这个命令会将已安装软件包裹的.deb文件一并删除。大多数情况下您不会再用到这些.debs文件，因此如果您为磁盘空间不足而感到焦头烂额，这个办法也许值得一试。

典型应用

我是个赛车发烧友，想装个赛车类游戏玩玩。有哪些赛车类游戏可供选择呢？
apt-cache search racing game
出来了一大堆结果。看看有没有更多关于torcs这个游戏的信息。
apt-cache show torcs
看上去不错。这个游戏是不是已经安装了？最新版本是多少？它属于哪一类软件，universe还是main?
apt-cache policy torcs
好吧，现在我要来安装它！
apt-get install torcs
在控制台下我应该调用什么命令来运行这个游戏呢？在这个例子中，直接用torcs就行了，但并不是每次都这么简单。我们可一通过查找哪些文件被安 装到了 “/usr/bin”文件夹下来确定二进制文件名。对于游戏软件，这些二进制文件将被安装到“/usr/games”下面。对于系统管理工具相应的文件夹是“/usr/sbin”。

这个游戏很酷哦。说不定还有其他赛道可玩的？
apt-cache search torcs
我的磁盘空间不够用了。我得把apt的缓存空间清空才行。
apt-get clean
哦不，老妈叫我把机器上的所有游戏都删掉。但是我想把配置文件保留下来，这样待会我只要重装一下就可以继续玩了。
apt-get remove torcs
如果我想连配置文件一块删除: 
apt-get remove –purge torcs
额外的软件包
deborphan和debfoster工具可以找出已经安装在系统上的不会被用到的软件包。
提高命令行方式下的工作效率
您可以通过定义别名 (alias) 来提高这些命令的输入速度。例如，您可以在您的*~/.bashrc*文件中添加下列内容

alias acs=’apt-cache search’
alias agu=’sudo apt-get update’
alias agg=’sudo apt-get upgrade’
alias agd=’sudo apt-get dist-upgrade’
alias agi=’sudo apt-get install’
alias agr=’sudo apt-get remove’

或者使用前面介绍的aptitude命令，如“alias agi=’sudo aptitude install’”。

———————————————————————————————-

aptitude 与 apt-get 一样，是 Debian 及其衍生系统中功能极其强大的包管理工具。与 apt-get 不同的是，aptitude 在处理依赖问题上更佳一些。举例来说，aptitude 在删除一个包时，会同时删除本身所依赖的包。这样，系统中不会残留无用的包，整个系统更为干净。以下是笔者总结的一些常用 aptitude 命令，仅供参考。
命令 作用
aptitude update 更新可用的包列表
aptitude upgrade 升级可用的包
aptitude dist-upgrade 将系统升级到新的发行版
aptitude install pkgname 安装包
aptitude remove pkgname 删除包
aptitude purge pkgname 删除包及其配置文件
aptitude search string 搜索包
aptitude show pkgname 显示包的详细信息
aptitude clean 删除下载的包文件
aptitude autoclean 仅删除过期的包文件

当然，你也可以在文本界面模式中使用 aptitude。

 

有的问题 apt-get 解决不了，必须使用 aptitude 解决，有的问题，用 aptitude 解决不了，必须使用 apt-get


aptitude 解决得更好的地方:  install, remove, reinstall (apt-get无此功能) , show (apt-get无此功能) , search (apt-get无此功能) , hold (apt-get无此功能) , unhold (apt-get无此功能) , 
apt-get 解决得更好的地方:  source (aptitude无此功能) , build-dep  (低版本的aptitude没有build-dep功能) 
apt-get 跟 aptitude 没什么区别的地方: update, upgrade (apt-get upgrade=aptitude safe-upgrade, apt-get dist-upgrade=aptitude full-upgrgade)


---

https://www.cnblogs.com/yuxc/archive/2012/08/02/2620003.html