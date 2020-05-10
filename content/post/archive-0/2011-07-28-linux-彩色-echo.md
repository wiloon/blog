---
title: linux 彩色 echo
author: wiloon
type: post
date: 2011-07-28T04:34:33+00:00
url: /?p=369
bot_views:
  - 5
views:
  - 1
categories:
  - Linux
tags:
  - Shell

---
[shell]
  
#黑底红字
  
echo -e &#8216;E[31;40mThis prints in red.&#8217;; tput sgr0
  
[/shell]

[shell]
  
#!/bin/bash
  
echo -e &#8216;E[COLOR1;COLOR2mSome text goes here.&#8217;
  
[/shell]

COLOR1: Foreground Color
  
COLOR2: Background Color

[shell]
  
#!/bin/bash
  
echo -e &#8216;E[32;40mThis prints in green.&#8217;; tput sgr0
  
echo -e:enable interpretation of backslash escapes
  
[/shell]

-e &#8220;允许 反斜杠 (对字符)的转义&#8221;
  
e[32;1m: 控制字体和背景颜色的转义字符，30~37是字体颜色、40~47是背景颜色
  
&#8220;m&#8221;终止该转义序列, 然后文本以结束的转义指定的属性显示.
  
tput sgr0: 把终端设置恢复为原样. 如果省略这一句会使后续在该终端的输出仍为xx色.

色彩 前景色 背景色
  
黑 30 40
  
红 31 41
  
绿 32 42
  
黄 33 43
  
蓝 34 44
  
洋红 35 45
  
青 36 46
  
白 37 47

note:!!!!
  
脚本开头一定是#!/bin/bash不是#!/bin/sh, 而且要用&#8221;./&#8221;执行, 否则是没有彩色出来的.