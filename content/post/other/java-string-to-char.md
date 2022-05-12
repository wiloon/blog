---
title: java string api
author: "-"
date: 2012-06-14T01:23:47+00:00
url: /?p=3528
categories:
  - Java
tags:$
  - reprint
---
## java string api
### 按tab分割
```java
String[] segments = line.split("\t"); //按tab分割
```
```java
char c="abc".charAt(1);

```

```java
/**
* 将元数据前补零，补后的总长度为指定的长度，以字符串的形式返回
* @param sourceDate
* @param formatLength
* @return 重组后的数据
*/
public static String frontCompWithZore(int sourceDate,int formatLength)
{
/*
* 0 指前面补充零
* formatLength 字符总长度为 formatLength
* d 代表为正数。
*/
String newString = String.format("%0"+formatLength+"d", sourceDate);
return newString;
}

```