---
title: MySQL 数据类型
author: "-"
date: 2011-12-26T04:42:58+00:00
url: /?p=2001
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL 数据类型

### datetime, timestamp

两者都是时间类型字段，格式都一致。两者主要有以下几点区别:

最主要的区别-受时区影响不同。timestamp会跟随设置的时区变化而变化，而datetime保存的是绝对值不会变化。
详细可以阅读这篇博客的演示: MySQL: Datetime Versus Timestamp Data Types
一个timestamp字段，一个datetime字段，修改时区SET TIME_ZONE = "america/new_york";后，timestamp字段的值变了!
因此，如果应用场景有跨时区要求的要特别注意这点。

占用存储空间不同。timestamp储存占用4个字节，datetime储存占用8个字节: 12.8 Data Type Storage Requirements

可表示的时间范围不同。timestamp可表示范围:1970-01-01 00:00:00~2038-01-09 03:14:07，datetime支持的范围更宽1000-01-01 00:00:00 ~ 9999-12-31 23:59:59

索引速度不同。timestamp更轻量，索引相对datetime更快。

### 数值类型

MySQL 的数值数据类型可以大致划分为两个类别，一个是整数，另一个是浮点数或小数。许多不同的子类型对这些类别中的每一个都是可用的，每个子类型支持不同大小的数据，并且 MySQL 允许我们指定数值字段中的值是否有正负之分或者用零填补。

各种数值类型以及它们的允许范围和占用的内存空间。

### TINYINT

* 大小: 1 字节
* 范围 (有符号) : -128 ~ 127
* 范围 (无符号) : 0 ~ 255
* 用途: 小整数值

### SMALLINT

* 大小: 2 字节
* 范围 (有符号) : -32,768 ~ 32,767
* 范围 (无符号) : 0 ~ 65,535
* 用途: 大整数值

### MEDIUMINT

* 大小: 3 字节
* 范围 (有符号) : -8,388,608，8,388,607
* 范围 (无符号) : 0，16,777,215
* 用途: 大整数值

### INT 或 INTEGER

* 大小: 4 字节
* 范围 (有符号) : -2 147 483 648，2 147 483 647
* 范围 (无符号) : 0，4 294 967 295
* 用途: 大整数值

