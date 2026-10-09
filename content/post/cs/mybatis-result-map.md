---
title: "MyBatis 实体属性与表字段名不一致"
author: "-"
date: 2014-05-07T09:01:55+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: mybatis-result-map
categories:
  - Java
tags:
  - MyBatis
  - remix
  - AI-assisted
aliases:
  - /mybatis_当实体属性与表字段名不一致/
---
## MyBatis_当实体属性与表字段名不一致
http://m.blog.csdn.net/blog/wuqinfei_cs/12873135

  映射

```java
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
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `mybatis-result-map.md`；title 改为「MyBatis 实体属性与表字段名不一致」；url 改为 `mybatis-result-map`；旧 url 加入 aliases；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
