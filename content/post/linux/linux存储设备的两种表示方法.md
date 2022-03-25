---
title: Linux存储设备的两种表示方法
author: "-"
date: 2012-01-02T02:31:21+00:00
url: /?p=2074
categories:
  - Linux

tags:
  - reprint
---
## Linux存储设备的两种表示方法
  
    
作者: 北南南北
LinuxSir.Org
 摘要:  硬盘和硬盘分区在Linux都表示为设备，按我们通俗的说法来说，就是怎么来表示或描述硬盘和或硬盘分区，但这种描述应该是科学和具体的；比如IDE硬 盘，在Linux 可以表示为 /dev/hda、/dev/hdb ... ；SCSI 接口的硬盘、SATA接口的硬盘表示为/dev/sda、/dev/sdb ... ... ；而IDE接口的硬盘/dev/hda，也可以表示为hd0 ，而 SCSI 接口的如果是 /dev/sda ，另一种表示方法是sd0； 理解两种表示方法有何用？至少GRUB引导管理器用到这些知识；另外我们mount (挂载)文件系统 (分区) ，也会用到这些知识； 目录索引 一、对于IDE接口的硬盘的两种表示方法；1、IDE接口硬盘，对于整块硬盘的两种表示方法；
 2、IDE接口硬盘分区的两种表示方法；1) 硬盘分区的第一种表示方法/dev/hd[a-z]X；
 1) 硬盘分区的第二种表示方法(hd[0-n],y)；二、关于SATA和SCSI接口的硬盘的两种表示方法； 三、usb及1394接口的存储设备和软驱设备； 四、关于存储设备的不同的表示方法的应用；1、/dev/hd[a-z] 表示方法的应用；1) 用于mount 挂载文件系统 (分区) 之用；
 2) 用于GRUB中指定Linux的根分区的位置；2、hd[0-n] 表示方法的应用；五、关于本文；
 六、参考文档；
 六、相关文档；
  
    一、对于IDE接口的硬盘的两种表示方法；
  
  
    1、IDE接口硬盘，对于整块硬盘的两种表示方法；
 IDE接口中的整块硬盘在Linux系统中表示为/dev/hd[a-z]，比如/dev/hda，/dev/hdb ... ... 以此类推，有时/dev/hdc可能表示的是CDROM ，还是以具体的fdisk -l 输出为准吧； 另一种表示方法是hd[0-n] ，其中n是一个正整数，比如hd0,hd1,hd2 ... ... hdn ； 如果机器中只有一块硬盘，无论我们通过fdisk -l 列出的是/dev/hda 还是/dev/hdb ，都是hd0;如果机器中存在两个或两个以上的硬盘，第一个硬盘/dev/hda 另一种方法表示为hd0,第二个硬盘/dev/hdb，另一种表法是hd1 ； 感觉大家对hd0，hd1这种表示方法并不寞生，现在新的机器，在BIOS 中，在启动盘设置那块，硬盘是有hd0，hd1之类的，这就是硬盘表示方法的一种； 对于/dev/hda 类似的表示方法，也并不寞生吧；我们在Linux通过fdisk -l 就可以查到硬盘是/dev/hda还是/dev/hdb； 
 [root@localhost ~]# fdisk -l
Disk /dev/hda: 80.0 GB, 80026361856 bytes

255 heads, 63 sectors/track, 9729 cylinders

Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot      Start         End      Blocks   Id  System

/dev/hda1   *           1         970     7791493+   7  HPFS/NTFS

/dev/hda2             971        9729    70356667+   5  Extended

/dev/hda5             971        2915    15623181    b  W95 FAT32

/dev/hda6            2916        4131     9767488+  83  Linux

/dev/hda7            4132        5590    11719386   83  Linux

/dev/hda8            5591        6806     9767488+  83  Linux

/dev/hda9            6807        9657    22900626   83  Linux

