---
title: mybatis 动态 sql
author: "-"
date: 2014-05-27T06:14:33+00:00
url: /?p=6667
categories:
  - Uncategorized
tags:
  - MyBatis

---
## mybatis 动态 sql
```xml
  
<update id="updateAuthorIfNecessary">
  
update Author
  
<set>
  
<if test="username != null">username=#{username},</if>
  
<if test="password != null">password=#{password},</if>
  
<if test="email != null">email=#{email},</if>
  
<if test="bio != null">bio=#{bio}</if>
  
</set>
  
where id=#{id}
  
</update>
  
```

http://mybatis.github.io/mybatis-3/zh/dynamic-sql.html