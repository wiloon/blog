---
title: 获得Shell脚本所在目录的绝对路径
author: "-"
date: 2012-04-22T07:34:46+00:00
url: /?p=2993
categories:
  - shell
tags:
  - reprint
---
## 获得Shell脚本所在目录的绝对路径

[http://www.zeali.net/entry/497](http://www.zeali.net/entry/497)

要得到正在执行的程序/脚本自身所存放的绝对路径，在 PHP 里面可以用 dirname(realpath(__FILE__)) ； C# 则有 System.Windows.Forms.Application.StartupPath ； java 似乎没有什么比较直接的方法，只能[利用 CodeSource 来间接获取][1] 。而在 linux shell 脚本里面如果想得到当前脚本文件存放的绝对路径，也没有太现成的命令可以调用，不过可以通过下面的语句来获取:

baseDirForScriptSelf=$(cd "$(dirname "$0")"; pwd)
 echo "full path to currently executed script is : ${baseDirForScriptSelf}"

虽说大部分情况下我们并不需要这样的绝对路径来完成工作；但如果要把多个脚本、数据文件等内容打包作为一个整体来交付别人使用，又希望不论用户拷贝到哪个目录下执行脚本都能够正确的找到这个包里面的其他内容的话，用这样的脚本来自动定位包的根目录应该是个比较鲁棒的做法。

 [1]: http://www.zeali.net/entry/404 "获得jar包存放路径的方法"
