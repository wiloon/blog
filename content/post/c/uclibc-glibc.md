---
title: "uclibc, glibc"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "uclibc, glibc"

uClibc 和Glibc 并不相同,两者有许多不同之处,而且以下不同有可能给你带来一些问题.

1. uClibc比Glibc小,虽然uClibc和Glibc在已有的接口上是兼容的,而且采用uClibc编译应用程序比采用Glibc编译应用程序要更方便,但是uClibc并没有包括Glibc中的所有接口实现,因此有些应用可能在uClibc中不能编译。
2. uClibc在可配置性上比Glibc要好。
3. uClibc 并不能保证发布的库二进制兼容旧版本uClibc库。当一个新的版本uClibc库被发布,则可能需要也可能不需要重新编译应用程序。
4. 在Glibc中调用malloc(0),将返回一个有效的指针,然而在uClibc中调用malloc(0),则返回NULL指针。根据在SuSv3中关于malloc(0)的行为的定义,两个库的实现都是正确的。对于调用relloc(NULL,0),两个库的实现也不同。个人感觉Glibc的如此实现不是特别安全。
    Glibc中malloc的实现可以通过MALLOC_CHECK_ 环境变量调节。这个方法主要用于malloc调试。这些扩展的malloc调试特性在uClibc中是不可用的。在Linux上有许多有些的malloc调试功能的库(如: dmalloc,electric fence,valgrind等)比Glibc中的扩展的malloc调试功能更好用。因此uClibc中去掉这些功能特性并不会有多打损失。
5. uClibc没有提供用于数据接口的库(libdb)。
6. uClibc不支持NSS(/lib/libnss_*),在这方面Glibc更容易支持不同方式的认证和DNS解析。uClibc仅仅支持采用flat口令文件或者shadow口令文件存储授权信息。如果需要比这些更复杂的的授权,可以编译安装pam。
7. uClibc中的libresolv库仅仅是一个桩。Glibc的libresolv库中的部分并不是全部的功能uClibc都提供,许多函数都没有实现。
8. 提供网络信息服务支持(NIS)libnsl库(最初被称为黄页YP),被SUN扩展为发明为RPC并用于网络共享Unix口令文件
。个人认为NIS是一个令人厌恶的东西并应该使用。因此,在实现相同的功能情况下采用ldap比NIS更有效。uClibc虽然提供一个桩libnsl,但并不支持NIS。我们因此也不提供在Glibc下提供的位于/usr/include/rpcsvc里的头文件。
9. uClibc的区域支持并不是100%的完全。正在这方面努力

10. uClibc的数据功能函数库内部仅仅支持long double,设置对于long double的支持也是非常有限。与此对应的只实现了较少的数学函数。如果应用程序采用double类型,则会程序会运行得较好。
11. uClibc的libcrpt库不支持可重入crypt_r,setkey_r和encrypt_r,因为这些也不是SuSv3所规定的。
12. uClibc直接采用内核的数据类型去定义大多数透明的数据类型。
13. uClibc支持采用linux内核结构特有的结构体"struct stat"。
14. uClibc的运行时库librt当前缺少aio接口、全部的时钟接口和共享内存接口(仅仅实现定时器接口和消息队列接口)

版权声明: 本文为CSDN博主「zengwh」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/zengwh/article/details/1482418](https://blog.csdn.net/zengwh/article/details/1482418)