/dev/hda10           9658        9729      578308+  82  Linux swap / Solaris 请注意第一行， Disk /dev/hda: 80.0 GB, 80026361856 bytes ，这个就是表示机器中只有一个硬盘设备/dev/hda ，体积大小为 80.0G；下面的就是硬盘的分区，每个分区都有详细的信息，在这里不详细说了；
 2、IDE接口硬盘分区的两种表示方法； 
    
    
      1) 硬盘分区的第一种表示方法/dev/hd[a-z]X；
 硬盘的分区也有两种表示方法，一种是/dev/hd[a-z]X，这个a- z表示a、b、c......z ，X是一个从1开始的正整数；比如/dev/hda1，/dev/hda2 .... /dev/hda6，/dev/hda7 ... ... 值得注意的是/dev/hd[a-z]X，如果X的值是1到4,表示硬盘的主分区 (包含扩展分区) ；逻辑分区从是从5开始的，比如/dev/hda5肯定 是逻辑分区了； 我 用fdisk -l 就能列出一个硬盘的分区表，比如:  
 [root@localhost ~]# fdisk -l
Disk /dev/hda: 80.0 GB, 80026361856 bytes

255 heads, 63 sectors/track, 9729 cylinders

Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot      Start         End      Blocks   Id  System

/dev/hda1   *           1         970     7791493+   7  HPFS/NTFS

/dev/hda2             971        9729    70356667+   5  Extended

/dev/hda5             971        2915    15623181    b  W95 FAT32

/dev/hda6            2916        4131     9767488+  83  Linux

/dev/hda7            4132        5590    11719386   83  Linux

/dev/hda8            5591        6806     9767488+  83  Linux

/dev/hda9            6807        9657    22900626   83  Linux

/dev/hda10           9658        9729      578308+  82  Linux swap / Solaris 
 2) 硬盘分区的第二种表示方法(hd[0-n],y)； 
      
      
        我们前面已经说过了整块硬盘也有两种表示方法，一种是/dev/hd[a-z]的，另种方法是hd[0-n]； 一个硬盘分区首先要大确认在哪个硬盘，然后再确认他所在的位置；做个比喻，比如我住在XXX宾馆YYY号房间，我仅仅是告诉别人我在XXX宾馆不够的，还 要告诉他YYY房间，这样来找我的人才能找到我；所以我们要知道一个硬盘分区，除了知道/dev/hd[a-z]以外，还要知道他在哪个位置，也就有前面 所说的/dev/hd[a-z]X的说法，确认了分区在/dev/hd[a-z]后，还要通过X来确认具体位置； 本标题中说的是另外一种表示方法 (hd[0-n],y)，hd[0-n]我们知道这是硬盘的表示方法之一，如果不懂，请看看前面的东西吧；那这里的y是什么意思呢？y的值是 /dev/hd[a-z]X中的 X-1 ； 用实例来理解吧； 
 [root@localhost ~]# fdisk -l
Disk /dev/hda: 80.0 GB, 80026361856 bytes

255 heads, 63 sectors/track, 9729 cylinders

Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot      Start         End      Blocks   Id  System

/dev/hda1   *           1         970     7791493+   7  HPFS/NTFS

/dev/hda2             971        9729    70356667+   5  Extended

/dev/hda5             971        2915    15623181    b  W95 FAT32

/dev/hda6            2916        4131     9767488+  83  Linux

/dev/hda7            4132        5590    11719386   83  Linux

/dev/hda8            5591        6806     9767488+  83  Linux

/dev/hda9            6807        9657    22900626   83  Linux

/dev/hda10           9658        9729      578308+  82  Linux swap / Solaris/dev/hda1 等同 (hd0,0)
 /dev/hda2 等同 (hd0,1) 注: 看好了，这个是扩展分区，在Linux还是Windows是不能挂载的；
 /dev/hda5 等同 (hd0,4)
 /dev/hda6 等同 (hd0,5)
 /dev/hda7 等同 (hd0,6)
 /dev/hda8 等同 (hd0,7)
 ... ...
 /dev/hda10 同 (hd0,9) 对于机器中只有一个硬盘来说，无论在Linux通过/dev/hda 还是/dev/hdb ，用 hd[0-n]表示方法，都是hd0；所以如果您如果硬盘中列出来的是； 
 [root@localhost ~]# fdisk -l
Disk /dev/hdb: 80.0 GB, 80026361856 bytes

255 heads, 63 sectors/track, 9729 cylinders

Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot      Start         End      Blocks   Id  System

/dev/hdb1   *           1         970     7791493+   7  HPFS/NTFS

/dev/hdb2             971        9729    70356667+   5  Extended

/dev/hdb5             971        2915    15623181    b  W95 FAT32

/dev/hdb6            2916        4131     9767488+  83  Linux

/dev/hdb7            4132        5590    11719386   83  Linux

/dev/hdb8            5591        6806     9767488+  83  Linux

