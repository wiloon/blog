---
title: Mybatis多参数查询映射
author: "-"
date: 2013-01-24T14:18:12+00:00
url: /?p=5074
categories:
  - Java
tags:
  - reprint
---
## Mybatis多参数查询映射
<http://fengfan876.iteye.com/blog/1473863>

最近在做一个Mybatis的项目，由于是接触不久，虽然看了一下资料，但在实际开发中还是暴露了很多问题，其中最让我头疼的就是selete的parameterType问题，网上这类的帖子虽然有但是不全，很多情况下很难找到你想要的答案。
  
为此我对这个问题进行了总结，希望对像我这样的新手有一定的帮助。

 (一) 单个参数
  
public List<XXBean> getXXBeanList(String xxCode);

<select id="getXXXBeanList" parameterType="java.lang.String" resultType="XXBean">
  
select 字段... from XXX where code = #{xxCode}
  
</select>

其中方法名和ID一致，#{}中的参数名与方法中的参数名一直， 我这里采用的是XXXBean是采用的短名字, select 后的字段列表要和bean中的属性名一致， 如果不一致的可以用 as 来补充。

 (二) 多参数
  
public List<XXXBean> getXXXBeanList(String xxId, String xxCode);

<select id="getXXXBeanList" resultType="XXBean">
  
select 字段... from XXX where id=#{0} code = #{1}
  
</select>

由于是多参数那么就不能使用parameterType， 改用#｛index｝是第几个就用第几个的索引，索引从0开始

 (三) Map封装多参数

public List<XXXBean> getXXXBeanList(HashMap map);

<select id="getXXXBeanList" parameterType="hashmap" resultType="XXBean">
  
select 字段... from XXX where id=#{xxId} code = #{xxCode}
  
</select>

其中hashmap是mybatis自己配置好的直接使用就行。map中key的名字是那个就在#{}使用那个，map如何封装就不用了我说了吧。

 (四) List封装IN
  
public List<XXXBean> getXXXBeanList(List<String> list);

<select id="getXXXBeanList" resultType="XXBean">
  
select 字段... from XXX where id in
  
<foreach item="item" index="index" collection="list"
  
open="(" separator="," close=")">
  
#{item}
  
</foreach>
  
</select>

foreach 最后的效果是select 字段... from XXX where id in ('1','2','3','4')

结束语: 

1: 知识在于不断地运用和总结；

2: 书读百遍其义自见；

3: 熟能生巧；

再次奉上Mybatis官方的中文指南<http://fengfan876.iteye.com/blog/1485686>