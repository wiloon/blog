---
title: IO
author: "-"
date: 2012-02-25T02:47:29+00:00
url: /?p=2389
categories:
  - OS
tags:
  - IO

---
## IO

下列是参数flags 所能使用的旗标:
O_RDONLY 以只读方式打开文件
O_WRONLY 以只写方式打开文件
O_RDWR 以可读写方式打开文件. 上述三种旗标是互斥的, 也就是不可同时使用, 但可与下列的旗标利用OR(|)运算符组合.
O_CREAT 若欲打开的文件不存在则自动建立该文件.
O_EXCL 如果O_CREAT 也被设置, 此指令会去检查文件是否存在. 文件若不存在则建立该文件, 否则将导致打开文件错误. 此外, 若O_CREAT 与O_EXCL 同时设置, 并且欲打开的文件为符号连接, 则会打开文件失败.
O_NOCTTY 如果欲打开的文件为终端机设备时, 则不会将该终端机当成进程控制终端机.
O_TRUNC 若文件存在并且以可写的方式打开时, 此旗标会令文件长度清为0, 而原来存于该文件的资料也会消失.
O_APPEND 当读写文件时会从文件尾开始移动, 也就是所写入的数据会以附加的方式加入到文件后面.
O_NONBLOCK 以不可阻断的方式打开文件, 也就是无论有无数据读取或等待, 都会立即返回进程之中.
O_NDELAY 同O_NONBLOCK.
O_SYNC 以同步的方式打开文件.
O_NOFOLLOW 如果参数pathname 所指的文件为一符号连接, 则会令打开文件失败.
O_DIRECTORY 如果参数pathname 所指的文件并非为一目录, 则会令打开文件失败。注：此为Linux2. 2 以后特有的旗标, 以避免一些系统安全问题.


>http://c.biancheng.net/cpp/html/238.html
>https://wiyi.org/linux-io-model.html
