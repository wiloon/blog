---
title: Oracle CHAR，VARCHAR，VARCHAR2,nvarchar类型的区别与使用
author: wiloon
type: post
date: 2013-06-28T02:32:01+00:00
url: /?p=5600
categories:
  - DataBase

---
一 varchar,nvarchar,
  
四个类型都属于变长字符类型， varchar和varchar2的区别在与后者把所有字符都占两字节，前者只对汉字和全角等字符占两字节。 nvarchar和nvarchar2的区别和上面一样，   与上面区别在于是根据Unicode   标准所进行的定义的类型，通常用于支持多国语言类似系统的定义。

1.char

char的长度是固定的，比如说，你定义了char(20),即使你你插入abc，不足二十个字节，数据库也会在abc后面自动加上17个空格，以补足二十个字节；

char是区分中英文的，中文在char中占两个字节，而英文占一个，所以char(20)你只能存20个字母或10个汉字。

char适用于长度比较固定的，一般不含中文的情况

2.varchar/varchar2

varchar是长度不固定的，比如说，你定义了varchar(20),当你插入abc，则在数据库中只占3个字节。

varchar同样区分中英文，这点同char。

varchar2基本上等同于varchar，它是oracle自己定义的一个非工业标准varchar，不同在于，varchar2用null代替varchar的空字符串

varchar/varchar2适用于长度不固定的，一般不含中文的情况

3.nvarchar/nvarchar2

nvarchar和nvarchar2是长度不固定的

nvarchar不区分中英文，比如说：你定义了nvarchar(20),你可以存入20个英文字母/汉字或中英文组合，这个20定义的是字符数而不是字节数

nvarchar2基本上等同于nvarchar，不同在于nvarchar2中存的英文字母也占两个字节

nvarchar/nvarchar2适用于存放中文

char [ ( n ) ]

固定长度，非 Unicode 字符数据，长度为 n 个字节。n 的取值范围为 1 至 8,000，存储大小是 n 个字节。

varchar [ ( n | max ) ]

可变长度，非 Unicode 字符数据。n 的取值范围为 1 至 8,000。max 指示最大存储大小是 2^31-1 个字节。存储大小是输入数据的实际长度加 2 个字节，用于反映存储的数据的长度。所输入数据的长度可以为 0 个字符。

* 如果列数据项的大小一致，则使用 char。
  
* 如果列数据项的大小差异相当大，则使用 varchar。
  
* 如果列数据项大小相差很大，而且大小可能超过 8,000 字节，请使用 varchar(max)。

如果未在数据定义或变量声明语句中char 或 varchar 数据类型指定 n，则默认长度为 1。如果在使用 CAST 和 CONVERT 函数时char 或 varchar 数据类型未指定 n，则默认长度为 30。
  
当执行 CREATE TABLE 或 ALTER TABLE 时，如果 SET ANSI_PADDING 为 OFF，则定义为 NULL 的 char 列将作为 varchar 处理。
  
另外帮助理解的，只供参考：转自http://www.51testing.com/?uid-258885-action-viewspace-itemid-141197
  
也可参照学习http://ce.sysu.edu.cn/garden/dispbbs.asp?boardid=26&ID=8774&replyID=18180&skin=1
  
1.NULL值(空值)。

a. char列的NULL值占用存储空间。

b. varcahr列的NULL值不占用存储空间。

c. 插入同样数量的NULL值，varchar列的插入效率明显高出char列。
  
2.插入数据

无论插入数据涉及的列是否建立索引，char的效率都明显低于varchar。

3. 更新数据

如果更新的列上未建立索引，则char的效率低于varchar，差异不大；建立索引的话，效率较高。

4. 修改结构

a. 无论增加或是删除的列的类型是char还是varchar，操作都能较快的完成，而且效率上没有什么差异。

b. 对于增加列的宽度而言，char与varchar有非常明显的效率差异，修改varcahr列基本上不花费时间，而修改char列需要花费很长的时间。

5.数据检索

无论是否通过索引，varchar类型的数据检索略优于char的扫描。

选择char还是选择varchar的建议

1.适宜于char的情况：

a. 列中的各行数据长度基本一致，长度变化不超过50字节；

b. 数据变更频繁，数据检索的需求较少。

c. 列的长度不会变化，修改char类型列的宽度的代价比较大。

d. 列中不会出现大量的NULL值。

e. 列上不需要建立过多的索引，过多的索引对char列的数据变更影响较大。

2.适宜于varchar的情况;

a. 列中的各行数据的长度差异比较大。

b. 列中数据的更新非常少，但查询非常频繁。
  
c. 列中经常没有数据，为NULL值或为空值

nchar [ ( n ) ]

n 个字符的固定长度的 Unicode 字符数据。n 值必须在 1 到 4,000 之间（含）。存储大小为两倍 n 字节。

nvarchar [ ( n | max ) ]

可变长度 Unicode 字符数据。n 值在 1 到 4,000 之间（含）。max 指示最大存储大小为 2^31-1 字节。存储大小是所输入字符个数的两倍 + 2 个字节。所输入数据的长度可以为 0 个字符。

注释

如果没有在数据定义或变量声明语句中指定 n，则默认长度为 1。如果没有使用 CAST 函数指定 n，则默认长度为 30。

如果列数据项的大小可能相同，请使用 nchar。

如果列数据项的大小可能差异很大，请使用 nvarchar。

sysname 是系统提供的用户定义数据类型，除了不可为空值外，在功能上与 nvarchar(128) 相同。sysname 用于引用数据库对象名。

为使用 nchar 或 nvarchar 的对象分配的是默认的数据库排序规则，但可使用 COLLATE 子句分配特定的排序规则。

SET ANSI\_PADDING ON 永远适用于 nchar 和 nvarchar。SET ANSI\_PADDING OFF 不适用于 nchar 或 nvarchar 数据类型。

在Oracle中CHAR,NCHAR,VARCHAR,VARCHAR2,NVARCHAR2这五种类型的区别

1.CHAR(size)和VARCHAR(size)的区别
  
CHAR为定长的字段，最大长度为2K字节；
  
VARCHAR为可变长的字段，最大长度为4K字节；

2.CHAR(size)和NCHAR(size)的区别
  
CHAR如果存放字母数字占1个字节，存放GBK编码的汉字存放2个字节，存放UTF-8编码的汉字占用3个字节；
  
NCHAR根据所选字符集来定义存放字符的占用字节数，一般都为2个字节存放一个字符(不管字符或者汉字)

3.VARCHAR(size)和VARCHAR2(size)的区别
  
在现在的版本中，两者是没有区别的；最大长度为4K字节；推荐使用VARCHAR2；

4.VARCHAR2(size)和NVARCHAR2(size)的区别
  
最大长度为4K字节，区别同CHAR与NCHAR的区别；（如果数据库字符集长度是2，则NVARCHAR2最大为2K）

5.共同特性
  
当执行insert的时候，插入的值为"，则转变成null，即insert ... values(") <=> insert ... values(null)
  
搜索的条件须用where xx is null

6.例子
  
比如有一个性别字段，里面存放“男，女”的其中一个值，两种常用选择
  
CHAR(2)    和 NCHAR(1)



[http://winie.iteye.com/blog/540340http://blog.sina.com.cn/s/blog_5fe8502601016bu7.html][1]

 [1]: http://winie.iteye.com/blog/540340