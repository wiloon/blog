---
title: Debian32位Linux系统大内存支持
author: wiloon
type: post
date: 2011-11-26T13:02:31+00:00
url: /?p=1650
views:
  - 8
bot_views:
  - 3
categories:
  - Linux

---
## <http://www.voland.com.cn/debian32-bit-linux-system-to-support-large-memory>

  
    公司的服务器为2G的内存，使用free命令查看，明显不够用了，现在使用了大量的交换分区，那么，就升级内存吧，两条4G的kingston内存就这样补加上了，但原来的系统是Debian32位Linux系统，上8G内存根本不支持，使用free命令查看，只支持3.1G的内存！如果换64位的系统比较麻烦，服务器上安装配置的东西太多了，只能升级系统内核来解决了，debian提供了bigmem内核，在升级之前，第一步需要更新一下源：
  
  
  
    
      $sudo apt-get update
    
  
  
  
    第二步就是查看一下自己当前的内核：
  
  
  
    
      $uname -a
    
  
  
  
    我当前服务器的内核是Linux mail 2.6.18-6-686 #1 SMP Sat Feb 20 00:15:53 UTC 2010 i686 GNU/Linux，可能你的系统的内核不是这个，所以第三步查看一下有哪些bigmem内核可以对应当前内核升级
  
  
  
    
      $sudo apt-cache search linux image bigmem
    
  
  
  
    本人的服务器显示如下：
 linux-headers-2.6.24-etchnhalf.1-686-bigmem – Header files for Linux 2.6.24 on PPro/Celeron/PII/PIII/P4
 linux-image-2.6.24-etchnhalf.1-686-bigmem – Linux 2.6.24 image on PPro/Celeron/PII/PIII/P4
 linux-headers-2.6.18-6-686-bigmem – Header files for Linux 2.6.18 on PPro/Celeron/PII/PIII/P4
 linux-image-2.6.18-6-686-bigmem – Linux 2.6.18 image on PPro/Celeron/PII/PIII/P4
 linux-image-2.6-686-bigmem-etchnhalf – Linux 2.6-etchnhalf image on PPro/Celeron/PII/PIII/P4
 linux-image-2.6-686-bigmem – Linux kernel 2.6 image on PPro/Celeron/PII/PIII/P4
 linux-image-686-bigmem – Linux kernel image on PPro/Celeron/PII/PIII/P4
  
  
  
    最后就是升级内核的超作了，
  
  
  
    
      $sudo apt-get install linux-image-2.6.18-6-686-bigmem
$sudo apt-get install linux-headers-2.6.18-6-686-bigmem
    
  
  
  
    内核升级完成后，重启系统
  
  
  
    
      sudo reboot
    
  
  
  
    系统重启后，再查看一下内核与内存使用情况吧，我的是可以了,现在可以最大支持到64个G了。不过据说这个需要主板的支持，服务器主板我想应该都支持吧。希望需要升级内存的你也能操作成功，good luck!
  
