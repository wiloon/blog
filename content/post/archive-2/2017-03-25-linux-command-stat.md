---
title: linux stat, 文件创建时间, 修改时间
author: wiloon
type: post
date: 2017-03-25T02:32:27+00:00
url: /?p=9935
categories:
  - Uncategorized

---
在windows下，一个文件有：创建时间、修改时间、访问时间。
  
而在Linux下，一个文件也有三种时间，分别是：访问时间、修改时间、状态改动时间。

两者有此不同，在Linux下没有创建时间的概念，也就是不能知道文件的建立时间，
  
如果文件建立后就没有修改过，修改时间=建立时间;
  
如果文件建立后，状态就没有改动过，那么状态改动时间=建立时间;
  
如果文件建立后，没有被读取过，那么访问时间=建立时间，因为不好判断文件是否被改过、读过、其状态是否变过，所以判断文件的建立时间基本上能为不可能。

如何查一个文件的三个时间呢？
  
先用下面的命令来建立一个文件

<pre><code class="language-shell line-numbers">date && echo "this is file be used test time of file" &gt;filetime.txt && ll --full-time filetime.txt
```

Tue Aug 4 15:13:44 HKT 2009
  
-rw-r–r– 1 root root 39 2009-08-04 15:13:44.000000000 +0800 filetime.txt

通过stat filename.txt来查，如：

# stat filetime.txt

File: \`filetime.txt’
  
Size: 39 Blocks: 8 IO Block: 4096 Regular File
  
Device: 802h/2050d Inode: 17 Links: 1
  
Access: (0644/-rw-r–r–) Uid: ( 0/ root) Gid: ( 0/ root)
  
Access: 2009-08-04 15:13:44.000000000 +0800
  
Modify: 2009-08-04 15:13:44.000000000 +0800
  
Change: 2009-08-04 15:13:44.000000000 +0800

说明：Access访问时间(存取时间)。Modify修改时间。Change状态改动时间。可以stat *查看这个目录所有文件的状态。
  
ctime=change time
  
atime=access time
  
mtime=modifiy time

因为这是一个新的文件（filetime.txt），没做过内容、属性的更改，也没读过这个文件，所以三者（访问时间、修改时间、状态改动时间）的时间是一致的，这时文件的修改时间与这三个时间是一样的，是没有疑问的。

1、访问时间，读一次这个文件的内容，这个时间就会更新。比如对这个文件运用 more、cat等命令。ls、stat命令都不会修改文件的访问时间。
  
2、修改时间，修改时间是文件内容最后一次被修改时间。比如：vi后保存文件。ls -l列出的时间就是这个时间。
  
3、状态改动时间。是该文件的inode最后一次被修改的时间，通过chmod、chown命令修改一次文件属性，这个时间就会更新。

另个除了可以通过stat来查看文件的mtime,ctime,atime等属性，也可以通过ls命令来查看，具体如下:
  
ls -lc filename 列出文件的 ctime （最后更改时间）
  
ls -lu filename 列出文件的 atime（最后存取时间）
  
ls -l filename 列出文件的 mtime （最后修改时间）

在linux中stat函数中，用st\_atime表示文件数据最近的存取时间(last accessed time)；用st\_mtime表示文件数据最近的修改时间(last modified time)；使用st_ctime表示文件inode数据最近的修改时间(last i-node’s status changed time)。

字段 说明 例子 ls(-l)
  
st_atime 文件数据的最后存取时间 read,cat -u
  
st_mtime 文件数据的最后修改时间 write,vi 缺省
  
st_ctime 文件数据的最后更改时间 chown,chmod,vi -c

在linux系统中，系统把文件内容数据与inode数据是分别存放的，inode存放了文件权限与文件属主之类的数据。

coreutils 8.31 stat 命令已经支持创建时间了。
  
ext4、xfs、btrfs 都支持创建时间
  
内核已经通过 4.11 版本引入的 statx 系统调用支持获取创建时间了。
  
http://blog.sina.com.cn/s/blog_605f5b4f01015k56.html

<blockquote class="wp-embedded-content" data-secret="0aBZM4XyiK">
  
    <a href="https://man.linuxde.net/stat">stat</a>
  
</blockquote>

<iframe title="《stat》—Linux命令大全" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://man.linuxde.net/stat/embed#?secret=0aBZM4XyiK" data-secret="0aBZM4XyiK" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
  
https://blog.lilydjwg.me/2018/7/11/get-file-birth-time-in-linux.213101.html