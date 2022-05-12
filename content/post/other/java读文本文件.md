---
title: JAVA读文本文件
author: "-"
date: 2012-09-02T04:14:58+00:00
url: /?p=3997
categories:
  - Java
tags:$
  - reprint
---
## JAVA读文本文件
一行一行的读~~

```java

public static void main(String[] args) throws Exception {
  
FileReader reader = new FileReader("D:\url.txt");
  
BufferedReader br = new BufferedReader(reader);
  
String s1 = null;
  
while((s1 = br.readLine()) != null) {
  
System.out.println(s1);
  
}
  
br.close();
  
reader.close();
  
}

```