/dev/hdb9            6807        9657    22900626   83  Linux

/dev/hdb10           9658        9729      578308+  82  Linux swap / Solaris 对于机器中只有一个硬盘来说，如果通过fdisk -l 列出来的是/dev/hdb的分区表；对应关系和/dev/hda列出的分区表对应关系一样； /dev/hdb1 等同 (hd0,0)
 /dev/hdb2 等同 (hd0,1) 注: 看好了，这个是扩展分区，在Linux还是Windows是不能挂载的；
 /dev/hdb5 等同 (hd0,4)
 /dev/hdb6 等同 (hd0,5)
 /dev/hdb7 等同 (hd0,6)
 /dev/hdb8 等同 (hd0,7)
 ... ...
 /dev/hdb10 等同 (hd0,9) 注意: 如果机器中有两块硬盘，那/dev/hda 另一种表示方法就是hd0,/dev/hdb 的另一种表示方法是hd1；这样我们就理解 (hd[0-n],y)的写法了吧；这样机器只有单个硬盘或者多个硬盘，我们都知道怎么写了；对不对？可能也不对，那就请指正吧；
 二、关于SATA和SCSI接口的硬盘的两种表示方法；
 理解方法和IDE接口的硬盘相同，只是把hd换成sd； 如果您的机器中比如有一个硬盘是/dev/hda ，也有一个硬盘是/dev/sda ，那/dev/sda的硬盘应该是sd0； 具体每个分区用(sd[0-n],y)的表示方法和IDE接口中的算法相同，比如/dev/sda1 就是(sd0,0)；
 三、usb及1394接口的存储设备和软驱设备；
 usb存储设备也目前在内核中在两种驱动方法，一种是模拟SCSI硬盘，通过 fdisk -l 出现的是/dev/sd[0-n] ；如果是模拟SCSI设备的方法来驱动。那usb 存储设备在Linux的另一种表示方法和前面所说的SCSI和SATA的相同； 但目前新版本的内核中，想抛弃模拟SCSI，我们通过fdisk 列系统存在的存储设置时会出现 /dev/uba 类似的；但目前这个驱动并不成熟，比如大数据量表现不稳定；其实USB接口的存储设备，在Linux表现还是比较差； 1394接口存储调备，在Linux中也是模拟SCSI，我们通过fdisk -l 后，出现的也是/dev/sd[0-n]，另一种表示方法(sd[a-z],y)的理解请参照前面所说的； 1394接口的存储设备在Linux表现极好，USB存储如果相对1394接口的存储表现来说，应该不值不提，建议大家购买1394接口的存储设备； 软驱在Linux中，是/dev/fd0设备这是一般情况，另一种表示为fd0 ； CDROM 或DVDROM ，以及COMBO ，一般的情况下是/dev/hdc ；看下面的例子，无论是 /dev/cdrom 还是/dev/dvd ，最后都指向了/dev/hdc； 
 [root@localhost ~]# ls -la /dev/cdrom

lrwxrwxrwx  1 root root 3 2005-12-14  /dev/cdrom -> hdc

[root@localhost ~]# ls -la /dev/dvd

lrwxrwxrwx  1 root root 3 2005-12-14  /dev/dvd -> hdc 
 四、关于存储设备的不同的表示方法的应用； 
        
        
          1、/dev/hd[a-z] 表示方法的应用
        
        
        
          1) 用于mount 挂载文件系统 (分区) 之用；
 我们在前面所说的，硬盘的分区/dev/hd[a-z]X表示方法，一般是用于挂载和读取文件系统之用的； 
 [root@localhost ~]# fdisk -l
Disk /dev/hda: 80.0 GB, 80026361856 bytes

255 heads, 63 sectors/track, 9729 cylinders

Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot      Start         End      Blocks   Id  System

/dev/hda1   *           1         970     7791493+   7  HPFS/NTFS

/dev/hda2             971        9729    70356667+   5  Extended

/dev/hda5             971        2915    15623181    b  W95 FAT32

/dev/hda6            2916        4131     9767488+  83  Linux

/dev/hda7            4132        5590    11719386   83  Linux

/dev/hda8            5591        6806     9767488+  83  Linux

/dev/hda9            6807        9657    22900626   83  Linux

/dev/hda10           9658        9729      578308+  82  Linux swap / Solaris 比如我要挂载 /dev/hda9 到系统中；所以过程应该是这样的；
 
 [root@localhost ~]# mkdir /opt/data/  注: 建立挂载点目录；

