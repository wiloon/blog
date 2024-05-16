---
title: JPA的视图查询
author: "-"
date: 2015-05-20T09:04:14+00:00
url: /?p=7692
categories:
  - Inbox
tags:
  - reprint
---
## JPA的视图查询
http://blog.csdn.net/chaijunkun/article/details/8442406

本文出处: http://blog.csdn.net/chaijunkun/article/details/8442406，转载请注明。由于本人不定期会整理相关博文，会对相应内容作出完善。因此强烈建议在原始出处查看此文。

昨天晚上遇到一个需求，每天早上要生成一份报告给各个部门的Leader。实现方式基本上确定为HTML格式的电子邮件。但是数据方面犯了难。原因在于数据库中存储的数据是跨表的，而且还要做count统计，这样得到的结果就不是原生的MySQL表，我用的又是JPA技术。我们知道，使用JPA第一步就是映射实体，每一张表就至少对应一个实体 (力求严谨，因为联合主键时一张表会对应两个对象) 。可是对于灵活的查询尤其是连接查询，并不存在一个真正的表与其对应，怎么样才能解决呢？来，我们来举个"栗子"
  
假设我们有两张表，一张学院表，一张学生表。学院表里存着学院ID和学院名称，学生表里存着学生的基本信息，包括学号、学院ID和学生姓名 (其它较复杂的属性我们不看了) ，正如下面的建表语句所示: 


```sql``` 
  
- ----------
  
- Table structure for \`depts\`
  
- ----------
  
DROP TABLE IF EXISTS \`depts\`;
  
CREATE TABLE \`depts\` (
  
\`deptId\` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '学院ID',
  
\`deptName\` varchar(50) NOT NULL COMMENT '学院名称',
  
PRIMARY KEY (\`deptId\`)
  
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

- ----------
  
- Records of depts
  
- ----------
  
INSERT INTO \`depts\` VALUES ('1', '哲学院');
  
INSERT INTO \`depts\` VALUES ('2', '经济学院');
  
INSERT INTO \`depts\` VALUES ('3', '法学院');
  
INSERT INTO \`depts\` VALUES ('4', '教育学院');
  
INSERT INTO \`depts\` VALUES ('5', '文学院');
  
INSERT INTO \`depts\` VALUES ('6', '历史学院');
  
INSERT INTO \`depts\` VALUES ('7', '理学院');
  
INSERT INTO \`depts\` VALUES ('8', '工学院');
  
INSERT INTO \`depts\` VALUES ('9', '农学院');
  
INSERT INTO \`depts\` VALUES ('10', '医学院');
  
INSERT INTO \`depts\` VALUES ('11', '军事学院');
  
INSERT INTO \`depts\` VALUES ('12', '管理学院');
  
INSERT INTO \`depts\` VALUES ('13', '艺术学院');

再建立一个学生表，再随便往里面插入点数据: 


```sql``` 
  
- ----------
  
- Table structure for \`students\`
  
- ----------
  
DROP TABLE IF EXISTS \`students\`;
  
CREATE TABLE \`students\` (
  
\`stuNo\` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '学号 从1000开始',
  
\`deptId\` int(10) unsigned NOT NULL COMMENT '学院ID',
  
\`stuName\` varchar(50) NOT NULL COMMENT '学生姓名',
  
PRIMARY KEY (\`stuNo\`),
  
KEY \`FK_DEPTID\` (\`deptId\`),
  
CONSTRAINT \`FK_DEPTID\` FOREIGN KEY (\`deptId\`) REFERENCES \`depts\` (\`deptId\`) ON UPDATE CASCADE
  
) ENGINE=InnoDB AUTO_INCREMENT=1006 DEFAULT CHARSET=utf8;

- ----------
  
- Records of students
  
- ----------
  
INSERT INTO \`students\` VALUES ('1000', '13', '鸟叔');
  
INSERT INTO \`students\` VALUES ('1001', '7', '乔布斯');
  
INSERT INTO \`students\` VALUES ('1002', '3', '阿汤哥');
  
INSERT INTO \`students\` VALUES ('1003', '3', '施瓦辛格');
  
INSERT INTO \`students\` VALUES ('1004', '2', '贝克汉姆');
  
INSERT INTO \`students\` VALUES ('1005', '3', '让雷诺');

现在我们想统计一下各个学院都有多少学生。这个题目在我们学习SQL的时候再简单不过了。两种实现方法: 

使用Group By和不使用Group By: 


```sql

