---
title: Bootchart
author: wiloon
type: post
date: 2012-02-28T14:43:40+00:00
url: /?p=2494
categories:
  - Linux

---
很多朋友抱怨自己的 Linux 系统启动速度太慢，但又苦于没有什么好途径进行分析，使之能够得到改进。如果你正受到这方面问题的困惑，那么有一个 Bootchart 小工具能够帮助你。

<div>
  <p>
    Bootchart 能够对系统的性能进行分析，并生成系统启动过程的图表，以便为你提供有价值的参考信息。综合所得的信息，你就可以进行相应的改进，从而加快你的 Linux 系统启动过程。
  </p>
  
  <p>
    在安装 Bootchart 并重新启动系统后，你就可以在 /var/log/bootchart/ 找到它生成的图片文件了。以下是我的系统所生成的启动过程图表，你可以参考一下。
  </p>
  
  <p>
    First you need to enable some options in the kernel to use the BSD process accounting. This feature is optional, but is highly recommended for improved accuracy. If you are using genkernel to build your kernel, run the following command:
  </p>
  
  <p>
    And enable the following options:
  </p>
  
  <blockquote>
    <p>
      General setup —><br /> [*] BSD Process Accounting<br /> [*] BSD Process Accounting version 3 file format
    </p>
  </blockquote>
  
  <p>
    <a href="http://www.krizka.net/2007/08/20/howto-bootchart-with-bsd-process-accounting-on-gentoo/">http://www.krizka.net/2007/08/20/howto-bootchart-with-bsd-process-accounting-on-gentoo/</a>
  </p>
</div>