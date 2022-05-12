---
title: java遍历目录及子目录下的文件
author: "-"
date: 2012-09-04T09:12:43+00:00
url: /?p=4009
categories:
  - Java
tags:$
  - reprint
---
## java遍历目录及子目录下的文件
http://blog.csdn.net/suncheng_hong/article/details/1671632

```java

package com.daacc.common;

  


  import java.io.File;

  


  public class FileManager {

  


  String dir = "";

  


  String temp = "";

  


  public String[] serachFiles(String dir) {

  


  File root = new File(dir);

  


  File[] filesOrDirs = root.listFiles();

  


  String[] result = new String[10];

  


  for (int i = 0; i < filesOrDirs.length; i++) {


  if (filesOrDirs[i].isDirectory()) {


  serachFiles(filesOrDirs[i].getAbsolutePath());


  } else {


  result[i] = filesOrDirs[i].getName();

  


  temp += filesOrDirs[i].getName() + ",";

  


  }


  }

  


  return temp.split(",");

  


  }

  


  /**


  * @param args


  */


  public static void main(String[] args) {


  FileManager fm = new FileManager();


  String[] files = fm.serachFiles("D:/abc");


  for (int i = 0; i < files.length; i++) {


  System.out.println("files[" + i + "]" + files[i]);


  }

  


  }


  }
  

  ```
