---
title: hibernate的ID生成策略
author: wiloon
type: post
date: 2014-05-29T01:47:15+00:00
url: /?p=6684
categories:
  - Uncategorized
tags:
  - JPA

---
http://www.cnblogs.com/seed_lee/archive/2011/02/14/1954720.html

hibernate的ID生成策略（annotation方式@GeneratedValue）
  
记录hibernate中使用annotation的方式实现主键生成策略：

一般情况下，hibernate中使用annotation的主键生成策略，都是使用annotation的标准注解（javax.persistence.GeneratedValue），而不是使用hibernate的扩展的annotation方式，当然，使用也是没有错的，推荐使用标准的annotation。

标准的annotation方式的主键生成策略如下：

AUTO &#8211; 可以是identity column类型,或者sequence类型或者table类型,取决于不同的底层数据库.
  
TABLE &#8211; 使用表保存id值（也就是会为应用的表创建一张专门保存Id的表，记录对应的表的对应最大的ID值,如下图）
  
CPU7@71(TD68TSQ(FD@D}MM

IDENTITY &#8211; identity column
  
SEQUENCE – sequence

下面的例子展示了使用SEQ_STORE配置的sequence生成器

@Id @GeneratedValue(strategy=GenerationType.SEQUENCE, generator=&#8221;SEQ_STORE&#8221;)
  
public Integer getId() { &#8230; }

下面这个例子使用的是identity生成器

@Id @GeneratedValue(strategy=GenerationType.IDENTITY)
  
public Long getId() { &#8230; }
  
AUTO生成器适用于可移植的应用(在多个DB间切换). 多个@Id可以共享同一个identifier生成器,只要把generator属性设成相同的值就可以了. 通过@SequenceGenerator 和@TableGenerator,你可以配置不同的identifier生成器. 每一个identifier生成器都有自己的适用范围,可以是应用级(application level)和类一级(class level). 类一级的生成器在外部是不可见的, 而且类一级的生成器可以覆盖应用级的生成器. 应用级的生成器则定义在包一级(package level)(如package-info.java):

@javax.persistence.TableGenerator(
  
name=&#8221;EMP_GEN&#8221;,
  
table=&#8221;GENERATOR_TABLE&#8221;,
  
pkColumnName = &#8220;key&#8221;,
  
valueColumnName = &#8220;hi&#8221;
  
pkColumnValue=&#8221;EMP&#8221;,
  
allocationSize=20
  
)
  
@javax.persistence.SequenceGenerator(
  
name=&#8221;SEQ_GEN&#8221;,
  
sequenceName=&#8221;my_sequence&#8221;
  
)
  
package org.hibernate.test.metadata;

如果在org.hibernate.test.metadata包下面的 package-info.java文件用于初始化EJB配置, 那么该文件中定义的 EMP\_GEN 和SEQ\_GEN都是应用级的生成器. EMP\_GEN定义了一个使用hilo算法 (max\_lo为20)的id生成器(该生成器将id的信息存在数据库的某个表中.). id的hi值保存在GENERATOR_TABLE中. 在该表中 pkColumnName&#8221;key&#8221;等价于 pkColumnValue &#8220;EMP&#8221;, 而valueColumnName &#8220;hi&#8221;中存储的是下一个要使用的最大值.

SEQ\_GEN则定义了一个sequence 生成器, 其对应的sequence名为 my\_sequence. 注意目前Hibernate Annotations还不支持sequence 生成器中的 initialValue和 allocationSize参数.

下面这个例子展示了定义在类范围(class scope)的sequence生成器:

@Entity
  
@javax.persistence.SequenceGenerator(
  
name=&#8221;SEQ_STORE&#8221;,
  
sequenceName=&#8221;my_sequence&#8221;
  
)
  
public class Store implements Serializable {
  
private Long id;

@Id @GeneratedValue(strategy=GenerationType.SEQUENCE, generator=&#8221;SEQ_STORE&#8221;)
  
public Long getId() { return id; }
  
}

在这个例子中,Store类使用名为my\_sequence的sequence,并且SEQ\_STORE 生成器对于其他类是不可见的. 注意在org.hibernate.test.metadata.id包下的测试代码有更多演示Hibernate Annotations用法的例子..

下面是定义组合主键的几种语法:

将组件类注解为@Embeddable,并将组件的属性注解为@Id
  
将组件的属性注解为@EmbeddedId
  
将类注解为@IdClass,并将该实体中所有属于主键的属性都注解为@Id
  
对于EJB2的开发人员来说 @IdClass是很常见的, 但是对于Hibernate的用户来说就是一个崭新的用法. 组合主键类对应了一个实体类中的多个字段或属性, 而且主键类中用于定义主键的字段或属性和 实体类中对应的字段或属性在类型上必须一致.下面我们看一个例子:

@Entity
  
@IdClass(FootballerPk.class)
  
public class Footballer {
  
//part of the id key
  
@Id public String getFirstname() {
  
return firstname;
  
}

public void setFirstname(String firstname) {
  
this.firstname = firstname;
  
}

//part of the id key
  
@Id public String getLastname() {
  
return lastname;
  
}

public void setLastname(String lastname) {
  
this.lastname = lastname;
  
}

public String getClub() {
  
return club;
  
}

public void setClub(String club) {
  
this.club = club;
  
}

//appropriate equals() and hashCode() implementation
  
}

@Embeddable
  
public class FootballerPk implements Serializable {
  
//same name and type as in Footballer
  
public String getFirstname() {
  
return firstname;
  
}

public void setFirstname(String firstname) {
  
this.firstname = firstname;
  
}

//same name and type as in Footballer
  
public String getLastname() {
  
return lastname;
  
}

public void setLastname(String lastname) {
  
this.lastname = lastname;
  
}

//appropriate equals() and hashCode() implementation
  
}
  
如上, @IdClass指向对应的主键类.

Hibernate支持在组合标识符中定义关联(就像使用普通的注解一样),而EJB3规范并不支持此类用法.

@Entity
  
@AssociationOverride( name=&#8221;id.channel&#8221;, joinColumns = @JoinColumn(name=&#8221;chan_id&#8221;) )
  
public class TvMagazin {
  
@EmbeddedId public TvMagazinPk id;
  
@Temporal(TemporalType.TIME) Date time;
  
}

@Embeddable
  
public class TvMagazinPk implements Serializable {
  
@ManyToOne
  
public Channel channel;
  
public String name;
  
@ManyToOne
  
public Presenter presenter;
  
}

具体的详细文档，参考hibernate-annotations-index 文档，hibernate的annotation API