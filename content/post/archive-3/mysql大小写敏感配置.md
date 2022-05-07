---
title: MySQL大小写敏感配置, COLLATE
author: "-"
date: 2019-07-02T05:13:32+00:00
url: /?p=14600
categories:
  - Uncategorized

tags:
  - reprint
---
## MySQL大小写敏感配置, COLLATE

<https://blog.csdn.net/fdipzone/article/details/73692929>

```sql
show global variables like '%lower_case%';
```

lower_case_file_system
  
表示当前系统文件是否大小写敏感，只读参数，无法修改。

ON 大小写不敏感
  
OFF 大小写敏感

lower_case_table_names
  
表示表名是否大小写敏感，可以修改。

lower_case_table_names = 0时，MySQL会根据表名直接操作，大小写敏感。
  
lower_case_table_names = 1时，MySQL会先把表名转为小写，再执行操作。

设置lower_case_table_names的值

打开my.cnf文件，加入以下语句后重启。

lower_case_table_names = 0 或 lower_case_table_names = 1

### 解决MySQL查询不区分大小写

MySQL默认的字符检索策略: utf8_general_ci，表示不区分大小写；utf8_general_cs表示区分大小写，utf8_bin表示二进制比较，同样也区分大小写 。 (注意: 在MySQL5.6.10版本中，不支持utf8_genral_cs！！！！)

创建表时，直接设置表的collate属性为utf8_general_cs或者utf8_bin；如果已经创建表，则直接修改字段的Collation属性为utf8_general_cs或者utf8_bin。

```sql
-- 创建表: 
CREATE TABLE testt(
id INT PRIMARY KEY,
name VARCHAR(32) NOT NULL
) ENGINE = INNODB COLLATE =utf8_bin;

-- 修改表结构的Collation属性
ALTER TABLE TABLENAME MODIFY COLUMN COLUMNNAME VARCHAR(50) BINARY CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL;
```

COLLATE: 排序规则
  
对于MySQL中那些字符类型的列，如VARCHAR，CHAR，TEXT类型的列，都需要有一个COLLATE类型来告知MySQL如何对该列进行排序和比较。简而言之，COLLATE会影响到ORDER BY语句的顺序，会影响到WHERE条件中大于小于号筛选出来的结果，会影响**DISTINCT**、**GROUP BY**、**HAVING**语句的查询结果。另外，MySQL建索引的时候，如果索引列是字符类型，也会影响索引创建，只不过这种影响我们感知不到。总之，凡是涉及到字符类型比较或排序的地方，都会和COLLATE有关。

作者: 腾讯云加社区
  
链接: <https://juejin.im/post/5bfe5cc36fb9a04a082161c2>
  
来源: 掘金
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

直接修改sql语句，在要查询的字段前面加上binary关键字即可。
  
- 在每一个条件前加上binary关键字
  
select * from user where binary username = 'admin' and binary password = 'admin';

- 将参数以binary(")包围
  
select * from user where username like binary('admin') and password like binary('admin');

utf8_general_ci 不区分大小写，这个你在注册用户名和邮箱的时候就要使用。
  
utf8_general_cs 区分大小写，如果用户名和邮箱用这个 就会照成不良后果
  
utf8_bin:字符串每个字符串用二进制数据编译存储。 区分大小写，而且可以存二进制的内容

用了这么长时间，发现自己竟然不知道utf_bin和utf_general_ci这两者到底有什么区别。。
  
ci是 case insensitive, 即 "大小写不敏感", a 和 A 会在字符判断中会被当做一样的;
  
bin 是二进制, a 和 A 会别区别对待.
  
例如你运行:
  
SELECT * FROM table WHERE txt = 'a'
  
那么在utf8_bin中你就找不到 txt = 'A' 的那一行, 而 utf8_general_ci 则可以.

本文转载自: <http://blog.csdn.net/chenghuan1990/article/details/10078931>

> 部分引用自文章: <http://www.imooc.com/article/14190>

> <https://blog.csdn.net/Veir_123/article/details/73730751>
