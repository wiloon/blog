---
title: Map, Dictionary
author: "-"
date: 2012-09-27T09:34:36+00:00
url: /?p=4345
categories:
  - Java
tags:$
  - reprint
---
## Map, Dictionary
### Dictionary

Dictionary 是 Hashtable 的抽象父类，在 java.util包下，他的子类有 Hashtable, Properties. 它的主要作用是用于记录 键到值的一一对应关系。没错，从数学的概念上讲，这种映射关系就是一对一的。也就是说，一个key最多只能找到一个value. 如果给出一个 Dictionary 的子类对象和一个 key， 就可以查找有没有包含相关的元素。需要注意的是：任何非空(non-null)的对象才能用作 key 和 value.

通常，类的实现应使用 equals 方法来确定两个键是否相同。

**注意：此类已过时。 新的实现应实现 Map 接口，而不是扩展此类。**

Map 接口
Map 是一个接口，还是看图：

Map 是一个将 keys 映射到 values 的对象。一个 map 对象不能包含重复的 keys. 每一个 key 最多只能映射到一个对象。
Map 这个接口是为了取代 Dictionary 这个抽象类的，更直白的说，就是拿一个接口去取代之前抽象类。

three collection views
Map 接口提供了三套查看方法来查看map所包含的内容。

查看它所包含的所有 keys (view as a set of keys)
查看它所包含的所有 values(view as collection of values)
查看它所包含的键-值映射。(view as a set of key-value mappings)

————————————————
版权声明：本文为CSDN博主「mysonghushu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/fudaxing/article/details/102937285