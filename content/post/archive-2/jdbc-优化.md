---
title: JDBC 优化
author: "-"
date: 2016-01-15T08:55:00+00:00
url: /?p=8671
categories:
  - Uncategorized

tags:
  - reprint
---
## JDBC 优化
http://www.infoq.com/cn/news/2017/03/Analysis-errors-MySQL-JDBC?utm_source=infoq&utm_medium=popular_widget&utm_campaign=popular_content_list&utm_content=homepage

这部分与jdbc无关,是对于MySQL优化的普通技巧

利用查询缓存。不要把函数直接写在sql语句里；
  
当只需要一条记录时查询加上LIMIT 1；
  
尽量避免SELECT *这样写；
  
用连接池；
  
建索引；
  
更多关于MySQL的优化


MySQL性能优化的最佳20+条经验
  
完全优化MySQL数据库性能的八大巧方法
  
jdbc的优化: 

尽量少用元数据方法；
  
尽量避免null。MySQL中对值为null情况花费更多的空间和处理而加重负担,应该指定专门的值来表示空值,在方法调用时传参也要避免null；
  
善用哑查询。在仅想得到表信息等而不需要返回记录的情况下,使用"select * from tableName where 1=0"这样的哑查询就能免于遍历；
  
善用预处理 (PreparedStatement,PreparedCall) 。PreparedStatement不但具有一次编译重复使用的优势,而且因为jdbc默认将参数以字符串形式传给数据库,而用PreparedStatement设参数则可以显式地指定数据类型,避免参数传递和来回转换的负担；
  
Java代码
  
pstmt=conn.preparedStatement(&quot;insert into test_table(......) values(....?)&quot;;

[code language=""][/code]

pstmt.setString(1,&quot;aaa&quot;;
  
pstmt.addBatch();
  
pstmt.setString(1,&quot;bbb&quot;);
  
pstmt.addBatch();
  
.....
  
pstmt.executeBatch();
  
合理选择excute方法,杀鸡就用鸡刀。execute(String sql)方法返回一个boolean值,它执行任意复杂的sql语句,可以产生多个结果集。如果有结果产生返回 true,如果没有结果集产生或仅是一个更新记数则返回 false。它产生的结果集可以通过getResultSet()和getMoreResults()获得,更新记数可通过getUpdateCount()获得。显然execute(String sql)方法的使用要复杂一些,因此如果只是简单的查询或更新操作请使用executeQuery(String sql)和executeUpdate(String sql)方法。executeUpdate(String sql)能执行INSERT,UPDATE,DELETE语句,及DDL和DML命令 (此时返回值为0) ；
  
批执行更高效。stmt.addBatch(String sql); stmt.executeBatch();
  
最好手动提交。不但可以可以保证数据原子性,而且对新能提高留下余地
  
Java代码
  
try{
  
boolean commitStat = connection.getAutoCommit();
  
connection.setAutoCommit(false);
  
// TODO: 用PreparedStatement  性能比Statementh好.
  
connection.commit();
  
connection.setAutoCommit(commitStat);
  
} catch(SQLException e){
  
} finally{
  
// TODO
  
if(connection!=null){
  
connection.close();
  
}
  
}
  
及时显式地关闭rs、stmt和conn (conn可以交由连接池管理) ；
  
使用数据库系统的强大查询功能去组织数据。这样程序运行是和数据库服务的交互次数少,数据库返回给程序的记录条数少的多,所以性能有很大的提高；
  
在rs中,正确使用get和set方法。使用列序号而不是字段名作为参数性能比较高；例如 Java代码
  
getInt(1,100);
  
setString(2,"aaaa");
  
比
  
getInt("id","100");
  
setString("name","aaaa");
  
性能好
  
以下并不完全理解,先记着: 
  
建立conn时适当合适的参数。setDefaultRowPrefetch(int) 和 setDefaultBatchValue(int) 两个参数可以优化连接； Java代码
  
Properties props=new Properties();
  
// TODO username pwd等参数
  
props.put("defaultRowPrefectch","30");
  
props.put("dufaultBatchValue","5");

Connection con=DriverManager.getConnection(url, props);

通过setFetchSize()和getFectchSize()方法来设定和查看这个参数。这个参数对体统的性能影响比较大,太小会严重地降低程序地性能.Connection Statement ResultSet都有这个参数,他们对性能地影响顺序是:rs>stmt>conn;
  
适当的选择事务的隔离级别。 TRANSACTION_READ_UNCOMMITED 性能最高；TRANSACTION_READ_COMMITED 快；TRANSACTION_REFEATABLE_READ 中等；RANSACTION_SERIALIZABLE 慢
  
在rs优化上,设置适当的滚动方向。有3个方向FETCH_FORWORD,FETCH_REVERSE FETCH_UNKNOWN单向滚动性能比较高；