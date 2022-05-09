---
title: jpa annotation, 注解
author: "-"
date: 2014-05-28T09:17:04+00:00
url: /?p=6678
categories:
  - Inbox
tags:
  - JPA

---
## jpa annotation, 注解
http://mzhj.iteye.com/blog/711685


**@Embedded**

你可以创建一个类被嵌套在实体类中，在这种情况下我们可以使用@Embedded注解。例如，在Hotel类中 可能会有一个Address。
  
Address是Hotel不可分割的一部分，没有ID, 并且不会被存储在分开的collection中。在这种情况下我们可以使用@Embedded注解


**@Entity**

标识这个pojo是一个jpa实体

Specifies that the class is an entity. This annotation is applied to the entity class.


@Table (name= users )

//指定表名为users


@Column

@Column(name="DESC", nullable=false, length=512)

设置字段类型
  
通过@Column注解设置，包含的设置如下
  
.name: 字段名
  
.unique: 是否唯一
  
.nullable: 是否可以为空
  
.inserttable: 是否可以插入
  
.updateable: 是否可以更新
  
.columnDefinition: 定义建表时创建此列的DDL
  
.secondaryTable: 从表名。如果此列不建在主表上 (默认建在主表) ，该属性定义该列所在从表的名字。

@Column(name = "user_code", nullable = false, length=32)//设置属性userCode对应的字段为user_code，长度为32，非空
  
private String userCode;
  
@Column(name = "user_wages", nullable = true, precision=12, scale=2)//设置属性wages对应的字段为user_wages，12位数字可保留两位小数，可以为空
  
private double wages;
  
@Temporal(TemporalType.DATE)//设置为时间类型
  
private Date joinDate;


@Id

设置主键


字段排序
  
在加载数据的时候可以为其指定顺序，使用@OrderBy注解实现

@OrderBy(name = "group_name ASC, name DESC")


主键生成策略

public class Users implements Serializable {
  
@Id
  
@GeneratedValue(strategy=GenerationType.IDENTITY)//主键自增，注意，这种方式依赖于具体的数据库，如果数据库不支持自增主键，那么这个类型是没法用的
  
@Column(name = "user_id", nullable = false)
  
private int userId;

public class Users implements Serializable {
  
@Id
  
@GeneratedValue(strategy=GenerationType.TABLE)//通过一个表来实现主键id的自增，这种方式不依赖于具体的数据库，可以解决数据迁移的问题
  
@Column(name = "user_code", nullable = false)
  
private String userCode;

public class Users implements Serializable {
  
@Id
  
@GeneratedValue(strategy=GenerationType.SEQUENCE)//通过Sequence来实现表主键自增，这种方式依赖于数据库是否有SEQUENCE，如果没有就不能用
  
@SequenceGenerator(name="seq_user")
  
@Column(name = "user_id", nullable = false)
  
private int userId;

7.一对多映射关系
  
有T_One和T_Many两个表，他们是一对多的关系，注解范例如下
  
主Pojo

@Entity
  
@Table(name = "T_ONE")
  
public class One implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "ONE_ID", nullable = false)
  
private String oneId;
  
@Column(name = "DESCRIPTION")
  
private String description;
  
@OneToMany(cascade = CascadeType.ALL, mappedBy = "oneId")//指向多的那方的pojo的关联外键字段
  
private Collection<Many> manyCollection;

子Pojo

@Entity
  
@Table(name = "T_MANY")
  
public class Many implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "MANY_ID", nullable = false)
  
private String manyId;
  
@Column(name = "DESCRIPTION")
  
private String description;

@JoinColumn(name = "ONE_ID", referencedColumnName = "ONE_ID")//设置对应数据表的列名和引用的数据表的列名
  
@ManyToOne//设置在"一方"pojo的外键字段上
  
private One oneId;

8.多对多映射关系
  
貌似多对多关系不需要设置级联，以前用hibernate的时候着实为多对多的级联头疼了一阵子，JPA的多对多还需要实际的尝试一下才能有所体会。
  
估计JPA的多对多也是可以转换成两个一对多的。

第一个Pojo

@Entity
  
@Table(name = "T_MANYA")
  
public class ManyA implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "MANYA_ID", nullable = false)
  
