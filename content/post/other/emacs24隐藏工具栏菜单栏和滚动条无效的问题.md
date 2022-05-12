---
title: Emacs24隐藏工具栏菜单栏和滚动条无效的问题
author: "-"
date: 2012-08-31T09:25:23+00:00
url: /?p=3979
categories:
  - Emacs
tags:
  - reprint
---
## Emacs24隐藏工具栏菜单栏和滚动条无效的问题
>http://blog.csdn.net/cherylnatsu/article/details/7663163


  
    前不久发布了Emacs 24.1，下载下来编译安装后发现这样一个问题，以前旧的.emacs文件里明确设置了不显示工具栏菜单栏滚动条，但是它还是都显示了出来，旧的配置是这样的。
  
  
    
      
      
    
    
    
      
        (tool-bar-mode nil)
      
      
        (menu-bar-mode nil)
      
      
        (scroll-bar-mode nil)
      
    
  
  
    后来经过提醒才发现，新版这里已经不能用nil了，必须用0
  
  
    改成: 
  
  
    
      
        (tool-bar-mode 0)
      
      
        (menu-bar-mode 0)
      
      
        (scroll-bar-mode 0)
      
    
  
  
    就好了。
  
