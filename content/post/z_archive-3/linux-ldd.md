---
title: ldd 查看程序依赖 动态链接库
author: "-"
date: 2019-04-05T14:05:40+00:00
url: ldd
categories:
  - Linux
tags:
  - reprint
---
## ldd 查看程序依赖 动态链接库

ldd 命令可以用于分析可执行文件的依赖。

我们使用 file 命令来分析一个可执行文件的时候，有时候可以看到输出中有 dynamically linked 这样的字眼。这个是啥意思呢？

大部分程序，都会使用到第三方库，这样就可以不用重复造轮子，节约大量时间。最简单的，我们写C程序代码的话，肯定会使用到 libc 或者 glibc 库。当然，除此之外，还可能使用其它的库。

那我们在什么情况下需要分析程序的依赖库呢？有一个场景大家肯定经历过。你去你同事那边拷备他写好的程序放到自己的环境下运行，有时候可能会跑不起来。当然跑不起来的原因可能很多，但其中一个原因可能就是缺少对应的依赖库。

这时候，ldd 就派上用场了。它可以分析程序需要一些什么依赖库，你只要把对应的库放在对应的位置就可以了。

ldd /bin/pwd
        linux-vdso.so.1 =>  (0x00007ffeb73e5000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f908b321000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f908b6ef000)

作用: 用来查看程式运行所需的共享库,常用来解决程式因缺少某个库文件而不能运行的一些问题。
  
示例: 查看test程序运行所依赖的库:

/opt/app/todeav1/test$ldd test
  
libstdc++.so.6 => /usr/lib64/libstdc++.so.6 (0x00000039a7e00000)
  
libm.so.6 => /lib64/libm.so.6 (0x0000003996400000)
  
libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00000039a5600000)
  
libc.so.6 => /lib64/libc.so.6 (0x0000003995800000)
  
/lib64/ld-linux-x86-64.so.2 (0x0000003995400000)
  
第一列: 程序需要依赖什么库
  
第二列: 系统提供的与程序需要的库所对应的库
  
第三列: 库加载的开始地址
  
通过上面的信息，我们可以得到以下几个信息:

通过对比第一列和第二列，我们可以分析程序需要依赖的库和系统实际提供的，是否相匹配
  
通过观察第三列，我们可以知道在当前的库中的符号在对应的进程的地址空间中的开始位置
  
如果依赖的某个库找不到，通过这个命令可以迅速定位问题所在；

注解

原理:  ldd不是个可执行程式，而只是个shell脚本； ldd显示可执行模块的dependency的工作原理，其实质是通过ld-linux.so (elf动态库的装载器) 来实现的。ld-linux.so模块会先于executable模块程式工作，并获得控制权，因此当上述的那些环境变量被设置时，ld-linux.so选择了显示可执行模块的dependency。

[https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/ldd.html](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/ldd.html)
