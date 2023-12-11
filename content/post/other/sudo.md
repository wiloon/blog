---
title: su, sudo
author: "-"
date: 2012-06-23T01:59:43+00:00
url: sudo
categories:
  - Linux
tags:
  - reprint
---
## su, sudo

## sudo 提供密码

```bash
echo 'password' | sudo -S command
```

```bash
#!/bin/bash
sudo -S apt-get update << EOF 
你的密码
EOF

```

-S 参数的作用
使用 man 命令查询 sudo，对参数 -S 的说明如下：

Write the prompt to the standard error and read the password from the standard input instead of using the terminal device. The password must be followed by a newline character.

可见加上 -S 参数 sudo 才会从标准输入中读取密码，不加 -S 参数以上命令将起不到作用

[https://askubuntu.com/questions/470383/how-to-avoid-being-prompted-for-a-password-by-sudo](https://askubuntu.com/questions/470383/how-to-avoid-being-prompted-for-a-password-by-sudo)

### sudo 免密码

```bash
sudo visudo
wiloon ALL=(ALL) NOPASSWD: ALL
```

注意： 有的时候你的将用户设了 `nopasswd`，但是不起作用，原因是被后面的group的设置覆盖了，需要把group的设置也改为 `nopasswd`。

```bash
joe ALL=(ALL) NOPASSWD: ALL
%admin ALL=(ALL) NOPASSWD: ALL
```

[https://www.cnblogs.com/itech/archive/2009/08/07/1541017.html](https://www.cnblogs.com/itech/archive/2009/08/07/1541017.html)

[https://askubuntu.com/questions/70534/what-are-the-differences-between-su-sudo-s-sudo-i-sudo-su](https://askubuntu.com/questions/70534/what-are-the-differences-between-su-sudo-s-sudo-i-sudo-su)

### This account is currently not available

比如我是 su kafka的时候出现的问题
用vi看看 kafka的帐号信息
    cat /etc/passwd | grep kafka
发现它的shell是“/sbin /nologin”，需要将起改成“/bin/bash”
    vipw /etc/passwd
修改完毕后，保存退出

sudo(substitute user do) 使得系统管理员可以授权特定用户或用户组作为 root 或他用户执行某些 (或所有) 命令，同时还能够对命令及其参数提供审核跟踪。

用户可以选择用 su 切换到 root 用户运行命令，但是这种方式会启动一个 root shell 并允许用户运行之后的所有的命令。而 sudo 可以针对单个命令、仅在需要时授予临时权限，减少因为执行错误命令损坏系统的可能性。sudo 也能以其他用户身份执行命令并且记录用户执行的命令，以及失败的权限申请。

环境变量继承
  
```bash
sudo visudo
```

或者
  
# vi /etc/sudoers 在Defaults env_keep添加JAVA_HOME和PATH就可以继承下来已有的环境变量了。

或者

1.编辑/etc/sudoers文件把Defaults env_reset改成Defaults !env_reset

2.编辑.bashrc,最后添加alias sudo='sudo env PATH=$PATH'

附: sudo应用简介以及sudoers

sudo是linux下常用的允许普通用户使用超级用户权限的工具。
  
它的主要配置文件是sudoers,linux下通常在/etc目录下，如果是solaris，缺省不装sudo的，编译安装后通常在安装目录的etc目录下，不过不管sudoers文件在哪儿，sudo都提供了一个编辑该文件的命令: visudo来对该文件进行修改。强烈推荐使用该命令修改 sudoers，因为它会帮你校验文件配置是否正确，如果不正确，在保存退出时就会提示你哪段配置出错的。
  
言归正传，下面介绍如何配置sudoers
  
首先写sudoers的缺省配置:
  
#############################################################

# sudoers file

#

# This file MUST be edited with the 'visudo' command as root

#

# See the sudoers man page for the details on how to write a sudoers file

#

# Host alias specification

# User alias specification

# Cmnd alias specification

# Defaults specification

# User privilege specification

root ALL=(ALL) ALL

# Uncomment to allow people in group wheel to run all commands

# %wheel ALL=(ALL) ALL

# Same thing without a password

# Samples

# %users ALL=/sbin/mount /cdrom,/sbin/umount /cdrom

# %users localhost=/sbin/shutdown -h now

##################################################################
  
1. 最简单的配置，让普通用户support具有root的所有权限
  
执行visudo之后，可以看见缺省只有一条配置:
  
root ALL=(ALL) ALL
  
那么你就在下边再加一条配置:
  
support ALL=(ALL) ALL
  
这样，普通用户support就能够执行root权限的所有命令
  
以support用户登录之后，执行:
  
sudo su –
  
然后输入support用户自己的密码，就可以切换成root用户了
  
2. 让普通用户support只能在某几台服务器上，执行root能执行的某些命令
  
首先需要配置一些Alias，这样在下面配置权限时，会方便一些，不用写大段大段的配置。Alias主要分成4种
  
Host_Alias
  
Cmnd_Alias
  
User_Alias
  
Runas_Alias
  
1) 配置Host_Alias: 就是主机的列表
  
Host_Alias HOST_FLAG = hostname1, hostname2, hostname3
  
2) 配置Cmnd_Alias: 就是允许执行的命令的列表
  
Cmnd_Alias COMMAND_FLAG = command1, command2, command3
  
3) 配置User_Alias: 就是具有sudo权限的用户的列表
  
