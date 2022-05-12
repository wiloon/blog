---
title: eclipse basic
author: "-"
date: 2011-06-05T03:07:03+00:00
url: /?p=223
categories:
  - Eclipse
  - Java
tags:$
  - reprint
---
## eclipse basic
### java 方法 注释
设置方法注释模板: 选择eclipse菜单栏中【窗口】下的【首选项】，展开左边树状结构, 到Java->代码样式->代码模板，展开右边出现的对话框中的注释->方法，点击右边的【编辑】按钮。编辑其中的内容。也可以点击下面的【插入变量】按钮添加变量。例如: 
  
/**
  
*@author${user}
  
*功能: 
  
*${tags}
  
*/
  
其中@author是JavaDoc的标示，带$符号的是变量。

使用时鼠标放置在需要添加注释的方法内部的任意位置。点击菜单栏中【源代码】下的【添加Javadoc注释】，或者使用快捷键Alt Shift J，则eclipse自动在该方法前面添加注释，例如public static void main(String[]args)生成如下注释: 
  
/**
  
* @authorhfm
  
*功能: 
  
* @param args
  
*/

当然添加完之后还需要手动添加其中的各项内容，如方法的功能和参数的含义等。