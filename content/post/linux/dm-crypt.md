---
author: "-"
date: "2021-03-30 13:27:18" 
title: "dm-crypt, 加密"

categories:
  - inbox
tags:
  - reprint
---
## "dm-crypt, 加密"

### 用 cryptsetup 创建 LUKS 的虚拟加密盘 (逻辑卷) 
在前一个章节，已经介绍了"对物理分区的加密"。其实 cryptsetup 也可以支持虚拟加密盘 (逻辑加密盘) ——类似于 TrueCrypt 那样。  
### 何为"虚拟加密盘"
考虑到某些读者没有看过《TrueCrypt 使用经验[1]: 关于加密算法和加密盘的类型》，俺再次唠叨一下: 所谓的"虚拟加密盘"，就是说这个盘并【不是】对应物理分区，而是对应一个虚拟分区 (逻辑卷) 。这个虚拟分区，说白了就是一个大文件。虚拟分区有多大，这个文件就有多大。  
"虚拟加密盘"的一个主要好处在于——可以拷贝复制。比如你可以在不同的机器之间复制这个虚假分区对应的大文件。甚至可以把这个大文件上传到云端 (网盘) 进行备份——这么干的好处参见《文件备份技巧: 组合"虚拟加密盘"与"网盘"》。  

### 创建一个文件作为容器
下面用 dd 命令创建 1GB (1024MB) 的大文件，该文件位于 /root/luks.vol 路径。当然，你也可以指定其它的文件大小或其它的文件路径。
```bash
dd if=/dev/zero of=/root/luks.vol bs=1M count=1024
```
 (dd 命令是一个牛逼命令，之前在《如何用 ISO 镜像制作 U 盘安装盘 (通用方法、无需 WinPE) 》介绍过该命令) 

经某个热心读者提醒，还可以使用 fallocate 命令创建容器文件。对于特别大的容器文件，性能【高于】dd 命令。
以下示例通过 fallocate 【瞬间】创建一个 64GB 的大文件。

```bash
fallocate -l 64G /root/luks.vol
```

### 用 LUKS 方式加密 (格式化) 该文件容器
使用前面章节提及的参数，对上述文件容器进行加密。得到一个虚拟的加密盘.提示 are you sure时,输入 大写的 YES

    cryptsetup --cipher aes-xts-plain64 --key-size 512 --hash sha512 --iter-time 10000 luksFormat /root/luks.vol

### 打开加密之后的文件容器
使用如下命令打开上述的文件容器，使用的映射名是 xxx (你也可以改用其它单词) 。

    cryptsetup luksOpen /root/luks.vol xxx

打开之后，该虚拟盘会被映射到 /dev/mapper/xxx
你可以用如下命令看到: 

    ls /dev/mapper/

### 创建文件系统
由于加密盘已经打开并映射到 /dev/mapper/xxx 你可以在 /dev/mapper/xxx 之上创建文件系统。命令如下 (文件系统类型以 ext4 为例) 

    mkfs.ext4 /dev/mapper/xxx

### 挂载文件系统
创建完文件系统之后，你还需要挂载该文件系统，才能使用它。挂载的步骤如下。
首先，你要先创建一个目录，作为【挂载点】。俺把"挂载点"的目录设定为 /mnt/xxx (当然，你可以用其它目录作为挂载点) 。

    mkdir /mnt/xxx

创建好"挂载点"对应的目录，下面就可以进行文件系统的挂载。

    mount /dev/mapper/xxx /mnt/xxx

挂载好文件系统，用如下命令查看，就可以看到你刚才挂载的文件系统。

    df -hT

接下来，你就可以通过 /mnt/xxx 目录去访问该文件系统。当你往 /mnt/xxx 下面创建下级目录或下级文件，这些东西将被存储到该虚拟加密盘上。

### 退出
当你使用完，要记得退出。包括下面两步: 
卸载文件系统

    sudo umount /mnt/xxx

关闭加密盘

    sudo cryptsetup close xxx

---

https://program-think.blogspot.com/2015/10/dm-crypt-cryptsetup.html