---
title: apache commons StringUtils
author: "-"
date: 2014-03-21T12:40:05+00:00
url: /?p=6430
categories:
  - Uncategorized
tags:
  - Java

---
## apache commons StringUtils
<http://vipcowrie.iteye.com/blog/1513017>

org.apache.commons.lang.StringUtils

StringUtils是apache commons lang库 (http://commons.apache.org/lang)旗下的一个工具类,提供了很多有用的处理字符串的方法,本文不打算把所有的方法都介绍一遍,我会介绍一些精选的常用的给大家。

目前StringUtils有两个版本可用,分别是较新的org.apache.commons.lang3.StringUtils和较老的org.apache.commons.lang.StringUtils,他们有比较大的区别,前者需要JAVA 5,我想这个应该是我们希望使用的。

1) public static boolean equals(CharSequence str1,CharSequence str2)

我们就先从最简单的方法equals开始,和你想的一样,他需要两个字符串参数,当相同的时候返回true,否则返回false。

但是java.lang.String已经有现成的比较完美的equals方法了,为何我们还需要一个第三方的实现呢？

这个问题很好,让我们来看看下面这些代码,看看有何问题？

Java代码 收藏代码

public void doStuffWithString(String stringParam) {

if(stringParam.equals("MyStringValue")) {

// do stuff }

}

这个可能有NullPointerException出现,那么有几个办法处理: 

Java代码 收藏代码

public void safeDoStuffWithString1(String stringParam) {

if(stringParam != null &&

stringParam.equals("MyStringValue")) {

// do stuff

}

}

public void safeDoStuffWithString2(String stringParm) {

if("MyStringValue".equals(stringParam))

{

// do stuff

}

}

我本人不喜欢上面的两个方法,第一个看起来太臃肿,第二个看起来像错误的。这里我们就可以用一些StringUtils类了,这个类提供的equals方法是空指针安全的,不用担心传递给他的是什么参数,他不会抛出空指针异常,这样写: 

Java代码 收藏代码

public void safeDoStuffWithString3(String stringParam) {

if(StringUtils.equals(stringParam,"MyStringValue))

{

// do stuff

}

}

这个是我个人的喜好,但是这个确实看起来比较简单易读。前面的两个方法虽然么有什么问题,但是我想StringUtils.equals还是值得考虑的。

2) isEmpty,isNotEmpty,isBlank,isNotBlank

和前面一样,这些方法相对于jdk提供的isEmpty方法来说,多了一个"空指针安全",即不用考虑传递参数的空值问题,让我们来看一个例子: 

Java代码 收藏代码

if(myString != null && !myString.isEmpty()) {

// 有点臃肿是把？

// Do stuff with myString

}

if(StringUtils.isNotEmpty(myString)) { // 好多了吧

// Do stuff with myString

}

Blank和empty的区别

isBlank将在字符串含有空白字符的时候,返回true,例如: 

Java代码 收藏代码

String someWhiteSpace = " \t \n";

StringUtils.isEmpty(someWhiteSpace); // false

StringUtils.isBlank(someWhiteSpace); // true

3) public static String[] split(String str,String separatorChars)

当然,这个方法相对于String.split也是空指针安全的,当你尝试split一个null字符串的时候,将返回Null,一个Null的分隔符将按照空白字符分隔字符串,但是,还有一个理由让你可考虑使用StringUtils.split () 方法,就是jdk自带的String.split由于支持正则表达式进行分隔,所以可能带来意想不到的后果,例如:

Java代码 收藏代码

public void possiblyNotWhatYouWant() {

String contrivedExampleString = "one.two.three.four";

String[] result = contrivedExampleString.split(".");

System.out.println(result.length); // 0

}

上面很明显你希望按照.分隔,但是jdk理解的"."是正则表达式的任意字符,导致字符串内任意字符都匹配,返回一个size=0的字符串数组。其实你只要传递"\\."就行了,但是这个确实是一个问题。

这样,使用StringUtils.split就简单多了,另外,我测试还发现StringUtils.split比jdk自带的split要快四倍。

4) public static String join(Iterable iterable,String separator) 

这个方法确实很实用,因为jdk自身没有提供,简单使用方法: 

Java代码 收藏代码

String[] numbers = {"one", "two", "three"};

StringUtils.join(numbers,","); // returns "one,two,three"

当然你可以传递一个数字或者迭代序列iterators.

好了,我确信,这个库确实是一个比较实用的库,推荐大家使用。

API请参考:http://commons.apache.org/lang/api-3.1/org/apache/commons/lang3/StringUtils.html