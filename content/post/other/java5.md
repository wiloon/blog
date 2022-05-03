---
title: java5
author: "-"
date: 2012-03-28T02:49:08+00:00
url: /?p=2668
tags:
  - Java

categories:
  - inbox
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

