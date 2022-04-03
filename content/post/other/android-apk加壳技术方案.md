---
title: Android APK加壳技术方案
author: "-"
date: 2014-03-20T07:21:35+00:00
url: /?p=6412
categories:
  - Uncategorized

tags:
  - reprint
---
## Android APK加壳技术方案
本文章由Jack_Jia编写,转载请注明出处。

文章链接: http://blog.csdn.net/jiazhijun/article/details/8678399

作者: Jack_Jia 邮箱:  309zhijun@163.com


一、什么是加壳？

加壳是在二进制的程序中植入一段代码,在运行的时候优先取得程序的控制权,做一些额外的工作。大多数病毒就是基于此原理。PC EXE文件加壳的过程如下: 


二、加壳作用

加壳的程序可以有效阻止对程序的反汇编分析,以达到它不可告人的目的。这种技术也常用来保护软件版权,防止被软件破解。


三、Android Dex文件加壳原理

PC平台现在已存在大量的标准的加壳和解壳工具,但是Android作为新兴平台还未出现APK加壳工具。Android Dex文件大量使用引用给加壳带来了一定的难度,但是从理论上讲,Android APK加壳也是可行的。

在这个过程中,牵扯到三个角色: 

1. 加壳程序: 加密源程序为解壳数据、组装解壳程序和解壳数据

2. 解壳程序: 解密解壳数据,并运行时通过DexClassLoader动态加载

3. 源程序: 需要加壳处理的被保护代码

阅读该文章,需要您对DEX文件结构有所了解,您可以通过以下网址了解相关信息: 

http://blog.csdn.net/jiazhijun/article/details/8664778


根据解壳数据在解壳程序DEX文件中的不同分布,本文将提出两种Android Dex加壳的实现方案。


 (一) 解壳数据位于解壳程序文件尾部


该种方式简单实用,合并后的DEX文件结构如下。


加壳程序工作流程: 

1. 加密源程序APK文件为解壳数据

2. 把解壳数据写入解壳程序Dex文件末尾,并在文件尾部添加解壳数据的大小。

3. 修改解壳程序DEX头中checksum、signature 和file_size头信息。

4. 修改源程序AndroidMainfest.xml文件并覆盖解壳程序AndroidMainfest.xml文件。


解壳DEX程序工作流程: 

1. 读取DEX文件末尾数据获取借壳数据长度。

2. 从DEX文件读取解壳数据,解密解壳数据。以文件形式保存解密数据到a.APK文件

3. 通过DexClassLoader动态加载a.apk。


 (二) 解壳数据位于解壳程序文件头


该种方式相对比较复杂, 合并后DEX文件结构如下: 


加壳程序工作流程: 

1. 加密源程序APK文件为解壳数据

2. 计算解壳数据长度,并添加该长度到解壳DEX文件头末尾,并继续解壳数据到文件头末尾。

 (插入数据的位置为0x70处) 

3. 修改解壳程序DEX头中checksum、signature、file_size、header_size、string_ids_off、type_ids_off、proto_ids_off、field_ids_off、

method_ids_off、class_defs_off和data_off相关项。 分析map_off 数据,修改相关的数据偏移量。

4. 修改源程序AndroidMainfest.xml文件并覆盖解壳程序AndroidMainfest.xml文件。


解壳DEX程序工作流程: 

1. 从0x70处读取解壳数据长度。

2. 从DEX文件读取解壳数据,解密解壳数据。以文件形式保存解密数据到a.APK

3. 通过DexClassLoader动态加载a.APK。


四、加壳及脱壳代码实现


http://blog.csdn.net/jiazhijun/article/details/8809542