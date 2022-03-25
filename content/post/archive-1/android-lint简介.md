---
title: Android Lint简介
author: "-"
date: 2014-12-24T03:52:50+00:00
url: /?p=7129
categories:
  - Uncategorized

tags:
  - reprint
---
## Android Lint简介
http://hubingforever.blog.163.com/blog/static/17104057920129249497980/

英文原文: http://tools.android.com/tips/lint
  
参照文章: http://blog.csdn.net/thl789/article/details/8037473
  
一、简介
  
Android Lint是SDK Tools 16 (ADT 16)之后才引入的工具，通过它对Android工程源代码进行扫描和检查，可发现潜在的问题，以便程序员及早修正这个问题。Android Lint提供了命令行方式执行，还可与IDE (如Eclipse) 集成，并提供了html形式的输出报告。
  
由于Android Lint在最初设计时就考虑到了independent于IDE,所以它可以很方便的与项目中的其他自动系统 (配置/ Build / 测试等) 集成.
  
Android Lint主要用于检查以下这些错误: 
  
1. Missing translations (and unused translations)没有翻译的文本
  
2. Layout performance problems (all the issues the old layoutopt tool used to find, and more)
  
3. Unused resources未使用的冗余资源
  
4. Inconsistent array sizes (when arrays are defined in multiple configurations)在多个配置中的数组大小不一致文件
  
5. Accessibility and internationalization problems (hardcoded strings, missing contentDescription, etc)
  
6. Icon problems (like missing densities, duplicate icons, wrong sizes, etc)
  
7. Usability problems (like not specifying an input type on a text field)
  
8. Manifest errors
  
当然Android Lint远远不至检查以上的错误，更多的内容请参考《Android Lint 检查规则列表》
  
在Eclipse中可以在菜单Window->Preference->"Lint Eerro checking"中设置规则的检查级别，如图1所示。
  
检查级别可以是:
  
Default
  
Fatal
  
Errro
  
Waring
  
Information
  
Ingore(即不检查)