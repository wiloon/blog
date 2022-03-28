---
title: 文件存储和删除的底层过程
author: "-"
date: 2015-04-23T02:28:19+00:00
url: /?p=7485
categories:
  - Uncategorized
tags:
  - Office

---
## 文件存储和删除的底层过程

>https://blog.csdn.net/MyySophia/article/details/107696414

当a.txt文件要存储到/tmp下时：

(1).首先从inode table中找一个空闲的inode号分配给a.txt，例如2222。再将inode map(imap)中2222这个inode号标记为已使用。
(2).在/tmp的data block中添加一条a.txt文件的记录。该记录中包括一个指向inode号的指针，例如"0x2222"。
(3).然后从block map(bmap)中找出空闲的data block，并开始将a.txt中的数据写入到data block中。每写一段空间(ext4每次分配一段空间)就从bmap中找一次空闲的data block，直到存完所有数据。
(4).设置inode table中关于2222这条记录的data block指针，通过该指针可以找到a.txt使用了哪些data block。
当要删除a.txt文件时：

(1).在inode table中删除指向a.txt的data block指针。这里只要一删除，外界就找不到a.txt的数据了。但是这个文件还存在，只是它是被"损坏"的文件，因为没有任何指针指向数据块。
(2).在imap中将2222的inode号标记为未使用。于是这个inode号就被释放，可以被后续的文件重用。
(3).删除父目录/tmp的data block中关于a.txt的记录。这里只要一删除，外界就看不到也找不到这个文件了。
(4).在bmap中将a.txt占用的block标记为未使用。这里被标记为未使用后，这些data block就可以被后续文件覆盖重用。
考虑一种情况，当一个文件被删除时，但此时还有进程在使用这个文件，这时是怎样的情况呢？外界是看不到也找不到这个文件的，所以删除的过程已经进行到了第(3)步。但进程还在使用这个文件的数据，也能找到这个文件的数据，是因为进程在加载这个文件的时候就已经获取到了该文件占用哪些data block，虽然删除了文件，但bmap中这些data block还没有标记为未使用。



>https://zhuanlan.zhihu.com/p/110943226

