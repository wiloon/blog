---
title: java hashcode
author: "-"
date: 2012-09-21T09:03:40+00:00
url: /?p=4169
categories:
  - Java
tags:$
  - reprint
---
## java hashcode
## java hash code
hash code是一种编码方式，在Java中，每个对象都会有一个hashcode，Java可以通过这个hashcode来识别一个对象。至于hashcode的具体编码方式，比较复杂 (事实上这个编码是可以由程序员通过继承和接口的实现重写的) ，可以参考数据结构书籍。而hashtable等结构，就是通过这个哈希实现快速查找键对象。这是他们的内部联系，但一般编程时无需了解这些，只要知道hashtable实现了一种无顺序的元素排列就可以了。


两个对象值相同(x.equals(y) == true)，则一定有相同的hash code。


因为: Hash，一般翻译做"散列"，也有直接音译为"哈希"的，就是把任意长度的输入 (又叫做预映射， pre-image) ，通过散列算法，变换成固定长度的输出，该输出就是散列值。这种转换是一种压缩映射，也就是，散列值的空间通常远小于输入的空间，不同的输入可能会散列成相同的输出，而不可能从散列值来唯一的确定输入值。


以下是java语言的定义: 


1) 对象相等则hashCode一定相等；


2) hashCode相等对象未必相等。


这也涉及到如何写自定义的hashCode方法的问题: 必须符合以上条件。注意条件2中的未必。具体可参见java doc; Effective Java中有更详细论述。


补充一点个人简介 hash 就是 类似于数学集合， 每一个键，k可以对应一个或多个值，对象就类似于值，所以"相同的对象"具有相同的键值，也就是hashCode;