User_Alias USER_FLAG = user1, user2, user3
  
4) 配置Runas_Alias: 就是用户以什么身份执行 (例如root，或者oracle) 的列表
  
Runas_Alias RUNAS_FLAG = operator1, operator2, operator3
  
5) 配置权限
  
配置权限的格式如下:
  
USER_FLAG HOST_FLAG=(RUNAS_FLAG) COMMAND_FLAG

配置示例:
  
############################################################################

# sudoers file

#

# This file MUST be edited with the 'visudo' command as root

#

# See the sudoers man page for the details on how to write a sudoers file

#

# Host alias specification

Host_Alias EPG = 192.168.1.1, 192.168.1.2

# User alias specification

# Cmnd alias specification

Cmnd_Alias SQUID = /opt/vtbin/squid_refresh, /sbin/service, /bin/rm

# Defaults specification

# User privilege specification

root ALL=(ALL) ALL

# Uncomment to allow people in group wheel to run all commands

# %wheel ALL=(ALL) ALL

# Same thing without a password

# %wheel ALL=(ALL) NOPASSWD: ALL

# Samples

# %users ALL=/sbin/mount /cdrom,/sbin/umount /cdrom

# %users localhost=/sbin/shutdown -h now

###############################################################
  
我们不可以使用su让他们直接变成root，因为这些用户都必须知道root的密码，这种方法很不安全，而且也不符合我们的分工需求。一般的做法是利用权限的设置，依工作性质分类，让特殊身份的用户成为同一个工作组，并设置工作组权限。例如: 要wwwadm这位用户负责管理网站数据，一般Apache Web Server的进程httpd的所有者是www，您可以设置用户wwwadm与www为同一工作组，并设置Apache默认存放网页目录 /usr/local/httpd/htdocs的工作组权限为可读、可写、可执行，这样属于此工作组的每位用户就可以进行网页的管理了。
  
但这并不是最好的解决办法，例如管理员想授予一个普通用户关机的权限，这时使用上述的办法就不是很理想。这时您也许会想，我只让这个用户可以以 root身份执行shutdown命令就行了。完全没错，可惜在通常的Linux系统中无法实现这一功能，不过已经有了工具可以实现这样的功能—— sudo。
  
sudo通过维护一个特权到用户名映射的数据库将特权分配给不同的用户，这些特权可由数据库中所列的一些不同的命令来识别。为了获得某一特权项，有资格的用户只需简单地在命令行输入sudo与命令名之后，按照提示再次输入口令 (用户自己的口令，不是root用户口令) 。例如，sudo允许普通用户格式化磁盘，但是却没有赋予其他的root用户特权。
  
1. sudo工具由文件/etc/sudoers进行配置，该文件包含所有可以访问sudo工具的用户列表并定义了他们的特权。一个典型的/etc/sudoers条目如下:
  
代码:
  
liming ALL=(ALL) ALL
  
这个条目使得用户liming作为超级用户访问所有应用程序，如用户liming需要作为超级用户运行命令，他只需简单地在命令前加上前缀sudo。因此，要以root用户的身份执行命令format，liming可以输入如下命令:
  
代码:

# sudo /usr/sbin/useradd sam

注意: 命令要写绝对路径，/usr/sbin默认不在普通用户的搜索路径中，或者加入此路径: PATH=$PATH:/usr/sbin;export PATH。另外，不同系统命令的路径不尽相同，可以使用命令"whereis 命令名"来查找其路径。
  
这时会显示下面的输出结果:
  
代码:
  
