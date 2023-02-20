---
title: windows bat basic
author: "-"
date: 2013-04-17T12:40:36+00:00
url: /?p=5406
categories:
  - inbox
tags:
  - reprint
---
## windows bat basic

### @echo off

@echo off
关闭回显

@echo on
打开回显

@echo off并不是DOS程序中的,
而是DOS批处理中的。
当年的DOS,所有操作都用键盘命令来完成,
当你每次都要输入相同的命令时,
可以把这么多命令存为一个批处理,
从此以后,只要运行这个批处理,
就相当于打了几行、几十行命令。

DOS在运行批处理时,
会依次执行批处理中的每条命令,
并且会在显示器上显示,
如果你不想让它们显示,
可以加一个"echo off"

当然,"echo off"也是命令,
它本身也会显示,
如果连这条也不显示,
就在前面加个"@"。

pause
使显示器停下,并显示"请按任意键继续"

例如:
@echo off
@echo hello!
pause

显示如下图hello1

@echo on
@echo hello!
pause
显示如下图hello2

## 注释

```bash
rem comments0
:: comments1

```

rem和::都起到注释的作用,然而又有些不同。
一、
rem是一条命令, 在运行的时候相当于把 rem 本身及其后面的内容置空。既然它是一条命令,就必须处于单独的一行或者有
类似"&"的连接符号连接。
二、
批处理遇到以冒号":"开头的行时 (忽略冒号前的空格) ,会将其后的语句识别为"标记"而不是命令语句,因此类似
":label"这样的东西在批处理中仅仅是一个标记。
三、
对于"::"而言,之所以可以达到注释的效果,是因为第二个:不是标签的合法字符 (把它换成\;.等等都行) ,它不被当
作一个合法的标签
这一点很好理解,如果在你的批处理中有一个永远用不到的标签hero,那么你就可以用":hero"打头来作为注释。只不过
冒号有其先天的优越性--语法上的问题。
好了,我们现在回过头来看看call。比如"call:hero",为什么要有冒号？这是为了与文件hero区分。
四、
嗯,我想你已经明白我的意思了,下面我将为你解释一些奇妙的东西。
经验告诉我们,在复合语句中使用":"经常会出问题。那么究竟什么时候会出现问题？

### sleep
在批次檔(*.bat)中內建並沒有 SLEEP 命令,當你在執行批次任務時若需要暫停執行幾秒鐘,就需要一些小技巧來實現了,以下分享幾個我之前用過的技巧: 

**1. 利用 PING 指令幫忙停 5 秒**

每壹台電腦都有 PING 執行檔,這個最好用啦!

  @ping 127.0.0.1 -n 5 -w 1000 > nul

**2. 利用 CHOICE 指令**

CHOICE 命令在 Windows XP 中找不到,但在 Windows Server 2003 或 Vista 都有內建。

  @CHOICE /C YN /N /T 5 /D y > nul


**3. 安裝 **Windows Server 2003 Resource Kit Tools** 即可獲得 sleep.exe 工具**

預設安裝路徑在 **C:Program FilesWindows Resource KitsTools** 目錄下會有個 sleep.exe 執行檔

  sleep 5

**4. 利用 TIMEOUT 指令**

TIMEOUT 命令在 Windows Server 2003 或 Vista 之後都有內建。

  timeout /t 5
http://blog.miniasp.com/post/2009/06/24/Sleep-command-in-Batch.aspx

### setlocal enabledelayedexpansion: 设置本地为延迟扩展
setlocal enabledelayedexpansion: 设置本地为延迟扩展

在cmd执行命令前会对脚本进行预处理,其中有一个过程是变量识别过程,在这个过程中,如果有两个%括起来的如%value%类似这样的变量,就会对其进行识别,并且查找这个变量对应的值,再而将值替换掉这个变量,这个替换值的过程,就叫做变量扩展,然后再执行命令。


为了更好的说明问题,先引入一个例子。
例1:
复制代码 代码如下:
@echo off
set a=4
set a=5&echo %a%
pause

结果: 4
解说: 为什么是4而不是5呢？在echo之前明明已经把变量a的值改成5了？让我们先了解一下批处理运行命令的机制: 批处理读取命令时是按行读取的 (另外例如for命令等,其后用一对圆括号闭合的所有语句也当作一行) ,在处理之前要完成必要的预处理工作,这其中就包括对该行命令中的变量赋值。我们现在分析一下例1,批处理在运行到这句"set a=5&echo %a%"之前,先把这一句整句读取并做了预处理——对变量a赋了值,那么%a%当然就是4了！ (没有为什么,批处理就是这样做的。) 而为了能够感知环境变量的动态变化,批处理设计了变量延迟。简单来说,在读取了一条完整的语句之后,不立即对该行的变量赋值,而会在某个单条语句执行之前再进行赋值,也就是说"延迟"了对变量的赋值。那么如何开启变量延迟呢？变量延迟又需要注意什么呢？


举个例子说明一下: 
例2:
复制代码 代码如下:
@echo off
setlocalenabledelayedexpansion
set a=4
set a=5&echo !a!
pause

结果: 5
解说: 由于启动了变量延迟,得到了正确答案。变量延迟的启动语句是"setlocalenabledelayedexpansion",并且变量要用一对叹号"!!"括起来 (注意要用英文的叹号) ,否则就没有变量延迟的效果。分析一下例2,首先"setlocalenabledelayedexpansion"开启变量延迟,然后"set a=4"先给变量a赋值为4,"set a=5&echo !a!"这句是给变量a赋值为5并输出 (由于启动了变量延迟,所以批处理能够感知到动态变化,即不是先给该行变量赋值,而是在运行过程中给变量赋值,因此此时a的值就是5了) 。