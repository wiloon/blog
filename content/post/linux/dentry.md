---
title: dentry
author: "-"
date: 2011-11-09T06:08:32+00:00
url: dentry
categories:
  - Linux
tags:
  - reprint
---
## dentry

上一节提到了，struct file并不是文件系统的核心数据结构，那么dentry和inode，这两个结构体谁是文件系统的核心数据结构呢，它们存在的目的又分别是什么呢？

首先dentry是目录项缓存，是一个存放在内存里的缩略版的磁盘文件系统目录树结构,他是directory entry的缩写。我们知道文件系统内的文件可能非常庞大，目录树结构可能很深，该树状结构中，可能存在几千万，几亿的文件。

首先假设不存在dentry这个数据结构，我们看下我们可能会面临什么困境：

比如我要打开/usr/bin/vim 文件， 1 首先需要去／所在的inode找到／的数据块，从／的数据块中读取到usr这个条目的inode， 2 跳转到user 对应的inode，根据/usr inode 指向的数据块，读取到/usr 目录的内容，从中读取到bin这个条目的inode 3 跳转到/usr/bin/对应的inode，根据/usr/bin/指向的数据块，从中读取到/usr/bin/目录的内容，从里面找到vim的inode

我们都知道，Linux提供了page cache页高速缓存，很多文件的内容已经缓存在内存里，如果没有dentry，文件名无法快速地关联到inode，即使文件的内容已经缓存在页高速缓存，但是每一次不得不重复地从磁盘上找出来文件名到VFS inode的关联。

因此理想情况下，我们需要将文件系统所有文件名到VFS inode的关联都纪录下来，但是这么做并不现实，首先并不是所有磁盘文件的inode都会纪录在内存中，其次磁盘文件数字可能非常庞大，我们无法简单地建立这种关联，耗尽所有的内存也做不到将文件树结构照搬进内存

>https://bean-li.github.io/vfs-inode-dentry/
