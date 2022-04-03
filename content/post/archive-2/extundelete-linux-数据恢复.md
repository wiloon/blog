---
title: extundelete linux 数据恢复
author: "-"
date: 2018-02-08T15:27:49+00:00
url: /?p=11843
categories:
  - Uncategorized

tags:
  - reprint
---
## extundelete linux 数据恢复
http://blog.51cto.com/ixdba/1566856

Linux下高效数据恢复软件extundelete应用实战 推荐
  
原创南非蚂蚁2014-10-22 17:58:11评论(8)11866人阅读
  
推荐: 10年技术力作: 《高性能Linux服务器构建实战Ⅱ》全网发行,附试读章节和全书实例源码下载！

作为一名运维人员,保证数据的安全是根本职责,所以在维护系统的时候,要慎之又慎,但是有时难免会出现数据被误删除的情况,在这个时候改如何快速、有效地恢复数据呢？本文我们就来介绍一下Linux系统下常用的几个数据恢复工具。

一、如何使用"rm -rf"命令

在Linux系统下,通过命令"rm -rf"可以将任何数据直接从硬盘删除,并且没有任何提示,同时Linux下也没有与Windows下回收站类似的功能,也就意味着,数据在删除后通过常规的手段是无法恢复的,因此使用这个命令要非常慎重。在使用rm命令的时候,比较稳妥的方法是把命令参数放到后面,这样有一个提醒的作用。其实还有一个方法,那就是将要删除的东西通过mv命令移动到系统下的/tmp目录下,然后写个脚本定期执行清除操作,这样做可以在一定程度上降低误删除数据的危险性。

其实保证数据安全最好的方法是做好备份,虽然备份不是万能的,但是没有备份是万万不行的。任何数据恢复工具都有一定局限性,都不能保证完整地恢复出所有数据,因此,把备份作为核心,把数据恢复工具作为辅助是运维人员必须坚持的一个准则。

二、extundelete与ext3grep的异同

在Linux下,基于开源的数据恢复工具有很多,常见的有debugfs、R-Linux、ext3grep、extundelete等,比较常用的有ext3grep和extundelete,这两个工具的恢复原理基本一样,只是extundelete功能更加强大,本文重点介绍extundelete的使用。

三、extundelete的恢复原理

在介绍使用extundelete进行恢复数据之前,简单介绍下关于inode的知识。在Linux下可以通过"ls –id"命令来查看某个文件或者目录的inode值,例如查看根目录的inode值,可以输入: 

[root@cloud1 ~]# ls -id /
  
2 /
  
由此可知,根目录的inode值为2。

在利用extundelete恢复文件时并不依赖特定文件格式,首先extundelete会通过文件系统的inode信息 (根目录的inode一般为2) 来获得当前文件系统下所有文件的信息,包括存在的和已经删除的文件,这些信息包括文件名和inode。然后利用inode信息结合日志去查询该inode所在的block位置,包括直接块,间接块等信息。最后利用dd命令将这些信息备份出来,从而恢复数据文件。

四、 安装extundelete

extundelete的官方网站是http://extundelete.sourceforge.net/ ,其目前的稳定版本是extundelete-0.2.4。,在安装extundelete之前需要安装e2fsprogs和e2fsprogs-libs两个依赖包。

e2fsprogs和e2fsprogs-libs安装非常简单,这里不做介绍。下面是extundelete的编译安装过程: 

[root@cloud1 app]#tar jxvf extundelete-0.2.4.tar.bz2
  
[root@cloud1 app]#cd extundelete-0.2.4
  
[root@cloud1 extundelete-0.2.4]#./configure
  
[root@cloud1 extundelete-0.2.4]#make
  
[root@cloud1 extundelete-0.2.4]#make install
  
成功安装extundelete后,会在系统中生成一个extundelete可执行文件。extundelete的使用非常简单,读者可以通过"extundelete -help"获得此软件的使用方法。

五、extundelete 用法详解

extundelete安装完成后,就可以执行数据恢复操作了,本节详细介绍下extundelete每个参数的含义。extundelete用法如下: 

extundelete -help

命令格式:

extundelete [options] [action] device-file
  
其中参数 (options) 有: 

-version, -[vV],显示软件版本号。

-help,显示软件帮助信息。

-superblock, 显示超级块信息。

-journal,显示日志信息。

-after dtime,时间参数,表示在某段时间之后被删的文件或目录。

-before dtime,时间参数,表示在某段时间之前被删的文件或目录。

动作 (action) 有: 

-inode ino,显示节点"ino"的信息。

-block blk,显示数据块"blk"的信息。

-restore-inode ino[,ino,...],恢复命令参数,表示恢复节点"ino"的文件,恢复的文件会自动放在当前目录下的RESTORED_FILES文件夹中,使用节点编号作为扩展名。

