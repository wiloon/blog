---
title: 利用spring的jdbcTemplate处理blob、clob
author: "-"
date: 2013-01-16T04:41:51+00:00
url: /?p=5034
categories:
  - Java
  - Web
tags:
  - Spring

---
## 利用spring的jdbcTemplate处理blob、clob
spring定义了一个以统一的方式操作各种数据库的Lob类型数据的LobCreator(保存的时候用),同时提供了一个LobHandler为操作二进制字段和大文本字段提供统一接口访问。
  
举例，例子里面的t_post表中post_text字段是CLOB类型,而post_attach是BLOG类型: 

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
  
String sql = " INSERT INTO t_post(post_id,user_id,post_text,post_attach)"
  
+ " VALUES(?,?,?,?)";
  
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

设置相对应的配置文件(Oracle 9i版本),Oracle的数据库最喜欢搞搞特别的东西啦: 

<bean id="nativeJdbcExtractor"

lazy-init="true" />
  
<bean id="oracleLobHandler"

lazy-init="true">
  
<property name="nativeJdbcExtractor" ref="nativeJdbcExtractor" />
  
</bean>
  
<bean id="dao" abstract="true">
  
<property name="jdbcTemplate" ref="jdbcTemplate" />
  
</bean>
  
<bean id="postDao" parent="dao"
  

  
<property name="lobHandler" ref="oracleLobHandler" />
  
</bean>

Oracle 10g或其他数据库如下设置: 

<bean id="defaultLobHandler"

lazy-init="true" />
  
<bean id="dao" abstract="true">
  
<property name="jdbcTemplate" ref="jdbcTemplate" />
  
</bean>
  
<bean id="postDao" parent="dao"
  

  
<property name="lobHandler" ref="defaultLobHandler" />
  
</bean>

读取BLOB/CLOB块,举例: 

public List getAttachs(final int userId){
  
String sql = "SELECT post_id,post_attach FROM t_post where user_id =? and post_attach is not null";
  
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