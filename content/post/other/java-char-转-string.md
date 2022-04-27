---
title: 'java char[] 转  String'
author: "-"
date: 2013-01-24T14:35:04+00:00
url: /?p=5076
categories:
  - Java

tags:
  - reprint
---
## 'java char[] 转  String'

```java
  
public class Test{

public static void main(String[] args){

char[] data={a,b,c};

String s=new String(data);

System.out.println(s);
  
char[] chars = s.toCharArray();

}

}

```
