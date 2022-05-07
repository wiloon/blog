---
title: java 7, jdk 7
author: "-"
date: 2017-03-25T01:59:05+00:00
url: /?p=9927
categories:
  - Inbox
tags:
  - reprint
---
## java 7, jdk 7

### 数字文字中的下划线

Java 7的一个特性是数字文字中的下划线。可以在任何数字文字的数字之间放置下划线，如：int，byte，short，float，long，double。在数字文字中使用下划线将它们分成组以获得更好的可读性。

```java
public class UnderscoreNumericLiterals {

    public static void main(String[] args) {
        long ccNumber = 1234_5678_9012_3456L;
        long ssn = 999_99_9999L;
        float pi =     3.14_15F;
        long hexadecimalBytes = 0xFF_EC_DE_5E;
        long hexadecimalWords = 0xCAFE_BABE;
        long maxOfLong = 0x7fff_ffff_ffff_ffffL;
        byte byteInBinary = 0b0010_0101;
        long longInBinary = 0b11010010_01101001_10010100_10010010;
        int add = 12_3 + 3_2_1;
        System.out.println("ccNumber="+ccNumber);
        System.out.println("ssn="+ssn);
        System.out.println("pi="+pi);
        System.out.println("hexadecimalBytes="+hexadecimalBytes);
        System.out.println("hexadecimalWords="+hexadecimalWords);
        System.out.println("maxOfLong="+maxOfLong);
        System.out.println("byteInBinary="+byteInBinary);
        System.out.println("longInBinary="+longInBinary);
        System.out.println("add="+add);
    }

}

```

>https://www.yiibai.com/java/underscores-in-numeric-literals-java-7-feature.html
https://www.ibm.com/developerworks/cn/java/j-lo-jdk7-1/

http://blog.ubone.com/blog/2014/11/18/java-7de-6ge-xin-te-xing/


http://www.infoq.com/cn/articles/jdk7-garbage-first-collector