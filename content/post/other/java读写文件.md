---
title: java读写文件
author: "-"
date: 2012-09-27T02:31:11+00:00
url: /?p=4340
categories:
  - Java
tags:
  - reprint
---
## java读写文件

Java获取当前路径
1. 利用System.getProperty()函数获取当前路径: 
System.out.println(System.getProperty("user.dir"));//user.dir指定了当前的路径

2. 使用File提供的函数获取当前路径: 
File directory = new File("");//设定为当前文件夹
try{
    System.out.println(directory.getCanonicalPath());//获取标准的路径
    System.out.println(directory.getAbsolutePath());//获取绝对路径
}catch(Exceptin e){}

File.getCanonicalPath()和File.getAbsolutePath()大约只是对于new File(".")和new File("..")两种路径有所区别。

# 对于getCanonicalPath()函数，"."就表示当前的文件夹，而".."则表示当前文件夹的上一级文件夹
# 对于getAbsolutePath()函数，则不管"."、".."，返回当前的路径加上你在new File()时设定的路径
# 至于getPath()函数，得到的只是你在new File()时设定的路径
  
    http://sharewind.iteye.com/blog/227538
  
  
    ```java 
    
    
      //=============================写文件
    
    
    
      package fier;
    
    
    
      import java.io.*;
    
    
    
      public class write {
    
    
    
      public static void main(String[] args) {
    
    
    
      write("E:\123.txt", "hello");
    
    
    
      }
    
    
    
      public static void write(String path, String content) {
    
    
    
      String s = new String();
    
    
    
      String s1 = new String();
    
    
    
      try {
    
    
    
      File f = new File(path);
    
    
    
      if (f.exists()) {
    
    
    
      System.out.println("文件存在");
    
    
    
      } else {
    
    
    
      System.out.println("文件不存在，正在创建...");
    
    
    
      if (f.createNewFile()) {
    
    
    
      System.out.println("文件创建成功！");
    
    
    
      } else {
    
    
    
      System.out.println("文件创建失败！");
    
    
    
      }
    
    
    
      }
    
    
    
      BufferedReader input = new BufferedReader(new FileReader(f));
    
    
    
      while ((s = input.readLine()) != null) {
    
    
    
      s1 += s + "n";
    
    
    
      }
    
    
    
      System.out.println("文件内容: " + s1);
    
    
    
      input.close();
    
    
    
      s1 += content;
    
    
    
      BufferedWriter output = new BufferedWriter(new FileWriter(f));
    
    
    
      output.write(s1);
    
    
    
      output.close();
    
    
    
      } catch (Exception e) {
    
    
    
      e.printStackTrace();
    
    
    
      }
    
    
    
      }
    
    
    
      }
    
    
    
      //=============================读文件
    
    
    
      package fier;
    
    
    
      import java.io.BufferedReader;
    
    
    
      import java.io.File;
    
    
    
      import java.io.FileInputStream;
    
    
    
      import java.io.FileNotFoundException;
    
    
    
      import java.io.InputStreamReader;
    
    
    
      public class sdsd {
    
    
    
      /**
    
    
    
      * @param args
    
    
    
      */
    
    
    
      public static void main(String[] args) {
    
    
    
      read("E:\123.txt");
    
    
    
      }
    
    
    
      public static void read(String file) {
    
    
    
      String s = null;
    
    
    
      StringBuffer sb = new StringBuffer();
    
    
    
      File f = new File(file);
    
    
    
      if (f.exists()) {
    
    
    
      System.out.println("文件存在");
    
    
    
      try {
    
    
    
      BufferedReader br = new BufferedReader(new InputStreamReader(
    
    
    
      new FileInputStream(f)));
    
    
    
      while ((s = br.readLine()) != null) {
    
    
    
      sb.append(s);
    
    
    
      }
    
    
    
      System.out.println(sb);
    
    
    
      } catch (Exception e) {
    
    
    
      e.printStackTrace();
    
    
    
      }
    
    
    
      }else{
    
    
    
      System.out.println("文件不存在!");
    
    
    
      }
    
    
    
      }
    
    
    
      }
    
    
    
      ```
  
