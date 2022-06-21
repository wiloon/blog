---
title: FOR XML PATH
author: "-"
date: 2013-07-29T08:27:48+00:00
url: /?p=5741
categories:
  - DataBase
tags:
  - reprint
---
## FOR XML PATH
<http://www.cnblogs.com/doubleliang/archive/2011/07/06/2098775.html>

FOR XML PATH 有的人可能知道有的人可能不知道，其实它就是将查询结果集以XML形式展现，有了它我们可以简化我们的查询语句实现一些以前可能需要借助函数活存储过程来完成的工作。那么以一个实例为主.

一.FOR XML PATH 简单介绍

那么还是首先来介绍一下FOR XML PATH ，假设现在有一张兴趣爱好表 (hobby) 用来存放兴趣爱好，表结构如下: 

接下来我们来看应用FOR XML PATH的查询结果语句如下: 

SELECT * FROM @hobby FOR XML PATH

结果: 

复制代码

<row>

<hobbyID>1</hobbyID>

<hName>爬山</hName>

</row>

<row>

<hobbyID>2</hobbyID>

<hName>游泳</hName>

</row>

<row>

<hobbyID>3</hobbyID>

<hName>美食</hName>

</row>

复制代码

由此可见FOR XML PATH 可以将查询结果根据行输出成XML各式！

那么，如何改变XML行节点的名称呢？代码如下: 

SELECT * FROM @hobby FOR XML PATH('MyHobby')

结果一定也可想而知了吧？没错原来的行节点<row> 变成了我们在PATH后面括号()中，自定义的名称<MyHobby>,结果如下: 

复制代码

<MyHobby>

<hobbyID>1</hobbyID>

<hName>爬山</hName>

</MyHobby>

<MyHobby>

<hobbyID>2</hobbyID>

<hName>游泳</hName>

</MyHobby>

<MyHobby>

<hobbyID>3</hobbyID>

<hName>美食</hName>

</MyHobby>

复制代码

这个时候细心的朋友一定又会问那么列节点如何改变呢？还记的给列起别名的关键字AS吗？对了就是用它!代码如下: 

SELECT hobbyID as 'MyCode',hName as 'MyName' FROM @hobby FOR XML PATH('MyHobby')

那么这个时候我们列的节点名称也会编程我们自定义的名称 <MyCode>与<MyName>结果如下: 

复制代码

<MyHobby>

<MyCode>1</MyCode>

<MyName>爬山</MyName>

</MyHobby>

<MyHobby>

<MyCode>2</MyCode>

<MyName>游泳</MyName>

</MyHobby>

<MyHobby>

<MyCode>3</MyCode>

<MyName>美食</MyName>

</MyHobby>

复制代码

噢！ 既然行的节点与列的节点我们都可以自定义，我们是否可以构建我们喜欢的输出方式呢？还是看代码: 

SELECT '[ '+hName+' ]' FROM @hobby FOR XML PATH(")

没错我们还可以通过符号+号，来对字符串类型字段的输出格式进行定义。结果如下: 

[ 爬山 ][ 游泳 ][ 美食 ]

那么其他类型的列怎么自定义？ 没关系，我们将它们转换成字符串类型就行啦！例如: 

SELECT '{'+STR(hobbyID)+'}','[ '+hName+' ]' FROM @hobby FOR XML PATH(")

好的 FOR XML PATH就基本介绍到这里吧，更多关于FOR XML的知识请查阅帮助文档！

接下来我们来看一个FOR XML PATH的应用场景吧！那么开始吧。。。。。。

二.一个应用场景与FOR XML PATH应用

首先呢！我们在增加一张学生表，列分别为 (stuID,sName,hobby) ,stuID代表学生编号，sName代表学生姓名，hobby列存学生的爱好！那么现在表结构如下: 

这时，我们的要求是查询学生表，显示所有学生的爱好的结果集，代码如下: 

复制代码

SELECT B.sName,LEFT(StuList,LEN(StuList)-1) as hobby FROM (

SELECT sName,

(SELECT hobby+',' FROM student

WHERE sName=A.sName

FOR XML PATH(")) AS StuList

FROM student A

GROUP BY sName

) B

复制代码

结果如下:

分析:  好的，那么我们来分析一下，首先看这句: 

SELECT hobby+',' FROM student

WHERE sName=A.sName

FOR XML PATH(")

这句是通过FOR XML PATH 将某一姓名如张三的爱好，显示成格式为: " 爱好1，爱好2，爱好3，"的格式！

那么接着看: 

复制代码

SELECT B.sName,LEFT(StuList,LEN(StuList)-1) as hobby FROM (

SELECT sName,

(SELECT hobby+',' FROM student

WHERE sName=A.sName

FOR XML PATH(")) AS StuList

FROM student A

GROUP BY sName

) B

复制代码

剩下的代码首先是将表分组，在执行FOR XML PATH 格式化，这时当还没有执行最外层的SELECT时查询出的结构为:

可以看到StuList列里面的数据都会多出一个逗号，这时随外层的语句:SELECT B.sName,LEFT(StuList,LEN(StuList)-1) as hobby 就是来去掉逗号，并赋予有意义的列明！


用在存储过程 里

```sql
  
DECLARE @xml_var XML
  
SET @xml_var =
  
(
    
SELECT *,
      
(
        
SELECT *

FROM Orders

WHERE Orders.CustomerID=Customers.CustomerID

FOR XML AUTO, TYPE

)

FROM Customers WHERE CustomerID='ALFKI'

FOR XML AUTO, TYPE

)```
  
```

<http://blogs.msdn.com/sqlprogrammability/articles/576095.aspx>

<http://stackoverflow.com/questions/914009/saving-the-for-xml-auto-results-to-variable-in-sql>