| 类型          | - 大小 | 范围 (有符号)  | 范围 (无符号)     | 用途   |
| -- | ----- | ---- | ----- | --- |
| BIGINT      | 8 字节       | (-9 233 372 036 854 775 808，9 223 372 036 854 775 807)    |   | (0，18 446 744 073 709 551 615)|极大整数值 |
| FLOAT       | 4 字节       | (-3.402 823 466 E+38，1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38)                                        | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                       | 单精度浮点数值                              |
| DOUBLE      | 8 字节       | (1.797 693 134 862 315 7 E+308，2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 双精度浮点数值                              |

### DECIMAL

对DECIMAL(M,D) ，如果M>D，为M+2否则为D+2 依赖于M和D的值 依赖于M和D的值小数值
  
DECIMAL(4, 1) -9.9 到 99.9 -999.9 到 9999.9
  
DECIMAL(5,1) -99.9 到 999.9 -9999.9 到 99999.9
  
DECIMAL(6,1) -999.9 到 9999.9 -99999.9 到 999999.9
  
DECIMAL(6,2) -99.99 到 999.99 -9999.99 到 99999.99
  
DECIMAL(6,3) -9.999 到 99.999 -999.999 到 9999.999

### tinyInt1isBit

1. tinyInt(1) 只用来代表Boolean含义的字段，且0代表False，1代表True。如果要存储多个数值，则定义为tinyInt(N), N>1。例如 tinyInt(2)。

2. JDBC的URL增加 tinyInt1isBit=false参数，注意参数名区分大小写，否则不生效:

jdbc:MySQL://localhost:3306/test?tinyInt1isBit=false

### varchar

在MySQL内部属于从blob发展出来的一个结构，在早期版本中  
innobase中，也是768字节以后进行overfolw存储。

### TEXT

是要要进overflow存储。 也是对于text字段，不会和行数据存在一  
 起。但原则上不会全部overflow ,会有768字节和原始的行存储在一块，多  
于768的行会存在和行相同的Page或是其它Page上。

### LONGTEXT

LONGTEXT
  
0-4 294 967 295字节
  
极大文本数据

对于Innodb-plugin后： 对于变长字段处理都是20Byte后进行overflow存储 (在新的row_format下：dynimic compress）

从最大值上讲：

* 在 Innobase 中, 变长字段，是尽可能的存储到一个 Page 里，这样，如果使用到这些大的变长字段，会造成一个Page里能容纳的行数很少，在查询时，虽然没查询这些大的字段，但也会加载到 innodb buffer pool中，等于浪费的内存。
     (buffer pool 的缓存是按 page 为单位） (不在一个page了会增加随机的IO）

* 在innodb-plugin中为了减少这种大的变长字段对内存的浪费，引入了大于20个字节的，都进行 overflow 存储，而且希望不要存到相同的page中，为了增加一个page里能存储更多的行，提高buffer pool的利用率。 这也要求我们，如果不是特别需要就不要读取那些变长的字段。

　　那问题来了？ 为什么varchar(255+)存储上和text很相似了，但为什么还要有varchar, mediumtext, text这些类型？
 (从存储上来讲大于255的varchar可以说是转换成了text.这也是为什么varchar大于65535了会转成mediumtext)

　　我理解：这块是一方面的兼容，另一方面在非空的默认值上varchar和text有区别。从整体上看功能上还是差别的。

　　这里还涉及到字段额外开销的：

    - varchar 小于255byte  1byte overhead
    - varchar 大于255byte  2byte overhead
     
    - tinytext 0-255 1 byte overhead
    - text 0-65535 byte 2 byte overhead
    - mediumtext 0-16M  3 byte overhead
     
    - longtext 0-4Gb 4byte overhead 

　　备注 overhead是指需要几个字节用于记录该字段的实际长度。

　　从处理形态上来讲varchar 大于768字节后，实质上存储和text差别不是太大了。 基本认为是一样的。  
另外从8000byte这个点说明一下： 对于varcahr, text如果行不超过8000byte (大约的数，innodb data  
page的一半） ,overflow不会存到别的page中。基于上面的特性可以总结为text只是一个MySQL扩展出  
来的特殊语法有兼容的感觉。
3.从默认值上讲：

    - 对于text字段，MySQL不允许有默认值。
    - varchar允许有默认值
　　总结：

　　根据存储的实现： 可以考虑用varchar替代tinytext

　　如果需要非空的默认值，就必须使用varchar

　　如果存储的数据大于64K，就必须使用到mediumtext , longtext

　　varchar(255+)和text在存储机制是一样的

　　需要特别注意varchar(255)不只是255byte ,实质上有可能占用的更多。

　　特别注意，varchar大字段一样的会降低性能，所以在设计中还是一个原则大字段要拆出去，主表还是要尽量的瘦小

　　源码中类型：
+--Field_str (abstract)
 |  +--Field_longstr
 |  |  +--Field_string
 |  |  +--Field_varstring
 |  |  +--Field_blob
 |  |     +--Field_geom
 |  |
 |  +--Field_null
 |  +--Field_enum
 |     +--Field_set
参考：

[http://yoshinorimatsunobu.blogspot.com/2010/11/handling-long-](http://yoshinorimatsunobu.blogspot.com/2010/11/handling-long-)
textsblobs-in-innodb-1-to.html
　　[http://nicj.net/mysql-text-vs-varchar-performance/](http://nicj.net/mysql-text-vs-varchar-performance/)
　　[http://www.pythian.com/blog/text-vs-varchar/](http://www.pythian.com/blog/text-vs-varchar/)

作者：HaleyLiu
链接：[https://www.jianshu.com/p/fbde22109a7b](https://www.jianshu.com/p/fbde22109a7b)
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

>[https://www.jianshu.com/p/fbde22109a7b](https://www.jianshu.com/p/fbde22109a7b)

INT 类型
  
在 MySQL 中支持的 5 个主要整数类型是 TINYINT，SMALLINT，MEDIUMINT，INT 和 BIGINT。这些类型在很大程度上是相同的，只有它们存储的值的大小是不相同的。

MySQL 以一个可选的显示宽度指示器的形式对 SQL 标准进行扩展，这样当从数据库检索一个值时，可以把这个值加长到指定的长度。例如，指定一个字段的类型为 INT(6)，就可以保证所包含数字少于 6 个的值从数据库中检索出来时能够自动地用空格填充。需要注意的是，使用一个宽度指示器不会影响字段的大小和它可以存储的值的范围。

万一我们需要对一个字段存储一个超出许可范围的数字，MySQL 会根据允许范围最接近它的一端截短后再进行存储。还有一个比较特别的地方是，MySQL 会在不合规定的值插入表前自动修改为 0。

UNSIGNED 修饰符规定字段只保存正值。因为不需要保存数字的正、负符号，可以在储时节约一个"位"的空间。从而增大这个字段可以存储的值的范围。

ZEROFILL 修饰符规定 0 (不是空格) 可以用来真补输出的值。使用这个修饰符可以阻止 MySQL 数据库存储负值。

FLOAT、DOUBLE 和 DECIMAL 类型
  
MySQL 支持的三个浮点类型是 FLOAT、DOUBLE 和 DECIMAL 类型。FLOAT 数值类型用于表示单精度浮点数值，而 DOUBLE 数值类型用于表示双精度浮点数值。

与整数一样，这些类型也带有附加参数: 一个显示宽度指示器和一个小数点指示器。比如语句 FLOAT(7,3) 规定显示的值不会超过 7 位数字，小数点后面带有 3 位数字。

对于小数点后面的位数超过允许范围的值，MySQL 会自动将它四舍五入为最接近它的值，再插入它。

DECIMAL 数据类型用于精度要求非常高的计算中，这种类型允许指定数值的精度和计数方法作为选择参数。精度在这里指为这个值保存的有效数字的总个数，而计数方法表示小数点后数字的位数。比如语句 DECIMAL(7,3) 规定了存储的值不会超过 7 位数字，并且小数点后不超过 3 位。

忽略 DECIMAL 数据类型的精度和计数方法修饰符将会使 MySQL 数据库把所有标识为这个数据类型的字段精度设置为 10，计算方法设置为 0。

UNSIGNED 和 ZEROFILL 修饰符也可以被 FLOAT、DOUBLE 和 DECIMAL 数据类型使用。并且效果与 INT 数据类型相同。

字符串类型
  
MySQL 提供了 8 个基本的字符串类型，可以存储的范围从简单的一个字符到巨大的文本块或二进制字符串数据。

类型
  
大小
  
用途
  
CHAR
  
0-255字节
  
定长字符串
  
VARCHAR
  
0-255字节
  
变长字符串
  
TINYBLOB
  
0-255字节
  
不超过 255 个字符的二进制字符串
  
TINYTEXT
  
0-255字节
  
短文本字符串
  
BLOB
  
0-65 535字节
  
二进制形式的长文本数据
  
TEXT
  
0-65 535字节
  
长文本数据
  
MEDIUMBLOB
  
0-16 777 215字节
  
二进制形式的中等长度文本数据
  
MEDIUMTEXT
  
0-16 777 215字节
  
中等长度文本数据
  
LOGNGBLOB
  
0-4 294 967 295字节
  
二进制形式的极大文本数据
  
CHAR 和 VARCHAR 类型
  
CHAR 类型用于定长字符串，并且必须在圆括号内用一个大小修饰符来定义。这个大小修饰符的范围从 0-255。比指定长度大的值将被截短，而比指定长度小的值将会用空格作填补。

CHAR 类型可以使用 BINARY 修饰符。当用于比较运算时，这个修饰符使 CHAR 以二进制方式参于运算，而不是以传统的区分大小写的方式。

CHAR 类型的一个变体是 VARCHAR 类型。它是一种可变长度的字符串类型，并且也必须带有一个范围在 0-255 之间的指示器。CHAR 和 VARCHGAR 不同之处在于 MuSQL 数据库处理这个指示器的方式: CHAR 把这个大小视为值的大小，不长度不足的情况下就用空格补足。而 VARCHAR 类型把它视为最大值并且只使用存储字符串实际需要的长度 (增加一个额外字节来存储字符串本身的长度) 来存储值。所以短于指示器长度的 VARCHAR 类型不会被空格填补，但长于指示器的值仍然会被截短。

因为 VARCHAR 类型可以根据实际内容动态改变存储值的长度，所以在不能确定字段需要多少字符时使用 VARCHAR 类型可以大大地节约磁盘空间、提高存储效率。

VARCHAR 类型在使用 BINARY 修饰符时与 CHAR 类型完全相同。

TEXT 和 BLOB 类型
  
对于字段长度要求超过 255 个的情况下，MySQL 提供了 TEXT 和 BLOB 两种类型。根据存储数据的大小，它们都有不同的子类型。这些大型的数据用于存储文本块或图像、声音文件等二进制数据类型。

TEXT 和 BLOB 类型在分类和比较上存在区别。BLOB 类型区分大小写，而 TEXT 不区分大小写。大小修饰符不用于各种 BLOB 和 TEXT 子类型。比指定类型支持的最大范围大的值将被自动截短。

日期和时间类型
  
在处理日期和时间类型的值时，MySQL 带有 5 个不同的数据类型可供选择。它们可以被分成简单的日期、时间类型，和混合日期、时间类型。根据要求的精度，子类型在每个分类型中都可以使用，并且 MySQL 带有内置功能可以把多样化的输入格式变为一个标准格式。

类型
  
大小
  
(字节)
  
范围
  
格式
  
用途
  
DATE
  
1000-01-01/9999-12-31
  
YYYY-MM-DD
  
日期值
  
TIME
  
'-838:59:59'/'838:59:59'
  
HH:MM:SS
  
时间值或持续时间
  
YEAR
  
1901/2155
  
YYYY
  
年份值
  
DATETIME
  
1000-01-01 00:00:00/9999-12-31 23:59:59
  
YYYY-MM-DD HH:MM:SS
  
混合日期和时间值

复合类型
  
MySQL 还支持两种复合数据类型 ENUM 和 SET，它们扩展了 SQL 规范。虽然这些类型在技术上是字符串类型，但是可以被视为不同的数据类型。一个 ENUM 类型只允许从一个集合中取得一个值；而 SET 类型允许从一个集合中取得任意多个值。

ENUM 类型
  
ENUM 类型因为只允许在集合中取得一个值，有点类似于单选项。在处理相互排拆的数据时容易让人理解，比如人类的性别。ENUM 类型字段可以从集合中取得一个值或使用 null 值，除此之外的输入将会使 MySQL 在这个字段中插入一个空字符串。另外如果插入值的大小写与集合中值的大小写不匹配，MySQL 会自动使用插入值的大小写转换成与集合中大小写一致的值。

 ENUM 类型在系统内部可以存储为数字，并且从 1 开始用数字做索引。一个 ENUM 类型最多可以包含 65536 个元素，其中一个元素被 MySQL 保留，用来存储错误信息，这个错误值用索引 0 或者一个空字符串表示。

MySQL 认为 ENUM 类型集合中出现的值是合法输入，除此之外其它任何输入都将失败。这说明通过搜索包含空字符串或对应数字索引为 0 的行就可以很容易地找到错误记录的位置。

SET 类型
  
SET 类型与 ENUM 类型相似但不相同。SET 类型可以从预定义的集合中取得任意数量的值。并且与 ENUM 类型相同的是任何试图在 SET 类型字段中插入非预定义的值都会使 MySQL 插入一个空字符串。如果插入一个即有合法的元素又有非法的元素的记录，MySQL 将会保留合法的元素，除去非法的元素。

一个 SET 类型最多可以包含 64 项元素。在 SET 元素中值被存储为一个分离的"位"序列，这些"位"表示与它相对应的元素。"位"是创建有序元素集合的一种简单而有效的方式。并且它还去除了重复的元素，所以 SET 类型中不可能包含两个相同的元素。

希望从 SET 类型字段中找出非法的记录只需查找包含空字符串或二进制值为 0 的行。

datetime

大小字节 8,

范围 1000-01-01 00:00:00/9999-12-31 23:59:59,

格式 YYYY-MM-DD HH:MM:SS,

用途 混合日期和时间值,

varchar(256)

VARCHAR 类型可以根据实际内容动态改变存储值的长度，所以在不能确定字段需要多少字符时使用 VARCHAR 类型可以大大地节约磁盘空间、提高存储效率。

————————————————
版权声明: 本文为CSDN博主「inrgihc」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/inrgihc/article/details/118713282](https://blog.csdn.net/inrgihc/article/details/118713282)

作者: 金星show
  
链接: [https://www.jianshu.com/p/51aeaeeb15cf](https://www.jianshu.com/p/51aeaeeb15cf)
  
来源: 简书
