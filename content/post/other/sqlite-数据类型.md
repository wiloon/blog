---
title: sqlite 数据类型
author: "-"
date: 2012-07-08T15:05:01+00:00
url: sqlite/datatype
categories:
  - db
tags:
  - reprint
---
## sqlite 数据类型

一般数据采用的固定的静态数据类型，而 SQLite 采用的是动态数据类型，会根据存入值自动判断。SQLite 具有以下五种数据类型:
  
- NULL: 空值。
- INTEGER: 带符号的整型，具体取决有存入数字的范围大小。
- REAL: 浮点数字，存储为8-byte IEEE浮点数。
- TEXT: 字符串文本。
- BLOB: 二进制对象。

但实际上，sqlite3 也接受如下的数据类型:

- smallint 16 位元的整数。
- interger 32 位元的整数。
- decimal(p,s) p 精确值和 s 大小的十进位整数，精确值p是指全部有几个数(digits)大小值，s是指小数点後有几位数。如果没有特别指定，则系统会设为 p=5; s=0 。
- float  32位元的实数。
- double  64位元的实数。
- char(n)  n 长度的字串，n不能超过 254。
- varchar(n) 长度不固定且其最大长度为 n 的字串，n 不能超过 4000。
- graphic(n) 和 char(n) 一样，不过其单位是两个字元 double-bytes， n不能超过127。这个形态是为了支援两个字元长度的字体，例如中文字。
- vargraphic(n) 可变长度且其最大长度为 n 的双字元字串，n不能超过 2000
- date  包含了 年份、月份、日期。
- time  包含了 小时、分钟、秒。
- timestamp 包含了 年、月、日、时、分、秒、千分之一秒。
- datetime DATETIME 类型用于存储日期和时间信息。它的格式通常是 "YYYY-MM-DD HH:MM:SS"
  
    Sqlite常用数据类型,
  
    这句话本身就有问题，因为: SQLite是无类型的. 这意味着你可以保存任何类型的数据到你所想要保存的任何表的任何列中, 无论这列声明的数据类型是什么(只有自动递增Integer Primary Key才有用). 对于SQLite来说对字段不指定类型是完全有效的. 如:
  
    Create Table ex3(a, b, c);
  
    即使SQLite允许忽略数据类型, 但是仍然建议在你的Create Table语句中指定数据类型. 因为数据类型对于你和其他的程序员交流, 或者你准备换掉你的数据库引擎是非常有用的. SQLite支持常见的数据类型, 如:
  
    SQL代码
  
        CREATE TABLE ex2(
      
      
        a VARCHAR(10),
      
      
        b NVARCHAR(15),
      
      
        c TEXT,
      
      
        d INTEGER,
      
      
        e FLOAT,
      
      
        f BOOLEAN,
      
      
        g CLOB,
      
      
        h BLOB,
      
      
        i TIMESTAMP,
      
      
        j NUMERIC(10,5),
      
      
        k VARYING CHARACTER (24),
      
      
        l NATIONAL VARYING CHARACTER(16)
      
      
        );

    char、varchar、text和nchar、nvarchar、ntext的区别
  
    1、CHAR。CHAR存储定长数据很方便，CHAR字段上的索引效率级高，比如定义char(10)，那么不论你存储的数据是否达到了10个字节，都要占去10个字节的空间,不足的自动用空格填充。
  
    2、VARCHAR。存储变长数据，但存储效率没有CHAR高。如果一个字段可能的值是不固定长度的，我们只知道它不可能超过10个字符，把它定义为 VARCHAR(10)是最合算的。VARCHAR类型的实际长度是它的值的实际长度+1。为什么"+1"呢？这一个字节用于保存实际使用了多大的长度。从空间上考虑，用varchar合适；从效率上考虑，用char合适，关键是根据实际情况找到权衡点。
  
    3、TEXT。text存储可变长度的非Unicode数据，最大长度为2^31-1(2,147,483,647)个字符。
  
    4、NCHAR、NVARCHAR、NTEXT。这三种从名字上看比前面三种多了个"N"。它表示存储的是Unicode数据类型的字符。我们知道字符中，英文字符只需要一个字节存储就足够了，但汉字众多，需要两个字节存储，英文与汉字同时存在时容易造成混乱，Unicode字符集就是为了解决字符集这种不兼容的问题而产生的，它所有的字符都用两个字节表示，即英文字符也是用两个字节表示。nchar、nvarchar的长度是在1到4000之间。和char、varchar比较起来，nchar、nvarchar则最多存储4000个字符，不论是英文还是汉字；而char、varchar最多能存储8000个英文，4000个汉字。可以看出使用nchar、nvarchar数据类型时不用担心输入的字符是英文还是汉字，较为方便，但在存储英文时数量上有些损失。
  
    所以一般来说，如果含有中文字符，用nchar/nvarchar，如果纯英文和数字，用char/varchar。
  
[http://blog.csdn.net/jin868/article/details/5961263](http://blog.csdn.net/jin868/article/details/5961263)
