---
title: sqlplus
author: "-"
date: 2011-11-09T06:31:28+00:00
url: /?p=1475
categories:
  - DataBase

---
## sqlplus
**连接DB**

sqlplus sys/PASSWORD@xxx.xxx.xxx.xxx:1521/orcl as sysdba


**创建用户**

create user  wiloon identified by "abcd@1234";


**授权**

grant connect,resource to wiloon;