-restore-file 'path',恢复命令参数,表示将恢复指定路径的文件,并把恢复的文件放在当前目录下的RECOVERED_FILES目录中。

-restore-files 'path',恢复命令参数,表示将恢复在路径中已列出的所有文件。

-restore-all,恢复命令参数,表示将尝试恢复所有目录和文件。

-j journal,表示从已经命名的文件中读取扩展日志。

-b blocknumber,表示使用之前备份的超级块来打开文件系统,一般用于查看现有超级块是不是当前所要的文件。

-B blocksize,表示使用数据块大小来打开文件系统,一般用于查看已经知道大小的文件。

六、实战: extundelete恢复数据的过程

在数据被误删除后,第一时间要做的是卸载被删除数据所在的磁盘或磁盘分区,如果是系统根分区的数据遭到误删除,就需要将系统进入单用户,并且将根分区以只读模式挂载。这样做的原因很简单,因为将文件删除后,仅仅是将文件的inode结点中的扇区指针清零,实际文件还存储在磁盘上,如果磁盘以读写模式挂载,这些已删除的文件的数据块就可能被操作系统重新分配出去,在这些数据块被新的数据覆盖后,这些数据就真的丢失了,恢复工具也回力无天。所以,以只读模式挂载磁盘可以尽量降低数据块中数据被覆盖的风险,以提高恢复数据成功的比率。

6.1通过extundelete恢复单个文件

1.模拟数据误删除环境

在演示通过extundelete恢复数据之前,我们首先要模拟一个数据误删除环境,这里我们以ext3文件系统为例,在ext4文件系统下的恢复方式与此完全一样。简单的模拟操作过程如下: 

[root@cloud1 ~]#mkdir /data
  
[root@cloud1 ~]#mkfs.ext3 /dev/sdc1
  
[root@cloud1 ~]#mount /dev/sdc1 /data
  
[root@cloud1 ~]# cp /etc/passwd /data
  
[root@cloud1 ~]# cp -r /app/ganglia-3.4.0 /data
  
[root@cloud1 ~]# mkdir /data/test
  
[root@cloud1 ~]# echo "extundelete test" > /data/test/mytest.txt
  
[root@cloud1 ~]#cd /data
  
[root@cloud1 data]# md5sum passwd
  
0715baf8f17a6c51be63b1c5c0fbe8c5 passwd
  
[root@cloud1 data]# md5sum test/mytest.txt
  
eb42e4b3f953ce00e78e11bf50652a80 test/mytest.txt
  
[root@cloud1 data]# rm -rf /data/*
  
2.卸载磁盘分区

在将数据误删除后,立刻需要做的就是卸载这块磁盘分区: 

[root@cloud1 data]#cd /mnt
  
[root@cloud1 mnt]# umount /data
  
3.查询可恢复的数据信息

通过extundelete命令可以查询/dev/sdc1分区可恢复的数据信息: 

[root@cloud1 /]# extundelete /dev/sdc1 -inode 2
  
......
  
File name | Inode number | Deleted status
  
. 2
  
.. 2
  
lost+found 11 Deleted
  
passwd 49153 Deleted
  
test 425985 Deleted
  
ganglia-3.4.0 245761 Deleted
  
根据上面的输出,标记为Deleted状态的是已经删除的文件或目录。同时还可以看到每个已删除文件的inode值,接下来就可以恢复文件了。

4.恢复单个文件

执行如下命令开始恢复文件: 

[root@cloud1 /]# extundelete /dev/sdc1 -restore-file passwd
  
Loading filesystem metadata ... 40 groups loaded.
  
Loading journal descriptors ... 54 descriptors loaded.
  
Successfully restored file passwd
  
[root@cloud1 /]# cd RECOVERED_FILES/
  
[root@cloud1 RECOVERED_FILES]# ls
  
passwd
  
[root@cloud1 RECOVERED_FILES]# md5sum passwd
  
0715baf8f17a6c51be63b1c5c0fbe8c5 passwd
  
extundelete恢复单个文件的参数是"-restore-file",这里需要注意的是,"-restore-file"后面指定的是恢复文件路径,这个路径是文件的相对路径。相对路径是相对于原来文件的存储路径而言的,比如,原来文件的存储路径是/data/passwd,那么在参数后面直接指定passwd文件即可,如果原来文件的存储路径是/data/test/mytest.txt,那么在参数后面通过"test/mytest.txt"指定即可。

在文件恢复成功后,extundelete命令默认会在执行命令的当前目录下创建一个RECOVERED_FILES目录,此目录用于存放恢复出来的文件,所以执行extundelete命令的当前目录必须是可写的。

根据上面的输出,通过md5sum命令校验,校验码与之前的完全一致,表明文件恢复成功。

6.2通过extundelete恢复单个目录

extundelete除了支持恢复单个文件,也支持恢复单个目录,在需要恢复目录时,通过 "-restore-directory"选项即可恢复指定目录的所有数据。

