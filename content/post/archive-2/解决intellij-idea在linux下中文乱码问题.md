---
title: 解决Intellij Idea在linux下中文乱码问题
author: "-"
date: 2016-08-13T05:30:48+00:00
url: /?p=9176
categories:
  - Uncategorized

tags:
  - reprint
---
## 解决Intellij Idea在linux下中文乱码问题
>http://lan2720.github.io/2015/11/04/%E8%A7%A3%E5%86%B3Intellij-Idea%E5%9C%A8linux%E4%B8%8B%E4%B8%AD%E6%96%87%E4%B9%B1%E7%A0%81%E9%97%AE%E9%A2%98/ {#Problem}

## Problem

但是打开project的源码发现之前写的中文注释乱码: 

> 中文变成了口口口口口

网上搜到的大部分答案说

> 进入File Settings 里的 Appearance 项,选中Override default fonts by ,把 Name 设置为 微软雅黑

之前默认的font是ubuntu,很好看,换成微软雅黑整个界面丑了不止一个档次！所以,如果只是想让源码中的中文能正常显示的话,只能另寻他路。

## Solution {#Solution}

一个快速而有效的方法是: 

  * 在这里点download下载yahei字体的ttf
  * 在ubuntu 下可以执行下面操作安装该字体<figure class="highlight plain"> 


  
    
      1
    
    
    
sudo mkdir /usr/share/fonts/truetype/yahei
sudo cp yahei.ttf  /usr/share/fonts/truetype/yahei
fc-cache -f -v
    
  
</figure> 

这里的yahei.ttf是刚刚下载的文件的名字

  * 重启Intellij Idea,发现中文已经可以正常显示了！