private String manyaId;
  
@Column(name = "DESCRIPTION")
  
private String description;
  
@ManyToMany
  
@JoinTable(name = "TMANY1_TMANY2", joinColumns = {@JoinColumn(name = "MANYA_ID", referencedColumnName = "MANYA_ID")}, inverseJoinColumns = {@JoinColumn(name = "MANYB_ID", referencedColumnName = "MANYB_ID")})
  
private Collection<ManyB> manybIdCollection;

第二个Pojo

@Entity
  
@Table(name = "T_MANYB")
  
public class ManyB implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "MANYB_ID", nullable = false)
  
private String manybId;
  
@Column(name = "DESCRIPTION")
  
private String description;
  
@ManyToMany(mappedBy = "manybIdCollection")
  
private Collection<ManyA> manyaIdCollection;

9.一对一映射关系
  
主Pojo

@Entity
  
@Table(name = "T_ONEA")
  
public class OneA implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "ONEA_ID", nullable = false)
  
private String oneaId;
  
@Column(name = "DESCRIPTION")
  
private String description;
  
@OneToOne(cascade = CascadeType.ALL, mappedBy = "oneA")//主Pojo这方的设置比较简单，只要设置好级联和映射到从Pojo的外键就可以了。
  
private OneB oneB;

从Pojo

@Entity
  
@Table(name = "T_ONEB")
  
public class OneB implements Serializable {
  
private static final long serialVersionUID = 1L;
  
@Id
  
@Column(name = "ONEA_ID", nullable = false)
  
private String oneaId;
  
@Column(name = "DESCRIPTION")
  
private String description;
  
@JoinColumn(name = "ONEA_ID", referencedColumnName = "ONEA_ID", insertable = false, updatable = false)//设置从方指向主方的关联外键，这个ONEA_ID其实是表T_ONEA的主键
  
@OneToOne
  
private OneA oneA;

10 大字段

@Lob //对应Blob字段类型
  
@Column(name = "PHOTO")
  
private Serializable photo;
  
@Lob //对应Clob字段类型
  
@Column(name = "DESCRIPTION")
  
private String description;

11.瞬时字段
  
不需要与数据库映射的字段，在保存的时候不需要保存倒数据库

@Transient
  
private int tempValue;

public int getTempValue(){
  
get tempValue;
  
}

public void setTempValue(int value){
  
this.tempValue = value;
  
}


@Inheritance(strategy = InheritanceType.JOINED)

Single Table    InheritanceType.SINGLE_TABLE 策略为类的继承体系采用同一个表。表名是基类的名称。例如: 

InheritanceType.JOINED策略为类继承体系中的每个类创建不同的表。每个表只包含类中定义的列，因此在load一个子类的时候，JPA实现需要同时查询子类映射的表，以及通过关联查询所有的父类映射的表。PrimaryKeyJoinColumn annotation用来指定子类映射的表如何关联到父类映射的表。它有以下属性: 
  
String name: 子类映射表中的列名。如果只有一个identity filed，那么缺省使用这个field对应的列名。
  
String referencedColumnName: 父类映射表中用来关联的列名。如果只有一个identity filed，那么缺省使用这个field对应的列名。
  
String columnDefinition: 数据库中列的数据类型。只有当JPA vendor支持通过metadata创建表的时候，这个属性才被使用。

Table Per Class    InheritanceType.TABLE_PER_CLASS策略为类继承体系中的每个类创建不同的表。和InheritanceType.JOINED策略不同的是，每个表中包含所有的子类和父类中定义的所有列。因此在load一个子类的时候，JPA实现只需要同时查询子类映射的表。

http://whitesock.iteye.com/blog/173543

http://blog.csdn.net/small_love/article/details/6300310

http://guyinglong.iteye.com/blog/520461