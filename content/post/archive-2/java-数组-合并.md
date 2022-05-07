---
title: java 数组 合并
author: "-"
date: 2016-03-25T04:04:05+00:00
url: /?p=8830
categories:
  - Uncategorized

tags:
  - reprint
---
## java 数组 合并
http://blog.csdn.net/jaycee110905/article/details/9179227


Java中如何把两个数组合并为一个
  
标签:  JavaArray合并数组
  
2013-06-26 14:54 22185人阅读 评论(1) 收藏 举报
  
分类: 
  
JAVA (39) 

目录(?)[+]

http://freewind.me/blog/20110922/350.html

在Java中,如何把两个String[]合并为一个？

看起来是一个很简单的问题。但是如何才能把代码写得高效简洁,却还是值得思考的。这里介绍四种方法,请参考选用。

一、apache-commons
  
这是最简单的办法。在apache-commons中,有一个ArrayUtils.addAll(Object[], Object[])方法,可以让我们一行搞定: 

String[] both = (String[]) ArrayUtils.addAll(first, second);
  
其它的都需要自己调用jdk中提供的方法,包装一下。

为了方便,我将定义一个工具方法concat,可以把两个数组合并在一起: 

static String[] concat(String[] first, String[] second) {}
  
为了通用,在可能的情况下,我将使用泛型来定义,这样不仅String[]可以使用,其它类型的数组也可以使用: 

static <T> T[] concat(T[] first, T[] second) {}
  
当然如果你的jdk不支持泛型,或者用不上,你可以手动把T换成String。

二、System.arraycopy()
  
 
  
static String[] concat(String[] a, String[] b) {
  
String[] c= new String[a.length+b.length];
  
System.arraycopy(a, 0, c, 0, a.length);
  
System.arraycopy(b, 0, c, a.length, b.length);
  
return c;
  
}
  
使用如下: 

String[] both = concat(first, second);
  
三、Arrays.copyOf()
  
在java6中,有一个方法Arrays.copyOf(),是一个泛型函数。我们可以利用它,写出更通用的合并方法: 

 
  
public static <T> T[] concat(T[] first, T[] second) {
  
T[] result = Arrays.copyOf(first, first.length + second.length);
  
System.arraycopy(second, 0, result, first.length, second.length);
  
return result;
  
}
  
如果要合并多个,可以这样写: 

 
  
public static <T> T[] concatAll(T[] first, T[]... rest) {
  
int totalLength = first.length;
  
for (T[] array : rest) {
  
totalLength += array.length;
  
}
  
T[] result = Arrays.copyOf(first, totalLength);
  
int offset = first.length;
  
for (T[] array : rest) {
  
System.arraycopy(array, 0, result, offset, array.length);
  
offset += array.length;
  
}
  
return result;
  
}
  
使用如下: 

String[] both = concat(first, second);
  
String[] more = concat(first, second, third, fourth);
  
四、Array.newInstance
  
还可以使用Array.newInstance来生成数组: 

 
  
private static <T> T[] concat(T[] a, T[] b) {
  
final int alen = a.length;
  
final int blen = b.length;
  
if (alen == 0) {
  
return b;
  
}
  
if (blen == 0) {
  
return a;
  
}
  
final T[] result = (T[]) java.lang.reflect.Array.
  
newInstance(a.getClass().getComponentType(), alen + blen);
  
System.arraycopy(a, 0, result, 0, alen);
  
System.arraycopy(b, 0, result, alen, blen);
  
return result;
  
}