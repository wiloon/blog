---
title: is not in the sudoers file
author: wiloon
type: post
date: 2011-09-23T09:33:02+00:00
url: /?p=902
views:
  - 3
bot_views:
  - 6
categories:
  - Linux

---
首需要切换到root身份
  
$su &#8211;
  
(注意有- ，这和su是不同的，在用命令&#8221;su&#8221;的时候只是切换到root，但没有把root的环境变量传过去，还是当前用户的环境变量，用&#8221;su -"命令将环境变量也一起带过去，就象和root登录一样)

然后
  
$visudo //切记，此处没有vi和sudo之间没有空格
  
或 emacs /etc/sudoers
  
1、移动光标，到最后一行
  
2、按a，进入append模式
  
3、输入
  
your\_user\_name ALL=(ALL) ALL
  
4、按Esc
  
5、输入“:w”(保存文件)
  
6、输入“:q”(退出)