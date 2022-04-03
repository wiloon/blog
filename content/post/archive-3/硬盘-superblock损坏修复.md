---
title: SuperBlock, 超级块
author: "-"
date: 2020-01-11T09:30:24+00:00
url: Superblock
categories:
  - linux
tags:
  - reprint
---
## Superblock, 超级块

A superblock is a record of the characteristics of a filesystem, including its size, the block size, the empty and the filled blocks and their respective counts, the size and location of the inode tables, the disk block map and usage information, and the size of the block groups.

Superblock 记录整个文件系统的整体信息，包括inode与数据块的总量，使用量，剩余量，以及文件系统的格式和相关信息，每个block group中都可能包含了superblock，但是除了第1个Primary superblock有用外，其它的superblock作为第1个superblock的备份，称呼为Backup superblock。

>http://www.linfo.org/superblock

## 硬盘 SuperBlock 损坏修复
### 找到super block 备份

```bash
#查看文件系统备份Superblock
mke2fs -n /dev/sdb
#查看文件系统备份Superblock
dumpe2fs /dev/sdb1 | grep --before-context=1 superblock

arch# dumpe2fs /dev/sdb1 | grep --before-context=1 superblock
dumpe2fs 1.45.5 (07-Jan-2020)
Group 0: (Blocks 0-32767) csum 0xb451 [ITABLE_ZEROED]
  Primary superblock at 0, Group descriptors at 1-38
--
Group 1: (Blocks 32768-65535) csum 0x5489 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 32768, Group descriptors at 32769-32806
--
Group 3: (Blocks 98304-131071) csum 0x2257 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 98304, Group descriptors at 98305-98342
--
Group 5: (Blocks 163840-196607) csum 0x57e3 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 163840, Group descriptors at 163841-163878
--
Group 7: (Blocks 229376-262143) csum 0xcfeb [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 229376, Group descriptors at 229377-229414
...
```

从上面操作可以看出，在第1、3、4、7、9这几个Block Group上存放有superblock备份

```bash
fsck -b 8193 /dev/sdb1
e2fsck -b 214990848 -y /dev/sdb
```

当你的系统出现 superblock corrupt 而无法启动时: 
  
1.用应急盘启动,先看fdisk的结果.如果你的分区表看起来正常,那么恢复的可能性就比较大,如果出现cannot open /dev/sda2的提示,那么想一想你的scsi卡启动没有,如果没有,那么你可以试着用小红帽的安装光盘启动,记住,仅仅是看分区表,千万不要写它.然后把分区情况详细记录下来.

2.试着e2fsck /dev/hda2,(先不要加-p -y 之类的参数,)用手动进行修复,同时也可以了解具体是文件系统的那些地方损坏了,如果你的运气好,e2fsck过去了,/dev/hda2已经基本修复,当然修复的可能是99.9%,也可能是99%这就看文件系统的损坏程度乐,不过现在可以说你的数据已经都找回来了.剩下的事就是mount上把数据备份出来以防万一.

3.如果e2fsck没过去(确保你的硬盘已经正确驱动乐),也不要着急,因为 superblock 在硬盘中有很多地方有备份,现在你最好把硬盘卸下来挂到另一个好的linux系统上,当然同样要保证硬盘被正确驱动乐.先用e2fsck /dev/hda2,如果结果和前面一样，就用e2fsck -b xxx -f /dev/hda2, xxx是硬盘上 superblock 的备份块,xxx=n*8192+1,n=1,2,3...一般来讲,如果系统瘫痪的真正原因是superblock损坏，这种办法就应该可以恢复你的数据了。如果执行后的结果还是不能通过,那么往下一步.

4.利用dd命令.先dd if=/dev/hda2 of=/tmp/rescue conv=noerror(/tmp/rescue是一个文件),把重要的数据拷出来,当然,这个盘要比你损坏的盘大一点,否则拷不下.另外,上面的dd命令在不同的境况下if和of应作相应的修改，写在这里只是一个例子，总之在用dd之前最好先看看man.刚才你已经看到你的分区表了,现在找一个和你的硬盘一样的硬盘,应该是一摸一样 (大小，型号),在这块硬盘上按照坏盘上的分区表分区，分的区也应该是也是一模一样然后用dd命令把坏盘上superblock location后的东西全部拷到好盘的superblock location后，上帝保佑你，当你再次启动系统时就可以看到熟悉的数据了,有人用这种方法恢复了99%以上的数据,不过好在这种方法(包括前面的方法)没有动那块坏盘上的数据,如果还是没有恢复,那没你还有最后一种选择.


  
    在手册页里称这种方法为last-ditch recovery method,就是说这是最后的恢复方法，只有当你已经尝试了其他的方法,都没有能恢复你的数据的情况下才用,因为这需要冒一定的风险.
 把你的硬盘挂在一台好的linux box上，运行: #mke2fs -S /dev/hda2(如果你的数据在hda2里) 这条命令只重建superblock，而不碰inode表，不过这仍有一定的风险。good luck to you all.当时也有人建议我如果实在不行的话就重装系统 (不动分区也不格式化) ，这也可能有效，但你也应该清楚这种方法就像mke2fs -S /dev/hd*一样是有风险的。
  


一点建议: 
  
如果你的硬盘不是可以轻易就重做的，最好在建立一个新的系统后: 
  
1。拿出笔和纸,把你的分区信息详细记录下来.
  
2. 用mkbootdisk做好现在这个系统的启动盘并测试.特别是如果你用的硬盘是scsi的。
  
3. 在用mke2fs建立一个文件系统后将屏幕上的superblock所在位置记录下来。
  
4. 用crontab对重要数据进行备份。ext2文件系统 (包括其他的unix文件系统) 是很强壮的，但你仍然应该小心。

RedHat官方解释: 
  
解决方法:
  
通常在作磁盘操作之前应该备份磁盘的数据，在作这个操作之前也应该把磁盘上的所有内容备份到另一个磁盘中。就是说如果这个故障盘是20g的话，就需要一个20G的备份空间。备份的命令如下: 
  
#dd if=/dev/baddrive of=/storagearea
  
然后可以在已经卸载的故障盘上运行如下命令找到备份的superblock.
  
#mke2fs -n /dev/badparition
  
再运行mke2fs命令的时候需要把参数设置成为文件系统创建时所用的参数。如果当初使用的是默认值， 那就可以使用如下命令: 
  
#mke2fs -n -b 4000 /dev/hdb1
  
可以看到有如下的输出:
  
Filesystem label=
  
OS type: Linux
  
Block size=1024 (log=0)
  
Fragment size=1024 (log=0)
  
122400 inodes, 488848 blocks
  
24442 blocks (5.00%) reserved for the super user
  
First data block=1
  
60 block groups
  
8192 blocks per group, 8192 fragments per group
  
2040 inodes per group
  
Superblock backups stored on blocks:
          
8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409
  
从输出可知superblock存在于: 8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409.

http://blog.sina.com.cn/s/blog_709df8c80100ldup.html
  
http://homepage.smc.edu/morgan_david/cs40/analyze-ext2.htm?spm=a2c4e.10696291.0.0.169219a4BS6PeP