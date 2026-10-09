---
title: "相互转换逗号分隔的字符串和 List"
author: "-"
date: ""
lastmod: 2026-10-09T21:22:13+08:00
url: string-list
categories:
  - Java
tags:
  - Inbox
  - java
  - remix
  - AI-assisted
---
## "相互转换逗号分隔的字符串和List"

https://blog.csdn.net/yywusuoweile/article/details/50315377

将逗号分隔的字符串转换为List

方法 1:  利用JDK的Arrays类

```java
String str = "a,b,c";
List<String> result = Arrays.asList(str.split(","));
```

方法 2:  利用Guava的Splitter

```java
String str = "a, b, c";
List<String> result = Splitter.on(",").trimResults().splitToList(str);
```

方法 3:  利用Apache Commons的StringUtils  (只是用了split)

```java
String str = "a,b,c";
List<String> result = Arrays.asList(StringUtils.split(str,","));
```

方法 4: 利用Spring Framework的StringUtils

```java
String str = "a,b,c";
List<String> str = Arrays.asList(StringUtils.commaDelimitedListToStringArray(str));
```

将List转换为逗号分隔符
方法 1:  利用JDK  (好像没有很好的方法，需要一步一步实现) 

NA

方法 2:  利用Guava的Joiner

```java
List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = Joiner.on(",").join(list);
```

方法 3:  利用Apache Commons的StringUtils

```java
List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = StringUtils.join(list.toArray(), ",");
```

方法 4: 利用Spring Framework的StringUtils

```java
List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = StringUtils.collectionToDelimitedString(list, ",");
```

比较下来，我的观点就是Guava库更灵活，适用面更广。项目中如果没有引入Guava的话，那就加上它。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；title 改为「相互转换逗号分隔的字符串和 List」；url 改为 `string-list`；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
