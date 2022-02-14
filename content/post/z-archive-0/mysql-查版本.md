---
title: MySQL 查看版本,version
author: "-"
date: 2011-12-25T08:41:01+00:00
url: /?p=1978
categories:
  - DataBase
  - Linux
tags:
  - MySQL

---
## MySQL 查看版本,version
MySQL -V
  
MySQL Ver 14.14 Distrib 5.5.32, for debian-linux-gnu (x86_64) using readline 6.2

# MySQL函数

select version();

### 在MySQL中: MySQL> status;

MySQL> status;

    MySQL Ver 14.7 Distrib 4.1.10a, for redhat-linux-gnu (i686)Connection id: 416
      
    SSL: Not in use
      
    Current pager: stdout
      
    Using outfile: "
      
    Using delimiter: ;
      
    Server version: 3.23.56-log
      
    Protocol version: 10
      
    Connection: Localhost via UNIX socket
      
    Client characterset: latin1
      
    Server characterset: latin1
      
    UNIX socket: /tmp/MySQL_3311.sock
      
    Uptime: 62 days 21 hours 21 min 57 secThreads: 1 Questions: 584402560 Slow queries: 424 Opens: 59664208 Flush tables: 1 Open tables: 64 Queries per second avg: 107.551

### MySQL -help

MySQL –help | grep Distrib
  
MySQL Ver 14.7 Distrib 4.1.10a, for redhat-linux-gnu (i686) 