[root@localhost ~]# mount /dev/hda9 /opt/data/  注: 挂载； 是不是挂载好了呢？看下面的信息，显示已经挂载好了，所以这时我们就能向/opt/data目录写东西了，写的所有东西都记录在了/dev/hda9上； 
 [root@localhost ~]# df -lh

Filesystem            容量  已用 可用 已用% 挂载点

/dev/hda7              11G  9.2G  1.1G  90% /

/dev/shm              236M     0  236M   0% /dev/shm

/dev/hda9              22G  3.9G   18G  18% /opt/data 注意: 挂载得需要内核支持，另外分区也得建立文件系统，请参考相关文档 ；
 2) 用于GRUB中指定Linux的根分区的位置；
 在GRUB系统引导管理器，用命令行启动一个操作系统时，要通过指定Linux根/所在的硬盘分区 /dev/hd[a-z]X；比如 root=/dev/hda7 ；
 2、hd[0-n] 表示方法的应用；
 这种一般是应用在GRUB的/boot所位于的硬盘分区的指定上；在GRUB的命令行和GRUB 的配置文件menu.lst 中都要应用到； 比如我们要把GRUB写到硬盘的MBR上，在GRUB的命令行模式中要通过root (hd[0-n],y)来指定；这里的root (hd[0-n],y)，在GRUB中就/boot所位于的分区；不要搞错了，有时/boot和Linux的根/并不是处于同一个分区的，就看您安装 Linux时怎么安装的了；而我们前面所说的root=/dev/hd[a-z]X来指定的是Linux 根/所位于的分区；虽然有时/boot和/同处一个分区，但两种表示方法在GRUB中各有用途；明白了吧； 比如/boot位于同一个硬盘分区，就可以用类似下的方法来把GRUB写到硬盘的MBR上；举个例子； 
 [root@localhost ~]# grub  注: 运行GRUB；
grub> root (hd0,6)  注: 比如/boot位于 (hd0,6)分区上，应该这样

Filesystem type is ext2fs, partition type 0x83
grub> setup (hd0)

Checking if "/boot/grub/stage1" exists... yes

Checking if "/boot/grub/stage2" exists... yes

Checking if "/boot/grub/e2fs_stage1_5" exists... yes

Running "embed /boot/grub/e2fs_stage1_5 (hd0)"...  15 sectors are embedded.

succeeded

Running "install /boot/grub/stage1 (hd0) (hd0)1+15 p (hd0,6)/boot/grub/stage2

/boot/grub/grub.conf"... succeeded

Done.
grub>quit 注: 退出GRUB命令行模式；
 如果您不懂，慢慢就会了，我这里写的只是为了应用罢了；如果您要搞懂为什么Linux的存储设备表达上是这样或者那样的，还是建议您看看kernel的文档；可能中文文档并不能满足您的需要，最好还是洋文的吧；
 五、关于本文；
 这篇关于存储设备在Linux中有两种不同的表达方法，可能说的有点复杂化了；用pandonny兄的话来说: "本来是 理论性的概念的东西，写得太理论性的东西新手反而看不懂，还是描述性的往往更容易被新手理解"。 这篇文档主要是把抽象的概念具体化，我不知道初学的弟兄是否能看得懂，至少我已经尽全力了，对我来说已经是"北南技穷"。关于理论文面的文档就是翻译过来 也是极为难翻译的，更不要说简单的描述了；初学Linux的弟兄，慢慢实践着来吧；实践是检验真理的唯一标准，相信这一真理绝对没错！！千万不要把我所说 过的是真理，真理在你手中。。。。。。因为您是实践者； 本来写GRUB入门文档了，结果发现不写一写存储设备的表示方法不太行，所以被迫写了这篇文章，虽然勉强，但还是写出来了；
 六、参考文档； 
          
          
            《GNU GRUB 手册和FAQ》
 七、相关文档；
 《合理规划您的硬盘分区》
 《系统引导过程及硬盘分区结构论述》
 《Linux 查看磁盘分区、文件系统、使用情况的命令和相关工具介绍》
 《实例解说 fdisk 使用方法》
 《在Fedora core 4.0 加载NTFS和FAT32分区详述》
 《Fedora Core 4.0 HAL配置即插即用移动存储 (USB及1394) 的实践》