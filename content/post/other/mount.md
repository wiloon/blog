---
title: mount, umount
author: "-"
date: 2011-12-03T08:52:06+00:00
url: /?p=1693
categories:
  - inbox
tags:
  - reprint
---
## mount, umount
### commands
    pacman -S nfs-utils
    showmount -e 192.168.50.227
    mount -t nfs 192.168.50.227:/data1t /mnt/nas

### mount iso

```bash
sudo mkdir /mnt/iso
sudo mount -o loop /path/to/my-iso-image.iso /mnt/iso
ls -l /mnt/iso/
sudo umount /mnt/iso/
```

mount 和 umount 命令
  
现在，文件系统已经创建成功，您应该挂载分区了。挂载文件系统的命令是 mount，其语法是: 

```bash
mount [选项]  [-o 挂载选项]
```

在本例中，我们首先会将分区临时挂载在 /mnt (或您选择的任何其它挂载点: 请记住，挂载点必须已经存在)。挂载我们新创建的分区的命令是: 

```bash
mount -t ext3 /dev/hdb1 /mnt
```

-t 选项用于指定分区上文件系统的类型。您最常遇到的文件系统应该是 ext2(GNU/Linux 文件系统)或 ext3(改进了日志性能的 ext2FS)，vfat (适用于所有 DOS/Windows® 分区: FAT 12, 16 or 32)以及 ISO9660(CD-ROM 文件系统), ntfs.

如果您不指定任何类型，mount 将会试着读取分区中的超块来猜测文件系统。

-o 选项用于指定一个或多个挂载选项。可供选择的选项视文件系统类型不同而有所不同。请参看 mount(8) 手册页中的细节。

现在，您已经挂载了您的新分区，现在该将整个 /usr 目录复制到新分区了: 

$ (cd /usr && tar cf - .) | (cd /mnt && tar xpvf -)
  
文件都已经复制完了，现在可以卸下分区了。要卸下分区，请使用 umount 命令。语法很简单: 

### umount
  
所以，要卸下我们的新分区，应该输入: 

$ umount /mnt
  
或者: 

$ umount /dev/hdb1
  
提示
  
有些时候，可能某些设备(通常是 CD-ROM)正忙或无法响应。此时，大多数用户的解决办法是重新启动计算机。我们大可不必这么做。例如，如果 umount /dev/hdc 失败的话，您可以试试"lazy" umount。语法十分简单: 

umount -l
  
此命令将会断开设备并关闭打开该设备的全部句柄。通常，您可以使用 eject命令弹出碟片。所以，如果 eject 命令失效而您又不想重新启动，请使用 lazy umount。

由于分区即将成为我们的 /usr 目录，我们现在需要通知系统。要完成这一操作，我们应该编辑 /etc/fstab 文件。该文件可使得系统在启动时自动挂载特定的文件系统。组成该文件的每一行分别描述了一组挂载关系，这其中包括文件系统、挂载点以及其它选项。这里是该文件的一个例子: 

/dev/hda1 / ext2 defaults 1 1
  
/dev/hda5 /home ext2 defaults 1 2
  
/dev/hda6 swap swap defaults 0 0
  
none /mnt/cdrom supermount dev=/dev/scd0,fs=udf:iso9660,ro,- 0 0
  
none /mnt/floppy supermount dev=/dev/fd0,fs=ext2:vfat,-,sync,umask=0 0 0
  
none /proc proc defaults 0 0
  
none /dev/pts devpts mode=0622 0 0
  
每行都由以下内容组成: 

文件系统所在的设备；

挂载点；

文件系统类型；

挂载选项；

dump 工具备份标志；

fsck(文件系统检查(FileSystem ChecK))的检查顺序。

总是有一行说明了根文件系统。swap 分区是一种特殊的分区，因为您无法在树形结构中找到其对应位置，而且这些分区的挂载点域只写着 swap 关键字。至于 /proc 文件系统，我们会在第 10 章 /proc 文件系统中有更详细的描述。另外一种特殊的文件系统是 /dev/pts。

在这里，我们需要将整个 /usr 层次移至 /dev/hdb1，并且想要在启动时将此分区挂载为 /usr。要达到这一目的，应该在 /etc/fstab 文件中添加下面一行: 

/dev/hdb1 /usr ext2 defaults 1 2
  
现在，分区将会在每次启动时自动挂载，并且必要时检查错误。

现在我们来介绍两个特殊选项: noauto 和 user。noauto 选项指定了文件系统不应该在启动时挂载，而只应该在您想要挂载的时候才挂载。而 user 选项指定了任何用户都可以挂载或卸下文件系统。这两个选项通常用于 CD-ROM 和软盘驱动器。有关 /etc/fstab 中其它选项的详情，请您查看 fstab(5) 手册页。

使用 /etc/fstab 的好处在于，它将极大简化 mount 命令的语法。要挂载文件中描述的文件系统，您只需要引用挂载点或设备。要挂载软盘，您可以只输入: 

$ mount /mnt/floppy
  
或: 

$ mount /dev/fd0
  
在分区转移这个例子的最后，我们来看看我们都做了什么。我们将 /usr 层次复制到了新分区，然后修改了 /etc/fstab，这样新分区就会在启动时自动挂载。这样似乎已经大功告成了。且慢，还有一个问题。老 /usr 中的文件仍然留在驱动器中原来的地方，我们还需要将它们删除以便腾出空间(这个才是我们最初的目标)。在执行接下来的命令之前，您需要先切换到单用户模式，请在命令行上执行 telinit 1 命令。

接下来，我们将会删除 /usr 目录中的全部文件。请记住，我们仍然是指"老"目录，因为新的大目录尚未挂载。rm -Rf /usr/*。

最后，我们需要挂载新的 /usr 目录: mount /usr/。

这样才是真正完成了我们最初的目标。现在，让我们回到多用户模式中(telinit 3 代表标准的文本模式，telinit 5 代表 X Window 系统)。如果没有后续的管理工作要做的话，您就可以从 root 账户注销了。
  
https://xionchen.github.io/2016/08/25/linux-bind-mount/