---
title: Linux下 快速创建大文件
author: "-"
date: 2020-04-12T13:51:25+00:00
url: /?p=15925
categories:
  - Uncategorized

tags:
  - reprint
---
## Linux下 快速创建大文件
https://www.jianshu.com/p/5a2b2a0b6468

dd命令
  
生成一个1000M的test文件，文件内容为全0 (因从/dev/zero中读取，/dev/zero为0源) 。但是这样为实际写入硬盘，文件产生速度取决于硬盘读写速度，如果想要产生超大文件，速度很慢。

[root@izwz94jtz9hbdq165vpxpxz www]# dd if=/dev/zero of=test1 bs=1M count=1000
   
1000+0 records in
   
1000+0 records out
   
1048576000 bytes (1.0 GB) copied, 16.6081 s, 63.1 MB/s //内存操作速度
  
在某种场景下，我们只想让文件系统认为存在一个超大文件在此，但是并不实际写入硬盘。则可以使用 seek

1) count=0 表示读写 0次，指定生成文件的大小为0M

[root@izwz94jtz9hbdq165vpxpxz www]# dd if=/dev/zero of=test2 bs=1M count=0 seek=100000
    
0+0 records in
    
0+0 records out
    
0 bytes (0 B) copied, 0.000221494 s, 0.0 kB/s
  
2) count=50 表示读写 50次，指定生成文件的大小为50M

[root@izwz94jtz9hbdq165vpxpxz www]# dd if=/dev/zero of=test3 bs=1M count=50 seek=100000
    
50+0 records in
    
50+0 records out
    
52428800 bytes (52 MB) copied, 0.066445 s, 789 MB/s
   
[root@izwz94jtz9hbdq165vpxpxz www]# ls -l test3 //查看目录大小
   
-rw-r-r- 1 root root 104910028800 Aug 3 23:50 test3
  
此时创建的文件在文件系统中的显示大小为100000MB，但是并不实际占用block，因此创建速度与内存速度相当。

作者: 倔强的潇洒小姐
  
链接: https://www.jianshu.com/p/5a2b2a0b6468
  
来源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。