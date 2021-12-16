---
title: sql server中的 stuff 函数
author: "-"
date: 2013-07-29T08:28:32+00:00
url: /?p=5742
categories:
  - DataBase

---
## sql server中的 stuff 函数
# STUFF

删除指定长度的字符并在指定的起始点插入另一组字符。

##### 语法

`STUFF ( character_expression , start , length , character_expression )`

##### 参数

_character_expression_

由字符数据组成的表达式。_character_expression _可以是常量、变量，也可以是字符或二进制数据的列。

_start_

是一个整形值，指定删除和插入的开始位置。如果 _start_ 或 _length_ 是负数，则返回空字符串。如果 _start_ 比第一个 _character_expression _长，则返回空字符串。

_length_

是一个整数，指定要删除的字符数。如果 _length_ 比第一个 _character_expression _长，则最多删除到最后一个 _character_expression_ 中的最后一个字符。

##### 返回类型

如果 _character_expression _是一个支持的字符数据类型，则返回字符数据。如果 _character_expression _是一个支持的 binary 数据类型，则返回二进制数据。

##### 注释

可以嵌套字符串函数。

##### 示例

下例通过在第一个字符串 (abcdef) 中删除从第二个位置（字符 b) 开始的三个字符，然后在删除的起始位置插入第二个字符串，创建并返回一个字符串。

    SELECT STUFF('abcdef', 2, 3, 'ijklmn')
    GO
    

下面是结果集: 

    ---------
    aijklmnef
    (1 row(s) affected)