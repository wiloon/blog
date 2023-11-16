---
title: MySQL 备份 还原 导入 导出 export import
author: "-"
date: 2011-04-30T01:18:05+00:00
url: mysql/export/import
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL 备份 还原 导入 导出 export import

```bash
#Export:

MySQLdump -uwiloon -pPASSWORD --default-character-set=utf8 enlab >enlab.sql
#-u与username 之前可以有空格, -p与password之间可以有空格, -p后也可以不跟密码, 命令执行后会提示输入密码.

#Import:
#1.
MySQL>source /path/to/sql/abc.sql;

#2.
#MySQL -u用户名 -p密码 数据库名 < 数据库名.sql
MySQL -uusername -ppassword db_name < db_name.sql
```

[http://blog.csdn.net/myron_sqh/article/details/13016945](http://blog.csdn.net/myron_sqh/article/details/13016945)
