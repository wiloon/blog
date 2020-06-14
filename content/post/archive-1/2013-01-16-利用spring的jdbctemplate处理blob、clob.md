---
title: 利用spring的jdbcTemplate处理blob、clob
author: wiloon
type: post
date: 2013-01-16T04:41:51+00:00
url: /?p=5034
categories:
  - Java
  - Web
tags:
  - Spring

---
spring定义了一个以统一的方式操作各种数据库的Lob类型数据的LobCreator(保存的时候用),同时提供了一个LobHandler为操作二进制字段和大文本字段提供统一接口访问。
  
举例，例子里面的t\_post表中post\_text字段是CLOB类型,而post_attach是BLOG类型：

public class PostJdbcDao extends JdbcDaoSupport implements PostDao {
  
private LobHandler lobHandler;
  
private DataFieldMaxValueIncrementer incre;
  
public LobHandler getLobHandler() {
  
return lobHandler;
  
}
  
public void setLobHandler(LobHandler lobHandler) {
  
this.lobHandler = lobHandler;
  
}
  
public void addPost(final Post post) {
  
String sql = &#8221; INSERT INTO t\_post(post\_id,user\_id,post\_text,post_attach)&#8221;
  
+ &#8221; VALUES(?,?,?,?)&#8221;;
  
getJdbcTemplate().execute(
  
sql,
  
new AbstractLobCreatingPreparedStatementCallback(
  
this.lobHandler) {
  
protected void setValues(PreparedStatement ps,
  
LobCreator lobCreator) throws SQLException {
  
ps.setInt(1, incre.nextIntValue());
  
ps.setInt(2, post.getUserId());
  
lobCreator.setClobAsString(ps, 3, post.getPostText());
  
lobCreator.setBlobAsBytes(ps, 4, post.getPostAttach());
  
}
  
});
  
}
  
}

设置相对应的配置文件(Oracle 9i版本),Oracle的数据库最喜欢搞搞特别的东西啦：

<bean id=&#8221;nativeJdbcExtractor&#8221;

lazy-init=&#8221;true&#8221; />
  
<bean id=&#8221;oracleLobHandler&#8221;

lazy-init=&#8221;true&#8221;>
  
<property name=&#8221;nativeJdbcExtractor&#8221; ref=&#8221;nativeJdbcExtractor&#8221; />
  
</bean>
  
<bean id=&#8221;dao&#8221; abstract=&#8221;true&#8221;>
  
<property name=&#8221;jdbcTemplate&#8221; ref=&#8221;jdbcTemplate&#8221; />
  
</bean>
  
<bean id=&#8221;postDao&#8221; parent=&#8221;dao&#8221;
  
>
  
<property name=&#8221;lobHandler&#8221; ref=&#8221;oracleLobHandler&#8221; />
  
</bean>

Oracle 10g或其他数据库如下设置：

<bean id=&#8221;defaultLobHandler&#8221;

lazy-init=&#8221;true&#8221; />
  
<bean id=&#8221;dao&#8221; abstract=&#8221;true&#8221;>
  
<property name=&#8221;jdbcTemplate&#8221; ref=&#8221;jdbcTemplate&#8221; />
  
</bean>
  
<bean id=&#8221;postDao&#8221; parent=&#8221;dao&#8221;
  
>
  
<property name=&#8221;lobHandler&#8221; ref=&#8221;defaultLobHandler&#8221; />
  
</bean>

读取BLOB/CLOB块,举例：

public List getAttachs(final int userId){
  
String sql = "SELECT post\_id,post\_attach FROM t\_post where user\_id =? and post_attach is not null&#8221;;
  
return getJdbcTemplate().query(
  
sql,new Object[] {userId},
  
new RowMapper() {
  
public Object mapRow(ResultSet rs, int rowNum) throws SQLException {
  
Post post = new Post();
  
int postId = rs.getInt(1);
  
byte[] attach = lobHandler.getBlobAsBytes(rs, 2);
  
post.setPostId(postId);
  
post.setPostAttach(attach);
  
return post;
  
}
  
});
  
}