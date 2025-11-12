---
title: MySQL coalesce
author: "-"
date: 2014-01-16T05:00:18+00:00
url: /?p=6215
categories:
  - Inbox
tags:
  - MySQL

---
## MySQL coalesce
coalesce函数表示可以返回参数中的第一个非空表达式,当你有N个参数时选取第一个非空值 (从左到右) 。

实例一: 

select coalesce (null,"carrot","apple") 

返回结果: carrot

实例二: 

select coalesce(1,"carrot","apple")

返回结果: 1

友情提示: coalesce里的参数如果是字符串的话,务必用单引号或者双引号廓起来；

这些语句可以直接在MySQL里运行。


http://hi.baidu.com/luoganet/item/7ec497dec10c88e2795daa1f