---
title: MySQL 函数
author: wiloon
type: post
date: 2011-04-16T09:33:27+00:00
url: /?p=59
bot_views:
  - 6
categories:
  - DataBase
tags:
  - MySQL

---
<code class="language-sql line-numbers">mysql&gt; select date_format(now(),'%Y-%m-%d');
mysql&gt; select time_format(now(),'%H-%i-%S');

-- 连接字符串, CONCAT
select CONCAT('My', 'S', 'QL');

```

### Oracle

SQL> select to_char(sysdate,&#8217;yyyy-mm-dd&#8217;) from dual;
  
SQL> select to_char(sysdate,&#8217;hh24-mi-ss&#8217;) from dual;