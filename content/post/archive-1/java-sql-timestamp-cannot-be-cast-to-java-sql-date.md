---
title: java.sql.Timestamp cannot be cast to java.sql.Date
author: "-"
date: 2015-09-22T10:05:46+00:00
url: /?p=8331
categories:
  - Uncategorized

tags:
  - reprint
---
## java.sql.Timestamp cannot be cast to java.sql.Date
java.sql.Timestamp cannot be cast to java.sql.Date
  
分类:  Java EE2010-05-10 18:14 3425人阅读 评论(0) 收藏 举报
  
date数据库sqlstringjava
  
java.lang.ClassCastException: java.sql.Timestamp cannot be cast to java.sql.Date
  
我在往数据库插入数据时用的是string型,SQL应该会转换为java.sql.Date型,但是取出值的时候不也应该是java.sql.Date型么?
  
但是这么会报这样的错误?还有一个问题,用你说的这种方式生成的java.sql.Date好像只有年月日,
  
我想要取到很详细的当前时间,包括到毫秒级别,这样应该怎样生成呢???
  
________________________________________________________
  
java.sql.Date->java.sql.Timestamp
  
new java.sql.Timestamp(yourDate.getTime());

java.sql.Timestamp->java.sql.Date
  
new java.sql.Date(yourTimestamp.getTime());

界面要显示毫秒的话,在date传到前面时转化格式即可！
  
__________________________________________________________________
  
Date b_date = new Date();(着这是util类型的)！

ps.setDate(new java.sql.Date(b_date.getTime()));(这是插入数据库是的Date)!

其中 (new java.sql.Date(b_date.getTime()));是把java类型的Date转换成sql类型的Date