---
title: dnf basic
author: "-"
date: 2020-04-26T02:14:25+00:00
url: dnf
categories:
  - Linux
tags:
  - reprint
  - remix
---
## dnf basic

### 升级所有系统软件包
用处: 该命令用于升级系统中所有有可用升级的软件包

```Bash
# "update" is just a deprecated alias for "upgrade", they do exactly the same thing.
dnf update
dnf upgrade
```


### 安装

```Bash
    dnf install rsync
```

### 删除

    dnf remove nano 或 # dnf erase nano

### 删除无用孤立的软件包

用处: 当没有软件再依赖它们时，某一些用于解决特定软件依赖的软件包将会变得没有存在的意义，该命令就是用来自动移除这些没用的孤立软件包。  

    dnf autoremove

```bash
dnf --version
dnf repolist
– 查看系统中可用和不可用的所有的 DNF 软件库

用处: 该命令用于显示系统中可用和不可用的所有的 DNF 软件库

命令: # dnf repolist all
– 列出所有安装了的 RPM 包
dnf list installed

– 列出所有 RPM 包
dnf list
– 列出所有可供安装的 RPM 包

用处: 该命令用于列出来自所有可用软件库的可供安装的软件包

命令: # dnf list available

– 搜索软件库中的 RPM 包

用处: 当你不知道你想要安装的软件的准确名称时，你可以用该命令来搜索软件包。你需要在"search"参数后面键入软件的部分名称来搜索。 (在本例中我们使用"nano") 

命令: # dnf search nano

– 查看软件包详情

用处: 当你想在安装某一个软件包之前查看它的详细信息时，这条命令可以帮到你。 (在本例中，我们将查看"nano"这一软件包的详细信息) 

命令: # dnf info nano

– 安装软件包

用处: 使用该命令，系统将会自动安装对应的软件及其所需的所有依赖 (在本例中，我们将用该命令安装nano软件) 

命令: # dnf install nano

– 升级软件包

用处: 该命令用于升级制定软件包 (在本例中，我们将用命令升级"systemd"这一软件包) 

命令: # dnf update systemd

– 检查系统软件包的更新

用处: 该命令用于检查系统中所有软件包的更新

命令: # dnf check-update

dnf upgrade --refresh

dnf system-upgrade reboot

– 删除软件包

用处: 删除系统中指定的软件包 (在本例中我们将使用命令删除"nano"这一软件包) 

命令: # dnf remove nano 或 # dnf erase nano

– 删除无用孤立的软件包

用处: 当没有软件再依赖它们时，某一些用于解决特定软件依赖的软件包将会变得没有存在的意义，该命令就是用来自动移除这些没用的孤立软件包。

命令: # dnf autoremove

– 删除缓存的无用软件包

用处: 在使用 DNF 的过程中，会因为各种原因在系统中残留各种过时的文件和未完成的编译工程。我们可以使用该命令来删除这些没用的垃圾文件。

命令: # dnf clean all
– 获取有关某条命令的使用帮助

用处: 该命令用于获取有关某条命令的使用帮助 (包括可用于该命令的参数和该命令的用途说明)  (本例中我们将使用命令获取有关命令"clean"的使用帮助) 

命令: # dnf help clean

– 查看所有的 DNF 命令及其用途

用处: 该命令用于列出所有的 DNF 命令及其用途

命令: # dnf help

– 查看 DNF 命令的执行历史

用处: 您可以使用该命令来查看您系统上 DNF 命令的执行历史。通过这个手段您可以知道在自您使用 DNF 开始有什么软件被安装和卸载。

命令: # dnf history

– 查看所有的软件包组

用处: 该命令用于列出所有的软件包组

命令: # dnf grouplist

– 安装一个软件包组

用处: 该命令用于安装一个软件包组 (本例中，我们将用命令安装"Educational Software"这个软件包组) 

命令: # dnf groupinstall 'Educational Software'

– 升级一个软件包组中的软件包

用处: 该命令用于升级一个软件包组中的软件包 (本例中，我们将用命令升级"Educational Software"这个软件包组中的软件) 

命令: # dnf groupupdate 'Educational Software'
– 删除一个软件包组

用处: 该命令用于删除一个软件包组 (本例中，我们将用命令删除"Educational Software"这个软件包组) 

命令: # dnf groupremove 'Educational Software'

– 从特定的软件包库安装特定的软件

用处: 该命令用于从特定的软件包库安装特定的软件 (本例中我们将使用命令从软件包库 epel 中安装 phpmyadmin 软件包) 

命令: # dnf –enablerepo=epel install phpmyadmin

– 更新软件包到最新的稳定发行版

用处: 该命令可以通过所有可用的软件源将已经安装的所有软件包更新到最新的稳定发行版

命令: # dnf distro-sync

– 重新安装特定软件包

用处: 该命令用于重新安装特定软件包 (本例中，我们将使用命令重新安装"nano"这个软件包) 

命令: # dnf reinstall nano

– 回滚某个特定软件的版本

用处: 该命令用于降低特定软件包的版本 (如果可能的话)  (本例中，我们将使用命令降低"acpid"这个软件包的版本) 

命令: # dnf downgrade acpid
```

DNF 包管理器作为 YUM 包管理器的升级替代品，它能自动完成更多的操作。但在我看来，正因如此，所以 DNF 包管理器不会太受那些经验老道的 Linux 系统管理者的欢迎。举例如下: 

在 DNF 中没有 –skip-broken 命令，并且没有替代命令供选择。
  
在 DNF 中没有判断哪个包提供了指定依赖的 resolvedep 命令。
  
在 DNF 中没有用来列出某个软件依赖包的 deplist 命令。
  
当你在 DNF 中排除了某个软件库，那么该操作将会影响到你之后所有的操作，不像在 YUM 下那样，你的排除操作只会咋升级和安装软件时才起作用。
  
我相信几乎所有的 Linux 用户都会很高兴看到 Linux 生态圈不断地发展壮大。先是 systemd 代替了源于 System V 的 init ，而如今， DNF 包管理器已经在 Fedora 22 上替代了 YUM 包管理器，并且很快它也将登陆 RHEL 和 CentOS 。

此时此刻的你将作何感想？难道这整一个 Linux 生态圈已经变得不重视它的用户们，并且往与用户期望完全相反的方向发展了么？现在，没有任何问题的 System V 和 YUM 被迫淡出历史舞台，这让我不禁想起 IT 从业者的一句老话"为何要修复没有损坏的东西？ (Why fix, If not broken?) "。

现在，这篇文章结束了。我们真诚的期盼您能在下面的评论区留下您的宝贵意见和想法。如果你觉得这篇文章不错的话，那就点个赞吧~

原文链接: http://www.tecmint.com/dnf-commands-for-fedora-rpm-package-management/

Linux Story 翻译链接:  http://www.linuxstory.org/dnf-commands-for-fedora-rpm-package-management