---
title: Bootchart, systemd-analyze
author: "-"
date: 2012-02-28T14:43:40+00:00
url: bootchart
categories:
  - Linux
tags:
  - reprint
---
## Bootchart, systemd-analyze

 Bootchart 已经成为 systemd 的一部分

<https://wiki.archlinux.org/title/Improving_performance/Boot_process#Analyzing_the_boot_process>

 systemd-analyze plot > plot.svg

很多朋友抱怨自己的 Linux 系统启动速度太慢，但又苦于没有什么好途径进行分析，使之能够得到改进。如果你正受到这方面问题的困惑，那么有一个 Bootchart 小工具能够帮助你。
  
    Bootchart 能够对系统的性能进行分析，并生成系统启动过程的图表，以便为你提供有价值的参考信息。综合所得的信息，你就可以进行相应的改进，从而加快你的 Linux 系统启动过程。
  
  
    在安装 Bootchart 并重新启动系统后，你就可以在 /var/log/bootchart/ 找到它生成的图片文件了。以下是我的系统所生成的启动过程图表，你可以参考一下。
  
  
    First you need to enable some options in the kernel to use the BSD process accounting. This feature is optional, but is highly recommended for improved accuracy. If you are using genkernel to build your kernel, run the following command:
  
  
    And enable the following options:
  
  
    
      General setup —>
 [*] BSD Process Accounting
 [*] BSD Process Accounting version 3 file format

    http://www.krizka.net/2007/08/20/howto-bootchart-with-bsd-process-accounting-on-gentoo/
  