---
title: MySQL int 长度
author: "-"
date: 2019-08-06T04:57:47+00:00
url: /?p=14770
categories:
  - Database
tags:
  - reprint
---
## MySQL int 长度
"浮点型"的长度是用来限制数字存储范围的. 比如 float(3,2) 只能够写入 0.00~999.99.
  
"整型"的长度并不会限制存储的数字范围. 比如, int 和 int(3) 的存储范围都是 -2147483648 ~ 2147483647, int unsigned 和 int(3) unsigned 的存储范围都是0 ~ 4294967295.
  
"整型"的长度实际上可以理解为"显示长度", 如果该字段开启 "Zerofill/补零"就能很明显地知道它的作用.

参考
  
"高性能MySQL" 的说明
  
"高性能MySQL" 书中在"4.1 选择优化的数据类型"中提到:

MySQL 可以为整数类型指定宽度, 例如 INT(11), 对大多数应用这是没有意义的: 它不会限制值的合法范围, 只是规定了 MySQL 的一些交互工具(例如 MySQL 命令行客户端)用来显示字符的个数. 对于存储和计算来说, INT(1) 和 INT(20) 是相同的
  
"MySQL 手册"的说明
  
MySQL 5.7 手册 "12.2.5 Numeric Type Attributes":

MySQL supports an extension for optionally specifying the display width of integer data types in parentheses following the base keyword for the type. For example, INT(4) specifies an INT with a display width of four digits. This optional display width may be used by applications to display integer values having a width less than the width specified for the column by left-padding them with spaces. (That is, this width is present in the metadata returned with result sets. Whether it is used or not is up to the application.)

MySQL 支持用括号包含的数字限定整型的显示长度. 比如 INT(4) 限定了整型的显示长度为 4 个字符, 对于小于 4 个字符的数字, 有些数据库软件会用"空格"来补齐小于 4 个位数的数字.

The display width does not constrain the range of values that can be stored in the column. Nor does it prevent values wider than the column display width from being displayed correctly. For example, a column specified as SMALLINT(3) has the usual SMALLINT range of -32768 to 32767, and values outside the range permitted by three digits are displayed in full using more than three digits.

这个显示长度并不会限制该字段的数字存储范围, 同时, 也不会阻止大于指定显示长度的数字写入该字段. 比如, SMALLINT(3) 的字段和 SMALLINT 的数字存储范围都是 -32768 to 32767, 如果存储的数字超过 3 个位数仍然是允许被存入 SMALLINT(3) 字段, 而且以其本来的位数显示.

When used in conjunction with the optional (nonstandard) attribute ZEROFILL, the default padding of spaces is replaced with zeros. For example, for a column declared as INT(4) ZEROFILL, a value of 5 is retrieved as 0005.

如果配合 ZEROFILL 属性, 将用 0 来补齐. 比如 INT(4) ZEROFILL 字段, 数字 5 会被存储为 0005.

https://www.jianshu.com/p/61293b416335