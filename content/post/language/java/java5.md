---
title: java5
author: "-"
date: 2012-03-28T02:49:08+00:00
url: java5
tags:
  - Java
categories:
  - inbox
aliases:
  - /p642/
  - /p728/
  - /p2045/
  - /p2668/
  - /p3207/
  - /p3209/
  - /p3279/
  - /p3909/
  - /p3911/
  - /p3997/
  - /p4014/
  - /p4139/
  - /p4340/
  - /p4356/
  - /p4410/
  - /p4585/
  - /p4961/
  - /p5029/
  - /p5083/
  - /p5981/
  - /p6399/
  - /p6461/
  - /p6513/
  - /p6518/
  - /p6658/
  - /p6700/
  - /p7847/
  - /p8122/
  - /p8392/
  - /p8447/
  - /p8842/
---
## java5

### 可变参数, 变长参数

在 Java 5 中提供了变长参数，允许在调用方法时传入不定长度的参数。变长参数是 Java 的一个语法糖，本质上还是基于数组的实现: 

    public class Varargs {

        public static void test(String... args) {
            for(String arg : args) {
                System.out.println(arg);
            }
        }

        public static void main(String[] args) {
            test();//0个参数
            test("a");//1个参数
            test("a","b");//多个参数
            test(new String[] {"a", "b", "c"});//直接传递数组
        }
    }

