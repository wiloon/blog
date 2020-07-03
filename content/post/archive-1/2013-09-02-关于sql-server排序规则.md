---
title: 关于SQL SERVER排序规则
author: wiloon
type: post
date: 2013-09-02T09:14:01+00:00
url: /?p=5788
categories:
  - DataBase

---
因为新的SQL SERVER 使用了英文版, 使用了默认的排序规则是:SQL\_Latin1\_General\_CP1\_CI_AS

但旧的数据使用的是中文版, 使用的排序规则是 Chinese\_PRC\_CI_AS. <wbr /> 当新建的数据与旧的数据库的表相关联时,出现排序规则不一致的错误信息:

Cannot resolve the collation conflict between "SQL\_Latin1\_General\_CP1\_CI\_AS" and "Chinese\_PRC\_CI\_AS" in the equal to operation.

<wbr />

解决方法: <wbr />

1. 可以在有 文字的Fields 上加上 **COLLATE DATABASE_DEFAULT**

**如:**

SELECT Title, FirstName, MiddleName, EmailAddress, EmailPromotion, ModifiedDate
  
FROM <wbr /> AdventureWorks.Person.Contact
  
WHERE ContactID<10
  
UNION
  
SELECT Title **COLLATE DATABASE_DEFAULT**,
  
FirstName **COLLATE DATABASE_DEFAULT**, <wbr /> MiddleName **COLLATE DATABASE_DEFAULT,** EmailAddress**COLLATE DATABASE_DEFAULT**

**<span style="color: #000000;">2. 在建表时直接更改表的排序规则:**

CREATE <wbr />TABLE <wbr />MyTable <wbr />(PrimaryKey <wbr />int <wbr />PRIMARY <wbr />KEY, <wbr />CharCol <wbr />varchar(10) <wbr />**<span>Chinese_PRC_CI_AS**)

<span style="color: #000000;">3. 使用以下语句更改,但不适用于临时表

ALTER <wbr />DATABASE <wbr />MyDatabase <wbr />**<span style="font-size: medium;">Chinese_PRC_CI_AS**


一、排序规则简介：

什么叫排序规则呢？MS是这样描述的："在 Microsoft SQL Server  中，
  
字符串的物理存储由排序规则控制。排序规则指定表示每个字符的位模式以及存
  
储和比较字符所使用的规则。"
  
在查询分析器内执行下面语句，可以得到SQL　SERVER支持的所有排序规则。
  
select * from ::fn_helpcollations()
  
排序规则名称由两部份构成，前半部份是指本排序规则所支持的字符集。
  
如：
  
Chinese\_PRC\_CS\_AI\_WS
  
前半部份：指UNICODE字符集，Chinese\_PRC\_指针对大陆简体字UNICODE的排序规则，按拼音排序。
  
Chinese\_PRC\_Stroke 表示按汉字笔画排序；
  
排序规则的后半部份即后缀 含义：
  
_BIN 二进制排序
  
_CI(CS) 是否区分大小写，CI不区分，CS区分(case-insensitive/case-sensitive)
  
_AI(AS) 是否区分重音，AI不区分，AS区分(accent-insensitive/accent-sensitive)
  
_KI(KS) 是否区分假名类型,KI不区分，KS区分(kanatype-insensitive/kanatype-sensitive)
  
_WI(WS) 是否区分宽度 WI不区分，WS区分(width-insensitive/width-sensitive)
  
区分大小写:如果想让比较将大写字母和小写字母视为不等，请选择该选项。
  
区分重音:如果想让比较将重音和非重音字母视为不等，请选择该选项。如果选择该选项，
  
比较还将重音不同的字母视为不等。
  
区分假名:如果想让比较将片假名和平假名日语音节视为不等，请选择该选项。
  
区分宽度:如果想让比较将半角字符和全角字符视为不等，请选择该选项。
  
二、修改、查看排序规则：

--修改列的排序规则
  
ALTER TABLE tb
  
ALTER COLUMN colname nvarchar(100) COLLATE Chinese\_PRC\_CI_AS

--修改数据库的排序规则
  
ALTER DATABASE database
  
COLLATE Chinese\_PRC\_CS_AS

--查看某个表的排序规则
  
select collation from syscolumns
  
where id=object_id(N'yourtablename')

五、排序规则应用：

SQL SERVER提供了大量的WINDOWS和SQLSERVER专用的排序规则，但它的应用往往
  
被开发人员所忽略。其实它在实践中大有用处。

例1:让表NAME列的内容按拼音排序：

create table #t(id int,name varchar(20))
  
insert #t select 1,'中'
  
union all select 2,'国'
  
union all select 3,'人'
  
union all select 4,'阿'

select * from #t order by name collate Chinese\_PRC\_CS\_AS\_KS_WS
  
drop table #t
  
/*结果：
  
id          name
  
---- -------
  
4           阿
  
2           国
  
3           人
  
1           中
  
*/

例2：让表NAME列的内容按姓氏笔划排序：

create table #t(id int,name varchar(20))

insert #t select 1,'三'
  
union all select 2,'乙'
  
union all select 3,'二'
  
union all select 4,'一'
  
union all select 5,'十'
  
select * from #t order by name collate Chinese\_PRC\_Stroke\_CS\_AS\_KS\_WS
  
drop table #t
  
/*结果：
  
id          name
  
---- -------
  
4           一
  
2           乙
  
3           二
  
5           十
  
1           三
  
*/

三、常见问题处理：

1.“无法解决 equal to 操作的排序规则冲突。”

示例1：

create table #t1(
  
name varchar(20) collate Albanian\_CI\_AI_WS,
  
value int)

create table #t2(
  
name varchar(20) collate Chinese\_PRC\_CI\_AI\_WS,
  
value int )

表建好后，执行连接查询：

select * from #t1 A inner join #t2 B on A.name=B.name

这样，错误就出现了：

服务器: 消息 446，级别 16，状态 9，行 1
  
无法解决 equal to 操作的排序规则冲突。
  
要排除这个错误，最简单方法是，表连接时指定它的排序规则，这样错误就
  
不再出现了。语句这样写：

select *
  
from #t1 A inner join #t2 B
  
on A.name=B.name collate Chinese\_PRC\_CI\_AI\_WS

示例2：

例如，在创建表时考虑使用下面的 Transact-SQL 语句：

CREATE TABLE TestTab (

id int,

GreekCol nvarchar(10) COLLATE greek\_ci\_as,

LatinCol nvarchar(10) COLLATE latin1\_general\_cs_as

)

INSERT TestTab VALUES (1, N'A', N'a')

GO

该语句创建了一个包含以下两列的表：一列使用不区分大小写和区分重音的希腊语排序规则，而另一列使用区分大小写和重音的通用 Latin1 排序规则。

您可以尝试使用查询来显式比较这两列：

SELECT *

FROM TestTab

WHERE GreekCol = LatinCol

但是，该查询会返回一个错误：

Msg 446, Level 16, State 9, Server V-MICHKA3, Line 1

无法解决等于运算的排序规则冲突。

之所以会出现此错误，是因为服务器无法使用不同的排序规则来比较两段文本。但是，如果您使用 COLLATE 关键字显式创建一个允许这两列兼容的表达式，则查询将以如下方式执行：

SELECT *

FROM TestTab

WHERE GreekCol = LatinCol COLLATE greek\_ci\_as

还需注意的是，尽管 LatinCol 通常有一个区分大小写的排序规则，但表达式不区分大小写的排序规则会将其覆盖，从而使“A”的大写和小写被视为等同。


<http://blog.sina.com.cn/s/blog_539c0c040100zxsn.html>