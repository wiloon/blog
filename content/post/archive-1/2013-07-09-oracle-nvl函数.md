---
title: Oracle Nvl函数
author: w1100n
type: post
date: 2013-07-09T06:01:30+00:00
url: /?p=5628
categories:
  - DataBase

---
以下的文章主要介绍的是[Oracle Nvl][1]函数，本文主要介绍的是其实际应用语法，以及实际应用的参数的介绍，以下就是相关的具体内容的相关描述，希望在你浏览之后会对你今后的学习中会有所帮助。

nvl( ) 函数

从两个表达式返回一个非 null 值。

语法

  1. NVL(eExpression1, eExpression2)

参数

  1. eExpression1, eExpression2

如果 eExpression1 的计算结果为 null 值，则 NVL( ) 返回 eExpression2。如果 eExpression1 的计算结果不是 null 值，则返回 eExpression1。eExpression1 和 eExpression2 可以是任意一种数据类型。如果 eExpression1 与 eExpression2 的结果皆为 null 值，则 NVL( ) 返回 .NULL.。

返回值类型

字符型、日期型、日期时间型、数值型、货币型、逻辑型或 null 值

说明

在不支持 null 值或 null 值无关紧要的情况下，可以使用 NVL( ) 来移去计算或操作中的 null 值。

  1. select nvl(a.name,'空得') as name from student a join school b on a.ID=b.ID

 [1]: http://database.51cto.com/art/200511/12457.htm