---
title: Oracle中的decimal与Number区别
author: wiloon
type: post
date: 2014-12-29T07:51:44+00:00
url: /?p=7139
categories:
  - Uncategorized

---
一、DECIMAL类型详细
  
Oracle只是在语法上支持decimal类型，但是在底层实际上它就是number类型，支持decimal类型是为了能把数据从Oracle数据库移到其他数据库中(如DB2等)。

因为decimal在Oracle底层就是number类型，所以就当number类型使用就可以了，如果需要对这种字段类型转为char类型可以用to_char函数对其转换。

decimal类型从根本上说应该是数字类型的,因为oracle内部的数据类型，对于数字只有number类型，都当数字类型进行处理即可。decimal(8,2)代表数字总共8位长度,小数部分是2位。范围是8位，精确到小数点后2位，并四舍五入，即存6位整数，两位小数。也就是最大值可以是999999.99,可存放2位小数。Oracle中,可以使用to_char函数对数字进行转换,使它变成字符类型.

二、NUMBER类型详细

在Oracle中Number类型可以用来存储0，正负定点或者浮点数，可表示的数据范围在

1.0 \* 10(-130) —— 9.9&#8230;9 \* 10(125) {38个9后边带88个0}
  
的数字，当Oracle中的数学表达式的值>=1.0*10(126)时，Oracle就会报错。

Number的数据声明如下：

表示
  
作用
  
说明
  
Number(p, s)
  
声明一个定点数
  
p(precision)为精度，s(scale)表示小数点右边的数字个数，精度最大值为38，scale的取值范围为-84到127
  
Number(p)
  
声明一个整数
  
相当于Number(p, 0)
  
Number
  
声明一个浮点数
  
其精度为38，要注意的是scale的值没有应用，也就是说scale的指不能简单的理解为0，或者其他的数。
  
定点数的精度(p)和刻度(s)遵循以下规则：

当一个数的整数部分的长度> p-s 时，Oracle就会报错

当一个数的小数部分的长度> s 时，Oracle就会舍入。

当s(scale)为负数时，Oracle就对小数点左边的s个数字进行舍入。

当s > p时, p表示小数点后第s位向左最多可以有多少位数字，如果大于p则Oracle报错，小数点后s位向右的数字被舍入.

NUMBER类型细讲

Oracle number datatype 语法：NUMBER[(precision [, scale])]
  
简称：precision &#8211;> p
  
scale     &#8211;> s

NUMBER(p, s)
  
范围：1 <= p <=38, -84 <= s <= 127
  
保存数据范围：-1.0e-130 <= number value < 1.0e+126
  
保存在机器内部的范围：1 ~ 22 bytes

有效位：从左边第一个不为0的数算起的位数。
  
s的情况：
  
s > 0
  
精确到小数点右边s位，并四舍五入。然后检验有效位是否<= p。
  
s < 0
  
精确到小数点左边s位，并四舍五入。然后检验有效位是否<= p + |s|。
  
s = 0
  
此时NUMBER表示整数。

eg:
  
Actual Data   Specified As  Stored As
  
&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
  
123.89           NUMBER         123.89
  
123.89           NUMBER(3)     124
  
123.89           NUMBER(6,2)   123.89
  
123.89           NUMBER(6,1)   123.9
  
123.89           NUMBER(4,2)   exceeds precision (有效位为5, 5 > 4)
  
123.89           NUMBER(6,-2)  100
  
.01234           NUMBER(4,5)   .01234 (有效位为4)
  
.00012           NUMBER(4,5)   .00012
  
.000127       NUMBER(4,5)   .00013
  
.0000012      NUMBER(2,7)   .0000012
  
.00000123     NUMBER(2,7)   .0000012
  
1.2e-4           NUMBER(2,5)   0.00012
  
1.2e-5           NUMBER(2,5)   0.00001
  
123.2564      NUMBER        123.2564
  
1234.9876     NUMBER(6,2)   1234.99
  
12345.12345   NUMBER(6,2)   Error (有效位为5+2 > 6)
  
1234.9876     NUMBER(6)     1235 (s没有表示s=0)
  
12345.345     NUMBER(5,-2)  12300
  
1234567       NUMBER(5,-2)  1234600
  
12345678      NUMBER(5,-2)  Error (有效位为8 > 7)
  
123456789     NUMBER(5,-4)  123460000
  
1234567890    NUMBER(5,-4)  Error (有效位为10 > 9)
  
12345.58      NUMBER(*, 1)  12345.6
  
0.1           NUMBER(4,5)   Error (0.10000, 有效位为5 > 4)
  
0.01234567    NUMBER(4,5)   0.01235
  
0.09999       NUMBER(4,5)   0.09999

三、Oracle语句距离

项目中的语句：

&nbsp;

[sql] view plaincopy
  
SELECT (CASE WHEN tt1.statistics\_date is not null THEN tt1.statistics\_date ELSE tt2.statistics\_date END) AS statistics\_date, NVL(tt1.actuser,0) AS actuser, NVL(tt2.new\_user,0) AS new\_user
  
FROM
  
(
  
SELECT t.statistics\_date, SUM(t.actuser) AS actuser FROM pdt\_stat\_act\_1133\_i t WHERE t.statistics\_date like &#8216;2013-04%&#8217; and t.statistics\_month = &#8216;2013-04&#8217; GROUP BY t.statistics\_date
  
) tt1
  
FULL JOIN
  
(
  
SELECT t2.statistics\_date, SUM(t2.new\_user) OVER(ORDER BY t2.statistics\_date) AS new\_user FROM (SELECT statistics\_date AS statistics\_date, SUM(new\_user) AS new\_user FROM pdt\_stat\_newuser\_1133\_i WHERE statistics\_date like &#8216;2013-04%&#8217; GROUP BY statistics\_date) t2
  
) tt2 ON tt1.statistics\_date = tt2.statistics\_date