---
title: 文件存储和删除的过程
author: "-"
date: 2015-04-23T02:28:19+00:00
url: file/create/delete
categories:
  - filesystem
tags:
  - file

---
## 查找文件

通过文件名打开文件时，通过文件名先找到对应的inode，然后通过inode找到文件内容所在的block来读取数据。

## 文件存储和删除的过程

[https://blog.csdn.net/MyySophia/article/details/107696414](https://blog.csdn.net/MyySophia/article/details/107696414)

## 创建文件 /tmp/a.txt

1. 首先从 inode table 中找一个空闲的 inode 号分配给 a.txt，例如 2222。再将 inode map(imap) 中 2222 这个 inode 标记为已使用。
2. 在 /tmp 的 data block 中添加一条 a.txt 文件的记录。该记录中包括一个指向 inode 的指针，例如 "0x2222"。
3. 然后从 block map (bmap) 中找出空闲的 data block，并开始将 a.txt 中的数据写入到 data block 中。每写一段空间 ( ext4 每次分配一段空间 ) 就从 bmap 中找一次空闲的 data block, 直到存完所有数据。
4. 设置 inode table 中关于 2222 这条记录的 data block 指针, 通过该指针可以找到 a.txt 使用了哪些 data block。

## 删除文件的过程 /tmp/a.txt

1. 在 inode table 中删除指向 a.txt 的 data block 指针。这里只要一删除，外界就找不到 a.txt 的数据了。但是这个文件还存在，只是它是被"损坏"的文件，因为没有任何指针指向数据块。
2. 在 imap 中将 2222 的 inode 标记为未使用。于是这个 inode 就被释放，可以被后续的文件重用。
3. 删除父目录 /tmp 的 data block 中关于 a.txt 的记录。 这里只要一删除，外界就看不到也找不到这个文件了。
4. 在 bmap 中将 a.txt 占用的 block 标记为未使用。这里被标记为未使用后，这些 data block 就可以被后续文件覆盖重用。

考虑一种情况，当一个文件被删除时，但此时还有进程在使用这个文件，这时是怎样的情况呢？外界是看不到也找不到这个文件的，所以删除的过程已经进行到了第 3 步。但进程还在使用这个文件的数据，也能找到这个文件的数据，是因为进程在加载这个文件的时候就已经获取到了该文件占用哪些 data block，虽然删除了文件，但 bmap 中这些 data block 还没有标记为未使用。

[https://zhuanlan.zhihu.com/p/110943226](https://zhuanlan.zhihu.com/p/110943226)
