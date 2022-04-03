---
title: /dev/zero和/dev/null
author: "-"
date: 2012-06-08T05:41:02+00:00
url: /?p=3453
categories:
  - Linux

tags:
  - reprint
---
## /dev/zero和/dev/null
### /dev/null
    在类Unix系统中，/dev/null，或称空设备，是一个特殊的设备文件，它丢弃一切写入其中的数据 (但报告写入操作成功) ，读取它则会立即得到一个EOF[1]。
  

在程序员行话，尤其是Unix行话中，`/dev/null`被称为bit bucket[2]或者黑洞。使用

空设备通常被用于丢弃不需要的输出流，或作为用于输入流的空文件。这些操作通常由重定向完成。

/dev/null是一个特殊_文件_，而不是目录，因此不能使用Unix命令mv 将文件移动到其中。使用rm命令才是Unix中删除文件的正确方法。

本概念大致相当于CP/M，DOS和Microsoft Windows中的NUL:或单纯的NUL设备，Windows NT及其后续系统中的DeviceNull或NUL，Amiga中的NIL:，以及OpenVMS中的NL:。在基于.NET的Windows PowerShell中，相同的概念为$null。

---
### /dev/zero
    /dev/zero,是一个输入设备，你可你用它来初始化文件。
 /dev/zero--该设备无穷尽地提供0(是ASCII 0 就是NULL)，可以使用任何你需要的数目——设备提供的要多的多。他可以用于向设备或文件写入NULL。
 使用/dev/zero
 像/dev/null一样, /dev/zero也是一个伪文件, 但它实际上产生连续不断的null的流 (二进制的零流，而不是ASCII型的) . 写入它的输出会丢失不见, 而从/dev/zero读出一连串的null也比较困难, 虽然这也能通过od或一个十六进制编辑器来做到. /dev/zero主要的用处是用来创建一个指定长度用于初始化的空文件，就像临时交换文件.
  
  
    关于 /dev/zero 的另一个应用是为特定的目的而用零去填充一个指定大小的文件, 如挂载一个文件系统到环回设备  (loopback device)  或"安全地" 删除一个文件
  
  
  
  
    /dev/null，外号叫无底洞，你可以向它输出任何数据，它通吃，并且不会撑着！
 /dev/null--它是空设备，也称为位桶 (bit bucket) 。任何写入它的输出都会被抛弃。如果不想让消息以标准输出显示或写入文件，那么可以将消息重定向到位桶。
 使用/dev/null
 把/dev/null看作"黑洞". 它非常等价于一个只写文件. 所有写入它的内容都会永远丢失. 而尝试从它那儿读取内容则什么也读不到. 然而, /dev/null对命令行和脚本都非常的有用.
 禁止标准输出.    cat $filename >/dev/null                -文件内容丢失，而不会输出到标准输出.
 禁止标准错误   rm $badname 2>/dev/null              -这样错误信息[标准错误]就被丢到太平洋去了.
 禁止标准输出和标准错误的输出.    1 cat $filename 2>/dev/null >/dev/null
 -如果"$filename"不存在，将不会有任何错误信息提示.
 - 如果"$filename"存在, 文件的内容不会打印到标准输出.
 -因此Therefore, 上面的代码根本不会输出任何信息.
 -当只想测试命令的退出码而不想有任何输出时非常有用。
 Deleting contents of a file, but preserving the file itself, with all attendant permissions :
 cat /dev/null > /var/log/messages       -> /var/log/messages   有同样的效果, 但不会产生新的进程.
 cat /dev/null > /var/log/wtmp     - 自动清空日志文件的内容 (适合处理由Web站点发送的讨厌的"cookies")
  
  
  
