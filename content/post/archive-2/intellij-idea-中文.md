---
title: IntelliJ IDEA
author: "-"
date: 2017-07-11T08:05:30+00:00
url: /?p=10819
categories:
  - Inbox
tags:
  - reprint
---
## IntelliJ IDEA
    IntelliJ IDEA Windows JBR是什么

https://www.4spaces.org/what-is-intellij-idea-jbr/embed/#?secret=ZFT4esKgN4

### idea without JBR

JBR是指JetBrains Runtime,JetBrains Runtime是一个运行时环境,用于在Windows,macOS和Linux上运行基于IntelliJ Platform的产品。 JetBrains Runtime基于OpenJDK项目并进行了一些修改。 这些修改包括: 亚像素抗锯齿(Subpixel Anti-Aliasing),Linux上的增强字体渲染,HiDPI支持,连字(ligatures),macOS上的San Francisco字体系列支持,官方构建中未提供的本机崩溃的一些修复,以及其他小的增强功能。

JetBrains Runtime与所有JetBrains IDE的最新版本捆绑在一起,默认情况下使用,除非执行显式重新配置。 例外是32位Linux系统,其中IDE需要单独的JDK安装,因为目前只捆绑了64位JetBrains Runtime。 对于Windows,捆绑了32位JetBrains Runtime,它可以在32位和64位系统上运行。

### 中文

IntelliJ IDEA是一个非常强大的IDE,但是只有英文版,且默认的中文显示有一定问题。本文介绍了IntelliJ IDEA 12.0中文显示问题解决方案。

IDE本身的中文乱码
  
这个问题体现在IDE本身,比如打开文件浏览目录的时候,中文名的文件或目录会显示成方块。
  
解决方法: 

进入设置页。File->Settings。
  
进入IDE Settings里的File Encodings项,把IDE Encoding项设置成UTF-8。确定。
  
进入IDE Settings里的Appearance项,选中Override default fonts by,把Name设置为你喜欢的字体 (我使用的是Yahei Consolas Hybrid) ,Size根据自己喜好设置 (我一般设为 14) 。确定。
  
以上应该可以保证中文显示没有问题了。

编辑器的中文问题
  
这个问题体现在代码编辑区中写中文时,可能会乱码或者中文汉子全部重叠在一起。
  
首先要确定你正在编辑的文件是UTF-8编码的,有很多文件可能默认是ANSI编码。

至于中文重叠那是因为你所选用的默认中文字体不对,一直以来我写代码都是用的consolas,但是这个字体不支持中文,Intellij IDEA 12中如果使用默认的中文字体 (不知道是哪个字体) 就会重叠在一起,在网上找了好久,终于找到一个神一般的字体Yahei Consolas Hybrid,即微软雅黑和consolas的混合！

于是乎,File->Settings IDE Settings->Editor->Color & Fonts->Font,设置字体为Yahei Consolas Hybrid即可。

神一般的字体Yahei Consolas Hybrid下载

如果发现安装了这个字体但是在设置中找不到的话,尝试使用以下这个方法: 
  
按图所示,保存为另外一个名字,由你喜欢。最好是英文字母组成,这里我们保存为Darcula1。

Intellij IDEA 12 设置字体
  
在此路径 (win7) "C:\Users\你的计算机名.IntelliJIdea12\config\colors"找到Darcula1.xml文件。
  
用记事本打开Darcula1.xml文件,把第8行改为然后重启IntelliJ IDEA 12.0,中文字符问题解决,
  
http://www.cnblogs.com/vhua/p/idea_1.html