---
title: vim宏录制
author: "-"
date: ""
url: ""
categories:
  - Editor
tags:
  - VIM
---
## vim宏录制

在编辑某个文件的时候,可能会出现需要对某种特定的操作进行许多次的情况,以编辑下面的文件为例:

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

    ;=====================================================================================;This is a sample configuration file when upgrading XXX using InstallShield.;Author:        ini_always;Date:          8/24/2011;Last modified: 9/20/2011;Note: Install script does NOT verify whether the configuration file is in a "WELL";format, a WRONG format may lead to installation failure.;If more information is needed, please check the document for details.;=====================================================================================

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

这是一个ini类型的配置文件,可以看到每一行的最前面有一个逗号,现在如果需要将每行前面的逗号去掉,怎么办？在第一行行首按x,然后按j,然后按x...这样重复下去？确实,我最开始也是这样的,但如果这个文件有100行要这样修改呢？或者1000行？

好吧,少废话,进入正题。所谓宏,在vim里面是指某种特定顺序的一系列操作,我们可以录制自己的操作序列,然后重复这个序列多次,以简化某种重复的操作。vim宏有录制和播放的过程,录制就是你教给vim该怎么操作,播放就是vim照着你教的进行自动操作。因此,对于上面的文件处理,首先要进行宏录制:

1. 把光标定位在第一行；
2. 在normal模式下输入qa(当然也可以输入qb, qc, etc,这里的a, b, c是指寄存器名称,vim会把录制好的宏放在这个寄存器中)(PS: 如果不知道什么是vim的寄存器,请自行放狗搜之)；
3. 正常情况下, vim的命令行会显示"开始录制"的字样,这时候,把光标定位到第一个字符 (按0或者|) ,再按x删除,按j跳到下一行；
4. normal模式下输入q,结束宏录制。

好了,经过以上步骤,我们定义了一个存储在寄存器a中的宏,它的操作序列是: 0->x->j,也就是跳到行首,删除,跳到下一行。

现在,第一行已经删除了行首的逗号,而且光标也已经在第二行,现在,在normal模式下输入@a,以播放我们刚录制好的存在寄存器a中的宏。于是,第二行行首的逗号也被删除,光标停在了第三行。

这也不简单啊？你肯定会这样想,要删除100行,我还得输入100个@a,我还不如手动删除呢。呵呵,vim早就想到了,输入7@a,好了,剩下的7行全部搞定了。 (PS: 在命令前面加数字,就是代表要执行这个命令多少次)

当然,这个例子很简单,但也很典型。利用好vim的宏,可以使一些原本很无聊的工作要简单很多。

[https://www.cnblogs.com/ini_always/archive/2011/09/21/2184446.html](https://www.cnblogs.com/ini_always/archive/2011/09/21/2184446.html "https://www.cnblogs.com/ini_always/archive/2011/09/21/2184446.html")
