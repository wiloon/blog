---
title: kvm 快捷键
author: "-"
date: 2011-12-12T12:53:24+00:00
url: /?p=1871
categories:
  - Linux
  - VM
tags:
  - KVM

---
## kvm 快捷键
在图形模拟时,我们可以使用下面的这些组合键:

**Ctrl-Alt-f**
:   全屏

**Ctrl-Alt-n**
:   切换虚拟终端'n'.标准的终端映射如下:

  * n=1 : 目标系统显示
  * n=2 : 临视器
  * n=3 : 串口 
    **Ctrl-Alt**
    :   抓取鼠标和键盘在虚拟控制台中,我们可以使用Ctrl-Up, Ctrl-Down, Ctrl-PageUp 和 Ctrl-PageDown在屏幕中进行移动. 

在模拟时,如果我们使用\`-nographic'选项,我们可以使用Ctrl-a h来得到终端命令:

**Ctrl-a h**
:   打印帮助信息

**Ctrl-a x**
:   退出模拟

**Ctrl-a s**
:   将磁盘信息保存入文件(如果为-snapshot)

**Ctrl-a b**
:   发出中断

**Ctrl-a c**
:   在控制台与监视器进行切换

**Ctrl-a Ctrl-a**
:   发送Ctrl-a