---
title: jmap
author: "-"
date: 2015-09-17T08:46:25+00:00
url: /?p=8292
categories:
  - Uncategorized

tags:
  - reprint
---
## jmap

  2) 、基本参数:

  -dump:[live,]format=b,file=<filename> 使用hprof二进制形式,输出jvm的heap内容到文件=. live子选项是可选的，假如指定live选项,那么只输出活的对象到文件.

  -finalizerinfo 打印正等候回收的对象的信息.

  -heap 打印heap的概要信息，GC使用的算法，heap的配置及wise heap的使用情况.

  -histo[:live] 打印每个class的实例数目,内存占用,类全名信息. VM的内部类名字开头会加上前缀"*". 如果live子参数加上后,只统计活的对象数量.

  -permstat 打印classload和jvm heap长久层的信息. 包含每个classloader的名字,活泼性,地址,父classloader和加载的class数量. 另外,内部String的数量和占用内存数也会打印出来.

  -F 强迫.在pid没有相应的时候使用-dump或者-histo参数. 在这个模式下,live子参数无效.

  -h | -help 打印辅助信息

  -J 传递参数给jmap启动的jvm.

  pid 需要被打印配相信息的java进程id,创业与打工的区别 - 博文预览,可以用jps查问.

## 4、使用示例

  1)、[fenglb@ccbu-156-5 ~]$ jmap -histo 4939

    sudo ./jmap -dump:format=b,file=/tmp/917dump.dat 8949
  
  
  
  
    If you take a look at the source code for com.sun.tools.hat.internal.parser.Reader, you'll see that it's looking for the magic number 0x4a415641.
  
  
    This value is used to help identify valid heap dump files. jmap should append this value as the first four bytes of any heap dump file it creates.
  
  
    http://stackoverflow.com/questions/15507047/jhat-throwing-unrecognized-magic-number
  
  
    http://blog.csdn.net/gtuu0123/article/details/6039474
  