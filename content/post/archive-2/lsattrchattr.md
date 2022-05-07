---
title: lsattr, chattr, 管理文件和目录属性
author: "-"
date: 2017-08-01T07:23:08+00:00
url: lsattr
categories:
  - Inbox
tags:
  - reprint
---
## lsattr, chattr, 管理文件和目录属性

为了允许添加数据,防止更改或者删除等,文件和文件夹可以设定了特定的控制属性。例如,你可以在关键的系统文件或者文件夹中启用属性,然后没有任何用户,包括root,可以删除或者修改它,比如不允许使用像dump这样的命令等备份工具去备份一个特定的文件或者文件夹,等等。这些属性只可以在ext2,ext3或者ext4文件系统中的文件和文件夹上设定。

```bash
# 使用'i'属性使文件不可更改
chattr +i /etc/passwd /etc/shadow /etc/group /etc/gshadow
# 查看文件属性
lsattr /etc/passwd
# ----i----------- /etc/passwd

# 移除不可更改属性
chattr -i /etc/passwd /etc/shadow /etc/group /etc/gshadow

lsattr /etc/passwd
# ---------------- /etc/passwd

```

现在试着删除或者修改文件
  
[root@linuxtechi ~]# rm -f dummy_data
  
rm: cannot remove 'dummy_data': Operation not permitted
  
[root@linuxtechi ~]# echo "test" >> dummy_data
  
-bash: dummy_data: Permission denied

```bash
chattr -ai /etc/passed
```


  
     (总结) Linux的chattr与lsattr命令详解
  


http://www.ha97.com/5172.html/embed#?secret=D3gPzD1nWk

PS: 有时候你发现用root权限都不能修改某个文件,大部分原因是曾经用chattr命令锁定该文件了。chattr命令的作用很大,其中一些功能是由Linux内核版本来支持的,不过现在生产绝大部分跑的linux系统都是2.6以上内核了。通过chattr命令修改属性能够提高系统的安全性,但是它并不适合所有的目录。chattr命令不能保护/、/dev、/tmp、/var目录。lsattr命令是显示chattr命令设置的文件属性。

这两个命令是用来查看和改变文件、目录属性的,与chmod这个命令相比,chmod只是改变文件的读写、执行权限,更底层的属性控制是由chattr来改变的。

chattr命令的用法: chattr [ -RVf ] [ -v version ] [ mode ] files…
  
最关键的是在[mode]部分,[mode]部分是由+-=和[ASacDdIijsTtu]这些字符组合的,这部分是用来控制文件的
  
属性。

  * : 在原有参数设定基础上,追加参数。
  * : 在原有参数设定基础上,移除参数。
  
    = : 更新为指定参数设定。
  
    A: 文件或目录的 atime (access time)不可被修改(modified), 可以有效预防例如手提电脑磁盘I/O错误的发生。
  
    S: 硬盘I/O同步选项,功能类似sync。
  
    a: 即append,设定该参数后,只能向文件中添加数据,而不能删除,多用于服务器日志文件安全,只有root才能设定这个属性。
  
    c: 即compresse,设定文件是否经压缩后再存储。读取时需要经过自动解压操作。
  
    d: 即no dump,设定文件不能成为dump程序的备份目标。
  
    i: 设定文件不能被删除、改名、设定链接关系,同时不能写入或新增内容。i参数对于文件 系统的安全设置有很大帮助。
  
    j: 即journal,设定此参数使得当通过mount参数: data=ordered 或者 data=writeback 挂 载的文件系统,文件在写入时会先被记录(在journal中)。如果filesystem被设定参数为 data=journal,则该参数自动失效。
  
    s: 保密性地删除文件或目录,即硬盘空间被全部收回。
  
    u: 与s相反,当设定为u时,数据内容其实还存在磁盘中,可以用于undeletion。
  
    各参数选项中常用到的是a和i。a选项强制只可添加不可删除,多用于日志系统的安全设定。而i是更为严格的安全设定,只有superuser (root) 或具有CAP_LINUX_IMMUTABLE处理能力 (标识) 的进程能够施加该选项。

应用举例: 

1. 用chattr命令防止系统中某个关键文件被修改: 

# chattr +i /etc/resolv.conf

然后用mv /etc/resolv.conf等命令操作于该文件,都是得到Operation not permitted 的结果。vim编辑该文件时会提示W10: Warning: Changing a readonly file错误。要想修改此文件就要把i属性去掉:  chattr -i /etc/resolv.conf

# lsattr /etc/resolv.conf

会显示如下属性
  
--i--- /etc/resolv.conf

2. 让某个文件只能往里面追加数据,但不能删除,适用于各种日志文件: 

# chattr +a /var/log/messages

https://linux.cn/article-5590-1.html


  
     (总结) Linux的chattr与lsattr命令详解
  


http://www.ha97.com/5172.html/embed#?secret=D3gPzD1nWk