``` 
  
SELECT b.deptId, b.deptName, count(*) as 'totalCount' FROM students a 
LEFT JOIN depts b ON a.deptId=b.deptId GROUP BY b.deptId ORDER BY b.deptId;
  
使用Group By之后，凡是没有对应学生记录的学院都没有显示出来 (我不明白为什么。。。如果有人知道的话麻烦告诉我好吗？) 
  
 
  
+---+-----+----+
  
| deptId | deptName     | totalCount |
  
+---+-----+----+
  
|      2 | 经济学院     |          1 |
  
|      3 | 法学院       |          3 |
  
|      7 | 理学院       |          1 |
  
|     13 | 艺术学院     |          1 |
  
+---+-----+----+
  
再来一个不使用Group By的查询: 


```sql``` 
  
SELECT a.deptId, a.deptName, (SELECT count(*) FROM students b where b.deptId=a.deptId) as 'totalCount' FROM depts a;
  
这次就完全显示出来了: 


 
  
+---+-----+----+
  
| deptId | deptName     | totalCount |
  
+---+-----+----+
  
|      1 | 哲学院       |          0 |
  
|      2 | 经济学院     |          1 |
  
|      3 | 法学院       |          3 |
  
|      4 | 教育学院     |          0 |
  
|      5 | 文学院       |          0 |
  
|      6 | 历史学院     |          0 |
  
|      7 | 理学院       |          1 |
  
|      8 | 工学院       |          0 |
  
|      9 | 农学院       |          0 |
  
|     10 | 医学院       |          0 |
  
|     11 | 军事学院     |          0 |
  
|     12 | 管理学院     |          0 |
  
|     13 | 艺术学院     |          1 |
  
+---+-----+----+

至此，我们的SQL写通了。但是怎么才能使用JPA来查询出一样的视图呢？

我们按照往常编码那样，从一个主要的实体操作服务中暴露出EntityManager来: 


 
  
package net.csdn.blog.chaijunkun.dao;

import javax.persistence.EntityManager;
  
import javax.persistence.PersistenceContext;

import org.springframework.stereotype.Service;

@Service
  
public class ObjectDaoServiceImpl implements ObjectDaoService {

@PersistenceContext
  
private EntityManager entityManager;

@Override
  
public EntityManager getEntityManager(){
  
return this.entityManager;
  
}

}

这样做的好处就是所有的数据操作都来源于同一个实体管理器。将来若部署发生变化，只改这一处注入就可以了。

然后我们还需要和以前一样构造两个表的实体类: 

学院表的实体类: 


 
  
package net.csdn.blog.chaijunkun.pojo;

import java.io.Serializable;

import javax.persistence.Column;
  
import javax.persistence.Entity;
  
import javax.persistence.GeneratedValue;
  
import javax.persistence.GenerationType;
  
import javax.persistence.Id;
  
import javax.persistence.Table;

@Entity
  
@Table(name="depts")
  
public class Depts implements Serializable {

/**
  
*
  
*/
  
private static final long serialVersionUID = 3602227759878736655L;

@Id
  
@GeneratedValue(strategy= GenerationType.AUTO)
  
@Column(name= "deptId")
  
private Integer deptId;

@Column(name= "deptName", length= 50, nullable= false)
  
private String deptName;

//getters and setters...
  
}

学生表的实体类: 


 
  
package net.csdn.blog.chaijunkun.pojo;

import java.io.Serializable;

import javax.persistence.Column;
  
import javax.persistence.Entity;
  
import javax.persistence.GeneratedValue;
  
import javax.persistence.GenerationType;
  
import javax.persistence.Id;
  
import javax.persistence.JoinColumn;
  
import javax.persistence.ManyToOne;
  
import javax.persistence.Table;

@Entity
  
@Table(name= "students")
  
public class Students implements Serializable {

/**
  
*
  
*/
  
private static final long serialVersionUID = -5942212163629824609L;

@Id
  
@GeneratedValue(strategy= GenerationType.AUTO)
  
@Column(name= "stuNo")
  
private Long stuNo;

@ManyToOne
  
@JoinColumn(name= "deptId", nullable= false)  
  
private Depts depts;

@Column(name= "stuName", length= 50, nullable= false)
  
private String stuName;

//getters and setters...

}
  
两个实体类都构造好了，我们接下来还要弄一个视图类，属性的类型完全由你想要的结构来构造。例如这个例子中我们要学院编号，学院名称和总人数。那么我们就这么定义: 


 
  
package net.csdn.blog.chaijunkun.pojo;

import java.io.Serializable;

public class Report implements Serializable {

/**
  
*
  
*/
  
private static final long serialVersionUID = 4497500574990765498L;

private Integer deptId;

private String deptName;

private Integer totalCount;

public Report(){};

public Report(Integer deptId, String deptName, Integer totalCount) {
  
this.deptId = deptId;
  
this.deptName = deptName;
  
this.totalCount = totalCount;
  
}

//getters and setters...

}

可以说，视图对象的定义比实体定义还要简单，不需要注解，不需要映射 (以上代码为了减少代码量均省去了各属性的get和set方法，请自行添加) 。但是唯一不同的是我们需要额外构造一个带有字段初始化的构造函数。并且还不能覆盖默认的无参构造函数。然后我们就开始进入真正的查询了 (作为视图来讲，SQL规范中是不允许修改数据的。因此，视图仅有SELECT特性。这也是为什么很多人使用JPA想通过实体映射数据库内建视图的方式进行查询，却始终映射不成功的症结所在。) 


 
  
package net.csdn.blog.chaijunkun.dao;

import java.util.List;

import javax.annotation.Resource;
  
import javax.persistence.EntityManager;
  
import javax.persistence.TypedQuery;

import org.springframework.stereotype.Service;

import net.csdn.blog.chaijunkun.pojo.Depts;
  
import net.csdn.blog.chaijunkun.pojo.Report;
  
import net.csdn.blog.chaijunkun.pojo.Students;

@Service
  
public class ReportServiceImpl implements ReportService {

@Resource
  
private ObjectDaoService objectDaoService;

@Override
  
public List<Report> getReport() {
  
String jpql= String.format("select new %3$s(a.deptId, a.deptName, (select count(*) from %2$s b where b.deptId= a.deptId) as totalCount) from %1$s a",
  
Depts.class.getName(),
  
Students.class.getName(),
  
Report.class.getName());

EntityManager entityManager= objectDaoService.getEntityManager();
  
//建立有类型的查询
  
TypedQuery<Report> reportTypedQuery= entityManager.createQuery(jpql, Report.class);
  
//另外有详细查询条件的在jpql中留出参数位置来(?1 ?2 ?3....)，然后在这设置
  
//reportTypedQuery.setParameter(1, params);
  
List<Report> reports= reportTypedQuery.getResultList();
  
return reports;
  
}

}

在上面的代码中我们构造了JPQL中的视图查询语句。最重要的就是要在最初的select后面new出新的对象。然后把我们查询到的结果通过视图对象的构造函数灌入各个属性。由统计生成的字段最好用as重命名结果以保持和视图对象属性名称相同。这样，我们就得到了视图数据。接下来就去尝试遍历这个List吧，操作非常方便。
  
2014年3月28日补充: 

最近在查阅资料的时候发现了另外一种变通的方式——"返璞归真"，将JPA对查询的包装进行去包装，得到实现JPA底层框架的原生查询，然后再进行操作。

Query query= entityManager.createNativeQuery(sql);

此时得到了query对象，我们可以执行去包装操作: SQLQuery nativeQuery= query.unwrap(SQLQuery.class);

上面的语句是针对Hibernate的，使用其他实现框架时可以查阅手册，找找对应的Query实现类。

得到原生查询后，我们可以再设置查询参数和字段类型: 

设置参数，诸如: nativeQuery.setParameter("id",123456);

设置字段类型，诸如: nativeQuery.addScalar("id", StandardBasicTypes.LONG);

这里多说一句，当字段声明类型为bigInt (MySQL数据库) 时，Hibernate查询返回的默认类型是BigInteger，当我们使用Long类型时就会产生类型转换异常。因此这种情况必须进行addScalar操作，限定好具体类型。

当返回的结果无法进行实体映射时，我们还可以声明ORM，让其返回Map，我们自己去对象化数据。

EclipseLink的方法是: nativeQuery.setHint(QueryHints.RESULT_TYPE, ResultType.Map);

Hibernate的方法是: nativeQuery.setResultTransformer(CriteriaSpecification.ALIAS_TO_ENTITY_MAP);

此时查询的结果就得写成: List<Map<String, Object>> retVal= nativeQuery.list();

然后就对retVal进行遍历取得数据行，遍历或者随机读取Map来取得对应字段。

另外，向大家推荐一本书——Apress出版社出版的《Pro JPA 2 Mastering the Java trade Persistence API》，这本书详细介绍了JPA的相关技术，非常实用。