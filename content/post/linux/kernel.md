---
title: linux 内核, kernel 
author: "-"
date: 2012-02-26T06:37:22+00:00
url: /?p=2457
categories:
  - Linux
tags:
  - reprint
---
## linux 内核, kernel

### kernel doc

    https://www.kernel.org/doc/html/latest/

### linux内核版本的分类

    Linux内核版本有两种: 稳定版和开发版 ，Linux内核版本号由3组数字组成: 第一个组数字.第二组数字.第三组数字
 第一个组数字: 目前发布的内核主版本。
 第二个组数字: 偶数表示稳定版本；奇数表示开发中版本。
 第三个组数字: 错误修补的次数。
  
    例1:  2.6.18-128.ELsmp ,
 第一个组数字: 2 , 主版本号
 第二个组数字: 6 , 次版本号，表示稳定版本(因为有偶数)
 第三个组数字 18 , 修订版本号 ， 表示修改的次数，头两个数字合在一齐可以描述内核系列。如稳定版的2.6.0，它是2.6版内核系列。128: 表示这个当前版本的第128次微调patch ， 而ELsmp指出了当前内核是为ELsmp特别调校的 EL : Enterprise Linux ； smp : 表示支持多处理器 ， 表示该内核版本支持多处理器
  
    linux内核下里的ELsmp与EL与smp

  
    在linux下ELsmp指出了当前内核是为ELsmp特别调校的 EL : Enterprise Linux ； smp : 表示支持多处理器 ， 表示该内核版本支持多处理器
 例2:Red Hat Linux开机的时候，GRUB的启动菜单会有两个选项，分别是
 Red Hat Enterprise Linux ES (版本号.ELsmp)
 Red Hat Enterprise Linux ES-up (版本号.EL)
 其实这个就是系统开机时由GRUB引导启动 － 单处理器与对称多处理器启动核心文件的区别。
 Red Hat Enterprise Linux ES (版本号.ELsmp) multiple processor (symmetric multiprocessing )
 Red Hat Enterprise Linux ES-up (版本号.EL) uniprocessor
  
    linux位数
    我们知道目前的CPU主要分为32位与64位，其中32位又可以分为:i386、i586、i686、而64的CPU则称为x86_64,这是因为不同等级的CPU命令集不相同，因此你的某些软件可能会再你的CPU进行某些优化，所以软件就有了i386、i586、i686与x86_64之分，以目前的CPU市场上来说，大多数都是64位的。
  
><https://linux-kernel-labs.github.io/refs/heads/master/index.html>
