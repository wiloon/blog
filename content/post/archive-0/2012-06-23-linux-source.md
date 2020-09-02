---
title: Linux source
author: wiloon
type: post
date: 2012-06-23T01:52:30+00:00
url: /?p=3635
categories:
  - Linux

---
source命令：

<div id="article_content">
  
    source是bash的内置命令，不需要（也没有）绝对路径.
  
  
    source命令也称为“点命令”，也就是一个点符号（.）。source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。
  
  
    用法：
  
  
    source filename 或 . filename
  
  
    source命令除了上述的用途之外，还有一个另外一个用途。在对编译系统核心时常常需要输入一长串的命令，如：
  
  
    make mrproper
  
  
    make menuconfig
  
  
    make dep
  
  
    make clean
  
  
    make bzImage
  
  
    …………
  
  
    如果把这些命令做成一个文件，让它自动顺序执行，对于需要多次反复编译系统核心的用户来说会很方便，而用source命令就可以做到这一点，它的作用就是把一个文件的内容当成shell来执行，先在linux的源代码目录下（如/usr/src/linux-2.4.20）建立一个文件，如make_command，在其中输入一下内容：
  
  
    make mrproper &&
  
  
    make menuconfig &&
  
  
    make dep &&
  
  
    make clean &&
  
  
    make bzImage &&
  
  
    make modules &&
  
  
    make modules_install &&
  
  
    cp arch/i386/boot/bzImage /boot/vmlinuz_new &&
  
  
    cp System.map /boot &&
  
  
    vi /etc/lilo.conf &&
  
  
    lilo -v
  
  
    文件建立好之后，每次编译核心的时候，只需要在/usr/src/linux-2.4.20下输入：
  
  
    source make_command
  
  
    即可，如果你用的不是lilo来引导系统，可以把最后两行去掉，配置自己的引导程序来引导内核。
  
  
    顺便补充一点，&&命令表示顺序执行由它连接的命令，但是只有它之前的命令成功执行完成了之后才可以继续执行它后面的命令。
  