继续在上面模拟的误删除数据环境下操作,现在要恢复/data目录下的ganglia-3.4.0文件夹,操作如下: 

[root@cloud1 mnt]# extundelete /dev/sdc1 -restore-directory /ganglia-3.4.0
  
Loading filesystem metadata ... 40 groups loaded.
  
Loading journal descriptors ... 247 descriptors loaded.
  
Searching for recoverable inodes in directory /ganglia-3.4.0 ...
  
781 recoverable inodes found.
  
Looking through the directory structure for deleted files ...
  
4 recoverable inodes still lost.
  
[root@cloud1 mnt]# ls
  
RECOVERED_FILES
  
[root@cloud1 mnt]# cd RECOVERED_FILES/
  
[root@cloud1 RECOVERED_FILES]# ls
  
ganglia-3.4.0
  
可以看到之前删除的目录ganglia-3.4.0已经成功恢复了,进入这个目录检查发现: 所有文件内容和大小都正常。

6.3 通过extundelete恢复所有误删除数据

当需要恢复的数据较多时,一个个地指定文件或目录将是一个非常繁重和耗时的工作,不过,extundelete考虑到了这点,此时可以通过"-restore-all"选项来恢复所有被删除的文件或文件夹。

仍然在上面模拟的误删除数据环境下操作,现在要恢复/data目录下所有数据,操作过程如下: 

[root@cloud1 mnt]# extundelete /dev/sdc1 -restore-all
  
Loading filesystem metadata ... 40 groups loaded.
  
Loading journal descriptors ... 247 descriptors loaded.
  
Searching for recoverable inodes in directory / ...
  
781 recoverable inodes found.
  
Looking through the directory structure for deleted files ...
  
0 recoverable inodes still lost.
  
[root@cloud1 mnt]# ls
  
RECOVERED_FILES
  
[root@cloud1 mnt]# cd RECOVERED_FILES/
  
[root@cloud1 RECOVERED_FILES]# ls
  
ganglia-3.4.0 passwd test
  
[root@cloud1 RECOVERED_FILES]# du -sh /mnt/RECOVERED_FILES/*
  
15M /mnt/RECOVERED_FILES/ganglia-3.4.0
  
4.0K /mnt/RECOVERED_FILES/passwd
  
8.0K /mnt/RECOVERED_FILES/test
  
可以看到所有数据全部完整地恢复了。

6.4通过extundelete恢复某个时间段的数据

有时候删除了大量的数据量,其中很多数据都是没用的,我们仅需要恢复其中的一部分数据,此时,如果采用恢复全部数据的办法,不但耗时,而且浪费资源,在这种情况下,就需要采用另外的一种恢复机制有选择地恢复,extundelete提供了"—after""和"-before"参数,可以通过指定某个时间段,进而只恢复这个时间段内的数据。

下面通过一个简单示例,描述下如何恢复某个时间段内的数据。

我们首先假定在/data目录下有个刚刚创建的压缩文件ganglia-3.4.0.tar.gz,然后删除此文件,接着卸载/data分区,开始恢复一小时内的文件,操作如下: 

[root@cloud1 ~]#cd /data/
  
[root@cloud1 data]# cp /app/ganglia-3.4.0.tar.gz /data
  
[root@cloud1 data]# date +%s
  
1379150309
  
[root@cloud1 data]# rm -rf ganglia-3.4.0.tar.gz
  
[root@cloud1 data]# cd /mnt
  
[root@cloud1 mnt]# umount /data
  
[root@cloud1 mnt]# date +%s
  
1379150340
  
[root@cloud1 mnt]# extundelete -after 1379146740 -restore-all /dev/sdc1
  
Only show and process deleted entries if they are deleted on or after 1379146740 and before 9223372036854775807.
  
Loading filesystem metadata ... 40 groups loaded.
  
Loading journal descriptors ... 247 descriptors loaded.
  
Searching for recoverable inodes in directory / ...
  
779 recoverable inodes found.
  
[root@cloud1 mnt]# cd RECOVERED_FILES/
  
[root@cloud1 RECOVERED_FILES]# ls
  
ganglia-3.4.0.tar.gz
  
可以看到,刚才删除的文件,已经成功恢复,而在/data目录下还有很多被删除的文件却没有恢复,这就是"-after"参数控制的结果,因为/data目录下其他文件都是在一天之前删除的,而我们恢复的是一个小时之内被删除的文件,这就是没有恢复其他被删除文件的原因。

在这个操作过程中,需要注意是"-after"参数后面跟的时间是个总秒数。起算时间为"1970-01-01 00:00:00 UTC",通过"date +%s"命令即可将当前时间转换为总秒数,因为恢复的是一个小时之内的数据,所以"1379146740"这个值就是通过"1379150340"减去"60*60=3600"获得的。