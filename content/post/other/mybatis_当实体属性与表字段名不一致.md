---
title: MyBatis_当实体属性与表字段名不一致
author: "-"
date: 2014-05-07T09:01:55+00:00
url: /?p=6601
categories:
  - Inbox
tags:
  - MyBatis

---
## MyBatis_当实体属性与表字段名不一致
http://m.blog.csdn.net/blog/wuqinfei_cs/12873135


  映射


  /*
<!-- 将表字段与实体属性一一对应 -->
<resultMap type="com.hehe.mybatis.domain.User" id="userMap">
    <id column="id" property="id"/>
    <result column="name" property="username"/>
    <result column="address" property="uaddress"/>
</resultMap>

<select id="selectUserById" parameterType="string" resultMap="userMap">
    select * from user where id = #{id}
</select>