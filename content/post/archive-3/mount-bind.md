---
title: mount --bind
author: "-"
date: 2020-02-11T01:31:18+00:00
url: /?p=15511
categories:
  - Inbox
tags:
  - reprint
---
## mount --bind

[https://xionchen.github.io/2016/08/25/linux-bind-mount/](https://xionchen.github.io/2016/08/25/linux-bind-mount/)

The bind mounts
  
bind 是 mount 中比较特殊的用法之一，这里对一些例子进行分析和实验

bind 的意思是，把其他地方的子树再进行挂载，也就是说可以把文件系统中的某一个部分进行挂载。这个特性是从 linux2.4.0 开始的。
  
或者更简单的说,就是挂载一个已有的文件夹

常见使用场景
  
在做一些 chroot 的操作的时候, 我们希望把当前的文件系统的一个目录(例如/dev) 出现在 chroot 的目录下.
  
但是又不希望 chroot 对这个目录进行更改, 我们该怎么做呢?

首先, 我们可以使用 mount --bind 将 /dev 目录挂载到 chroot 的目录下:

```bash
mount --bind /dev $chrootdir/dev
```
  
这样, 我们从chroot的目录和自己本身的文件系统的目录就都可以访问/dev目录.

不过有时我们不希望挂载的目录是可以修改的.
  
那么,可以通过下面的命令将挂载的属性设置为 readonly 的这样就实现了上述的要求

```bash
mount -o remount,ro,bind /dev $chrootdir/dev
```
  
最基础的用法的如下
  
```bash
mount --bind olddir newdir
```
  
如果执行了上面这个命令，在 olddir 和 newdir 都可以访问相同的内容，并且如果对其中一个目录内的内容进行了修改，在另一个目录会有相同的显示。

下面的命令可以创建一个挂载点
  
```bash
mount --bind foo foo
```
  
在挂载后可以通过 mount 命令查看所有的挂载点

如果要递归的挂载一个目录可以使用如下命令
  
```bash
mount -rbind olddir newdir
```
  
递归的挂载是指如果挂载的 olddir 内有挂载点，会把这个挂载点也一起挂载到 newdir 下。

-–bind可 以支持一些选项
  
例如: 挂载一个目录。并且让他是只读的:

```bash
mount --bind olddir newdir
```
  
```bash
mount -o remount,ro,bind olddir newdir
```
  
在使用 -o 的时候，是对一个已经挂载的

这样在新的目录中的内容是无法更改的，老的目录依然是可以修改的。
