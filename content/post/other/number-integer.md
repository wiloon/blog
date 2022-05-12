---
title: number integer
author: "-"
date: 2013-06-28T01:45:21+00:00
url: /?p=5593
categories:
  - DataBase
tags:$
  - reprint
---
## number integer

建表的时候,如果是浮点数,一般设置为 number(m,n )[m为精度,n为小数位数,所以整数为m-n位],  整数设置为integer;

比如: 

create table abc
  
(  a number(38,0),
  
b number(38)
  
c integer,
  
d number
  
)

那么a,b,c,d 分别有什么区别呢?
  
a,b其实是一样的,都是38位的范围；
  
c是不是和a,b一样呢?测试后是不一样的,c的最大值可以达到9e125,显然远远地大于38位的范围；
  
d和a,b,c有什么区别呢,首先d可以放小数,另外它的范围同样远远大于38位；

具体这a,b,c,d四种类型的明确差异,我也说不清楚,希望有专家把它解释清楚,我这里只是抛砖引玉。

以前我一直以为 integer=number(38,0) -38是number的最大精度

刚才无意中发现integer 是个超大的数据类型,最大可以表示为power(10,126)-1
  
也就是说这么大的数字,大概需要多少个字节呢,

因为一个字节最大表示256,那么N个字节最大表示power(256,n)>=power(10,126)

现在求这个N: 解法是: 
  
select  LOG(256,10)*126   from dual
  
求得的解是 53, 也就是说,一个integer类型最少使用53个字节。

所以我觉得Integer类型还是尽量少用,一般很少用到这么大的数字；

特别是某些人对于boolean类型的处理；

因为Oracle的表结构中没有布尔类型,所以很多人干脆用integer 代替布尔类型,这个感觉有点"奢侈"；

我一般都用char(1) 表示布尔型；'0'表示false,'1'表示true

另外,比如varchar2(200)这个类型,它是动态分配的,所以字符串按实际使用的占用空间,但是integer却是固定暂用了最少53个字节,所以大部分时候,integer 类型还是不用为妙；

就算在pl/sql 里；
  
定义变量的时候,也不要使用integer;
  
可以用binary_integer 或pls_integer ；11g里还出了个新的整形,效率更高,叫simple_integer,反正最好不用integer就是了。

效率测试下来: simple_integer>pls_integer>binary_integer>integer;


### SIMPLE_INTEGER Subtype of PLS_INTEGER {#autoId14}

`SIMPLE_INTEGER` is a predefined subtype of the `PLS_INTEGER` data type that has the same range as `PLS_INTEGER` and has a `NOT` `NULL` constraint (explained in["NOT NULL Constraint"][1]). It differs significantly from `PLS_INTEGER` in its overflow semantics.

If you know that a variable will never have the value `NULL` or need overflow checking, declare it as `SIMPLE_INTEGER` rather than `PLS_INTEGER`. Without the overhead of checking for nullness and overflow, `SIMPLE_INTEGER` performs significantly better than `PLS_INTEGER`.

<http://www.itpub.net/thread-1261515-1-1.html>

<http://docs.oracle.com/cd/E11882_01/appdev.112/e17126/datatypes.htm#CIHGBFGB>

 [1]: http://docs.oracle.com/cd/E11882_01/appdev.112/e17126/fundamentals.htm#CIHCJJAG