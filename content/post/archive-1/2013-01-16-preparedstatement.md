---
title: PreparedStatement
author: wiloon
type: post
date: 2013-01-16T04:30:38+00:00
url: /?p=5027
categories:
  - DataBase

---
<span style="color: #000000;">jdbc(java database connectivity，java数据库连接)的api中的主要的四个类之一的java.sql.statement要求开发者付出大量的时间和精力。在使用statement获取jdbc访问时所具有的一个共通的问题是输入适当格式的日期和时间戳：2002-02-05 20:56 或者 02/05/02 8:56 pm。 </span>
  
<span style="color: #000000;">通过使用java.sql.<strong>preparedstatement</strong>，这个问题可以自动解决。一个<strong>preparedstatement</strong>是从java.sql.connection对象和所提供的sql字符串得到的，sql字符串中包含问号（?），这些问号标明变量的位置，然后提供变量的值，最后执行语句，例如： </span>
  
<span style="color: #000000;">stringsql = &#8220;select * from people p where p.id = ? and p.name = ?&#8221;;</span>
  
<span style="color: #000000;"><strong>preparedstatement</strong> ps = connection.preparestatement(sql);</span>
  
<span style="color: #000000;">ps.setint(1,id);</span>
  
<span style="color: #000000;">ps.setstring(2,name);</span>
  
<span style="color: #000000;">resultset rs = ps.executequery(); </span>
  
<span style="color: #000000;">使用<strong>preparedstatement</strong>的另一个优点是字符串不是动态创建的。下面是一个动态创建字符串的例子： </span>
  
<span style="color: #000000;">stringsql = &#8220;select * from people p where p.i = &#8220;+id; </span>

<span style="color: #000000;">这允许jvm（javavirtual machine，java虚拟机）和驱动/数据库缓存语句和字符串并提高性能。</span>
  
<span style="color: #000000;"><strong>preparedstatement</strong>也提供数据库无关性。当显示声明的sql越少，那么潜在的sql语句的数据库依赖性就越小。</span>
  
<span style="color: #000000;">由于<strong>preparedstatement</strong>具备很多优点，开发者可能通常都使用它，只有在完全是因为性能原因或者是在一行sql语句中没有变量的时候才使用通常的statement。</span>