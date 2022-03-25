---
title: "相互转换逗号分隔的字符串和List"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "相互转换逗号分隔的字符串和List"

https://blog.csdn.net/yywusuoweile/article/details/50315377

将逗号分隔的字符串转换为List

方法 1:  利用JDK的Arrays类

String str = "a,b,c";
List<String> result = Arrays.asList(str.split(","));

方法 2:  利用Guava的Splitter
String str = "a, b, c";
List<String> result = Splitter.on(",").trimResults().splitToList(str);

方法 3:  利用Apache Commons的StringUtils  (只是用了split)
String str = "a,b,c";
List<String> result = Arrays.asList(StringUtils.split(str,","));

方法 4: 利用Spring Framework的StringUtils

String str = "a,b,c";
List<String> str = Arrays.asList(StringUtils.commaDelimitedListToStringArray(str));

将List转换为逗号分隔符
方法 1:  利用JDK  (好像没有很好的方法，需要一步一步实现) 

NA

方法 2:  利用Guava的Joiner

List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = Joiner.on(",").join(list);


方法 3:  利用Apache Commons的StringUtils

List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = StringUtils.join(list.toArray(), ",");

方法 4: 利用Spring Framework的StringUtils
List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");
String str = StringUtils.collectionToDelimitedString(list, ",");


比较下来，我的观点就是Guava库更灵活，适用面更广。项目中如果没有引入Guava的话，那就加上它。