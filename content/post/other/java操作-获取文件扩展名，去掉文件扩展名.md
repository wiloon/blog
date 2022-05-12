---
title: JAVA操作——获取文件扩展名，去掉文件扩展名
author: "-"
date: 2012-09-04T09:37:25+00:00
url: /?p=4014
categories:
  - Java
tags:$
  - reprint
---
## JAVA操作——获取文件扩展名，去掉文件扩展名
http://blog.csdn.net/redoffice/article/details/6652731

```java

/*

 * Java文件操作 获取文件扩展名

 *

 * Created on: 2011-8-2

 * Author: blueeagle

 */

 public static String getExtensionName(String filename) {

 if ((filename != null) && (filename.length() > 0)) {

 int dot = filename.lastIndexOf('.');

 if ((dot >-1) && (dot < (filename.length() - 1))) {

 return filename.substring(dot + 1);

 }

 }

 return filename;

 }

/*

 * Java文件操作 获取不带扩展名的文件名

 *

 * Created on: 2011-8-2

 * Author: blueeagle

 */

 public static String getFileNameNoEx(String filename) {

 if ((filename != null) && (filename.length() > 0)) {

 int dot = filename.lastIndexOf('.');

 if ((dot >-1) && (dot < (filename.length()))) {

 return filename.substring(0, dot);

 }

 }

 return filename;

 }


```