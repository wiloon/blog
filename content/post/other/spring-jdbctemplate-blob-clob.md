---
title: "利用 Spring 的 JdbcTemplate 处理 BLOB、CLOB"
author: "-"
date: 2013-01-16T04:41:51+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: spring-jdbctemplate-blob-clob
categories:
  - Java
tags:
  - Spring
  - jdbc
  - remix
  - AI-assisted
aliases:
  - /利用spring的jdbctemplate处理blob、clob/
---
## 利用spring的jdbcTemplate处理blob、clob
spring定义了一个以统一的方式操作各种数据库的Lob类型数据的LobCreator(保存的时候用),同时提供了一个LobHandler为操作二进制字段和大文本字段提供统一接口访问。
  
举例，例子里面的t_post表中post_text字段是CLOB类型,而post_attach是BLOG类型: 

```java
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
```

设置相对应的配置文件(Oracle 9i版本),Oracle的数据库最喜欢搞搞特别的东西啦: 

```xml
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
```

Oracle 10g或其他数据库如下设置: 

```xml
<bean id="defaultLobHandler"
lazy-init="true" />
<bean id="dao" abstract="true">
<property name="jdbcTemplate" ref="jdbcTemplate" />
</bean>
<bean id="postDao" parent="dao"
<property name="lobHandler" ref="defaultLobHandler" />
</bean>
```

读取BLOB/CLOB块,举例: 

```java
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
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `spring-jdbctemplate-blob-clob.md`；title 改为「利用 Spring 的 JdbcTemplate 处理 BLOB、CLOB」；url 改为 `spring-jdbctemplate-blob-clob`；旧 url 加入 aliases；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