We trust you have received the usual lecture from the local System
  
Administrator. It usually boils down to these two things:
  
# 1) Respect the privacy of others.
  
# 2) Think before you type.
  
Password:
  
如果liming正确地输入了口令，命令useradd将会以root用户身份执行。
  
注意: 配置文件/etc/sudoers必须使用命令 Visudo来编辑。
  
只要把相应的用户名、主机名和许可的命令列表以标准的格式加入到文件/etc/sudoers，并保存就可以生效，再看一个例子。
  
2. 例子: 管理员需要允许gem用户在主机sun上执行reboot和shutdown命令，在/etc/sudoers中加入:
  
代码:
  
gem sun=/usr/sbin/reboot，/usr/sbin/shutdown
  
注意: 命令一定要使用绝对路径，以避免其他目录的同名命令被执行，从而造成安全隐患。
  
然后保存退出，gem用户想执行reboot命令时，只要在提示符下运行下列命令:
  
代码:
  
$ sudo /usr/sbin/reboot
  
输入正确的密码，就可以重启服务器了。
  
如果您想对一组用户进行定义，可以在组名前加上%，对其进行设置，如:
  
代码:
  
%cuug ALL=(ALL) ALL
  
3. 另外，还可以利用别名来简化配置文件。别名类似组的概念，有用户别名、主机别名和命令别名。多个用户可以首先用一个别名来定义，然后在规定他们可以执行什么命令的时候使用别名就可以了，这个配置对所有用户都生效。主机别名和命令别名也是如此。注意使用前先要在/etc/sudoers中定义:  User_Alias, Host_Alias, Cmnd_Alias项，在其后面加入相应的名称，也以逗号分隔开就可以了，举例如下:
  
代码:
  
Host_Alias SERVER=no1
  
User_Alias ADMINS=liming，gem
  
Cmnd_Alias SHUTDOWN=/usr/sbin/halt，/usr/sbin/shutdown，/usr/sbin/reboot
  
ADMINS SERVER=SHUTDOWN

5. sudo命令还可以加上一些参数，完成一些辅助的功能，如
  
代码:
  
$ sudo –l
  
会显示出类似这样的信息:
  
代码:
  
User liming may run the following commands on this host:
  
(root) /usr/sbin/reboot
  
说明root允许用户liming执行/usr/sbin/reboot命令。这个参数可以使用户查看自己目前可以在sudo中执行哪些命令。
  
6. 在命令提示符下键入sudo命令会列出所有参数，其他一些参数如下:
  
代码:
  
-V 显示版本编号。
  
-h 显示sudo命令的使用参数。
  
-v 因为sudo在第一次执行时或是在N分钟内没有执行 (N预设为5) 会询问密码。这个参数是重新做一次确认，如果超过N分钟，也会问密码。
  
-k 将会强迫使用者在下一次执行sudo时询问密码 (不论有没有超过N分钟) 。
  
-b 将要执行的命令放在背景执行。
  
-p prompt 可以更改问密码的提示语，其中%u会替换为使用者的账号名称，%h会显示主机名称。
  
-u username/#uid 不加此参数，代表要以root的身份执行命令，而加了此参数，可以以username的身份执行命令 (#uid为该username的UID) 。
  
-s 执行环境变量中的 SHELL 所指定的 Shell ，或是 /etc/passwd 里所指定的 Shell。
  
-H 将环境变量中的HOME (宿主目录) 指定为要变更身份的使用者的宿主目录。 (如不加-u参数就是系统管理者root。)
  
要以系统管理者身份 (或以-u更改为其他人) 执行的命令

## is not in the sudoers file

首需要切换到root身份
  
$su -
  
(注意有- ，这和su是不同的，在用命令"su"的时候只是切换到root，但没有把root的环境变量传过去，还是当前用户的环境变量，用"su -"命令将环境变量也一起带过去，就象和root登录一样)

然后
  
visudo //切记，此处没有vi和sudo之间没有空格
  
或 emacs /etc/sudoers
  
1. 移动光标，到最后一行
  
2. 按a，进入append模式
  
3. 输入
  
your_user_name ALL=(ALL) ALL
  
4. 按Esc
  
5. 输入":w"(保存文件)
  
6. 输入":q"(退出)

原文地址: [http://kenshin54.iteye.com/blog/941896](http://kenshin54.iteye.com/blog/941896)
  
[https://wiki.archlinux.org/index.php/Sudo_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87](https://wiki.archlinux.org/index.php/Sudo_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
