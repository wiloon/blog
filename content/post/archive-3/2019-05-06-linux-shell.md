---
title: linux shell
author: wiloon
type: post
date: 2019-05-06T04:27:52+00:00
url: /?p=14295
categories:
  - Uncategorized

---
### 查看当前使用的shell

```bashecho $SHELL
ps |  grep $$  |  awk '{print $4}'
```

命令行式shell（Command Line Interface shell ，即CLI shell）
  
也就是通过命令行和计算机交互的shell。 Windows NT 系统下有 cmd.exe（命令提示字符）和近年来微软大力推广的 Windows PowerShell。 Linux下有bash / sh / ksh / csh／zsh等 一般情况下，习惯把命令行shell（CLI shell）直接称做shell，以后，如果没有特别说明，shell就是指 CLI shell，后文也是主要讲Linux下的 CLI shell。

```bashcat /etc/shells
```

3.1、bash
  
Bourne Again Shell 用来替代Bourne shell，也是目前大多数Linux系统默认的shell。

3.2、sh
  
Bourne Shell 是一个比较老的shell，目前已经被/bin/bash所取代，在很多linux系统上，sh已经是一个指向bash的链接了。 下面是CentOS release 6.5 的系统

sh\_to\_bash

3.3、csh／tcsh
  
C shell 使用的是“类C”语法,csh是具有C语言风格的一种shell，tcsh是增强版本的csh，目前csh已经很少使用了。

3.4、ksh
  
最早，bash交互体验很好，csh作为非交互式使用很爽，ksh就吸取了2者的优点。

3.5、zsh
  
zsh网上说的目前使用的人很少，但是感觉使用的人比较多。 zsh本身是不兼容bash的，但是他可以使用仿真模式（emulation mode）来模拟bash等，基本可以实现兼容。 在交互式的使用中，目前很多人都是zsh，因为zsh拥有很强大的提示和插件功能，炫酷吊炸天。推荐在终端的交互式使用中使用zsh，再安利一个插件Oh My Zsh 其实我个人的理解是，在终端中使用shell，基本上只是调用各种命令，比如：curl cat ls等等，基本不会使用到zsh的编程，所以终端中使用zsh是可以的。但是在写shell脚本的时候，需要考虑兼容性， 最主流的还是bash shell，所以，后文我们介绍的shell脚本也是bash shell的。

执行并获取返回结果，有点类似JavaScript 的eval函数。

#!/bin/bash
  
dt=`date` #反引号内的字符串会当作shell执行 ，并且返回结果。
  
echo "dt=${dt}&#8221;
  
Shell 变量
  
shell的使用比较简单，就像这样，并且没有数据类型的概念，所有的变量都可以当成字符串来处理：

#!/bin/bash
  
myName=&#8221;tom&#8221;
  
youName=&#8221;cat&#8221;

使用变量

ABC=&#8221;tom&#8221;
  
echo $ABC #使用变量前面加$美元符号
  
echo "ABC=$ABC&#8221; #可以直接在字符串里面引用
  
echo "ABC=${ABC}&#8221; #但是建议把变量名字用{}包起来
  
只读变量

ABC=&#8221;tom&#8221;
  
echo "ABC=${ABC}&#8221;
  
readOnly ABC #设置只读
  
ABC=&#8221;CAT&#8221; #会报错，因为设置了只读，不能修改

删除变量

ABC=&#8221;tom&#8221;
  
echo "ABC=${ABC}&#8221;
  
unset ABC #删除
  
echo "ABC=$ABC&#8221;
  
echo "ABC=${ABC}&#8221;

Shell 的字符串
  
使用字符串

NAME=&#8221;tom&#8221;
  
A=my #你甚至可以不用引号，但是字符串当中不能有空格，这种方式也不推荐
  
B=&#8217;my name is ${NAME}&#8217; #变量不会被解析
  
C=&#8221;my name is ${NAME}&#8221; #变量会解析
  
echo $A
  
echo $B
  
echo $C

https://my.oschina.net/u/2428064/blog/3045121