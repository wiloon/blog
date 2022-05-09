---
title: druid
author: "-"
date: 2016-09-22T07:15:01+00:00
url: /?p=9209
categories:
  - Inbox
tags:
  - reprint
---
## druid
### maxWait

默认值是无限大,当连接池中连接已经用完了,等待建立一个新连接的最大毫秒数 ( 在抛异常之前 )
  
获取连接时最大等待时间,单位毫秒。配置了maxWait之后,缺省启用公平锁,并发效率会有所下降,如果需要可以通过配置useUnfairLock属性为true使用非公平锁。

### poolPreparedStatements

是否缓存preparedStatement,也就是PSCache。PSCache对支持游标的数据库性能提升巨大,比如说oracle。
  
在MySQL5.5以下的版本中没有PSCache功能,建议关闭掉。5.5及以上版本有PSCache,建议开启。

### maxOpenPreparedStatements

要启用PSCache,必须配置大于0,当大于0时,poolPreparedStatements自动触发修改为true。
  
在Druid中,不会存在Oracle下PSCache占用内存过多的问题,可以把这个数值配置大一些,比如说100

### maxOpenPreparedStatements

statement cache的大小,默认为-1,也就是不限制

http://www.oschina.net/question/563890_2151605
  
https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8