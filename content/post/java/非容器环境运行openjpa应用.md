---
title: 非容器环境运行OpenJPA应用
author: "-"
date: 2011-12-25T09:33:57+00:00
url: /?p=1986
categories:
  - Uncategorized

tags:
  - reprint
---
## 非容器环境运行OpenJPA应用
参考来源: <http://lxy19791111.iteye.com/blog/184113>

2.Animal.java

```java
   
package com.openjpa.entity;

import javax.persistence.Basic;
   
import javax.persistence.Entity;
   
import javax.persistence.GeneratedValue;
   
import javax.persistence.GenerationType;
   
import javax.persistence.Id;
   
import javax.persistence.SequenceGenerator;

/**
   
* Animal 用于表征系统中的Animal对象，他有两个属性

* id - 编号，编号将由Oracle数据库自动生成

* name - Animal的名称
   
*/
   
/* Entity注释表示该类是持久化类，的name属性是该实体在查询中对应的唯一名称，默认是类名 */
   
@Entity
   
public class Animal {
   
// 名称
   
@Basic
   
private String name;

// 编号
   
/* Id注释表示该字段是标识字段 */
   
@Id
   
//for oracle
   
//@GeneratedValue(strategy = GenerationType.SEQUENCE, generator="SEQ_ANIMAL")
   
//@SequenceGenerator(name="SEQ_ANIMAL", sequenceName="SEQ_ANIMAL")
   
//for MySQL
  
@GeneratedValue(strategy = GenerationType.IDENTITY)
  
private int id;

public int getId() {
   
return id;
   
}

public void setId(int id) {
   
this.id = id;
   
}

public String getName() {
   
return name;
   
}

public void setName(String name) {
   
this.name = name;
   
}

}
  
```

AnimalDAO.java

```java
   
package com.openjpa.dao;

import java.util.List;
  
import com.openjpa.entity.Animal;

/**
   
* @author king
   
*
   
*/
   
public interface AnimalDAO {
   
/**
   
* 增加新的Animal对象
   
*
   
* @param animal
   
* 新的Animal对象
   
*/
   
public void persistAnimal(Animal animal);

/**
   
* 修改Animal对象的信息
   
*
   
* @param animal
   
* 修改后的Animal对象
   
*/
   
public void updateAnimal(Animal animal);

/**
   
* 删除Animal对象
   
*
   
* @param id
   
* 被删除的Animal对象
   
*/
   
public void removeAnimal(int id);

/**
   
* 根据id查找符合条件的Animal
   
*
   
* @param id
   
* animal的编号
   
* @return 编号为指定id的Animal对象
   
*/
   
public Animal getAnimalByPrimaryKey(int id);

/**
   
* 根据输入的名称字符串模糊查找所有符合条件的Animal对象列表
   
*
   
* @param name
   
* Animal对象名称
   
* @return 符合条件的Animal对象列表
   
*/
   
public List findAnimalsByName(String name);

}
  
```

AnimalDAOImpl.java
  
```java
   
package com.openjpa.impl.ejb3;

import java.util.List;

import javax.persistence.EntityManager;
   
import javax.persistence.EntityManagerFactory;
   
import javax.persistence.Persistence;
   
import javax.persistence.Query;

import com.openjpa.dao.AnimalDAO;
   
import com.openjpa.entity.Animal;

/**
   
* AnimalDAOImpl 演示了如何使用OpenJPA访问数据库的方法和步骤
   
*
   
* @author king
   
*
   
*/
   
public class AnimalDAOImpl implements AnimalDAO {

/**
   
* removeAnimal方法可以从数据库中删除指定编号的Animal对象
   
*
   
* @param id
   
* Animal对象的编号
   
*/
   
public void removeAnimal(int id) {
   
// 获取EntityManagerFactory
   
EntityManagerFactory factory = Persistence
   
.createEntityManagerFactory("oracle");
   
// 获取EntityManager
   
EntityManager em = factory.createEntityManager();
   
// 开始事务处理
   
em.getTransaction().begin();

// 使用Query删除对象
   
em.createQuery("delete from Animal animal where animal.id=" + id)
   
.executeUpdate();

// 我们还可以选择通过对象来完成
   
/*
   
* // 从EntityManager中查询到符合条件的对象 Animal animal =
   
* em.find(Animal.class,id); // 调用EntityManager的remove方法删除对象
   
* em.remove(animal);
   
*/

// 提交事务
   
em.getTransaction().commit();
   
// 关闭EntityManager
   
em.close();
   
// 关闭EntityManagerFactory
   
factory.close();

}

/**
   
* findAnimalsByName 通过输入的name内容模糊查找符合条件的Animal对象列表
   
*
   
* @param name
   
* Animal对象的name
   
* @return 符合模糊查找条件的Animal对象列表
   
*/
   
public List findAnimalsByName(String name) {
   
// 获取EntityManagerFactory
   
EntityManagerFactory factory = Persistence
   
.createEntityManagerFactory("oracle");
   
// 获取EntityManager
   
EntityManager em = factory.createEntityManager();

/*
   
* 通过EntityManager的createQuery方法获取Query对象
   
* createQuery方法的参数是JPQL查询语句，JPQL语句的语法请参考OpenJPA的帮助文档.
   
*
   
* 由于查询不需要事务的支持，因此Query操作的前后没有出现begin、commit方法的调用
   
*
   
*/
   
Query q = em.createQuery("select animal from Animal animal where animal.name like :name");
   
q.setParameter("name", "%" + name + "%");
   
List l = q.getResultList();
   
// 关闭EntityManager
   
em.close();
   
// 关闭EntityManagerFactory
   
factory.close();

return l;
   
}

/**
   
* getAnimalByPrimaryKey 方法可以查找符合条件的单个Animal对象，如果不存在对应的Animal对象将返回null
   
*
   
* @param id
   
* Animal对象的编号
   
* @return 唯一符合条件的Animal对象
   
*
   
*/
   
public Animal getAnimalByPrimaryKey(int id) {
   
// 获取EntityManagerFactory
   
EntityManagerFactory factory = Persistence
   
.createEntityManagerFactory("oracle");
   
// 获取EntityManager
   
EntityManager em = factory.createEntityManager();

// 查找符合条件的对象
   
Animal animal = em.find(Animal.class, id);

// 关闭EntityManager
   
em.close();
   
// 关闭EntityManagerFactory
   
factory.close();

return animal;
   
}

/**
   
* 将对象持久化到数据库中
   
*
   
* @param animal
   
* 需要被持久化的对象
   
*/
   
public void persistAnimal(Animal animal) {
   
// 获取EntityManagerFactory
   
EntityManagerFactory factory = Persistence
   
.createEntityManagerFactory("oracle");
   
// 获取EntityManager
   
EntityManager em = factory.createEntityManager();
   
// 开始事务处理
   
em.getTransaction().begin();

// 持久化对象
   
em.persist(animal);

// 提交事务
   
em.getTransaction().commit();
   
// 关闭EntityManager
   
em.close();
   
// 关闭EntityManagerFactory
   
factory.close();
   
}

/*
   
* (non-Javadoc)
   
*
   
* @see org.vivianj.openjpa.AnimalDAO#updateAnimal(org.vivianj.openjpa.entity.Animal)
   
*/
   
public void updateAnimal(Animal animal) {
   
// 获取EntityManagerFactory
   
EntityManagerFactory factory = Persistence
   
.createEntityManagerFactory("oracle");
   
// 获取EntityManager
   
EntityManager em = factory.createEntityManager();
   
// 开始事务处理
   
em.getTransaction().begin();

// 持久化对象
   
em.merge(animal);

// 提交事务
   
em.getTransaction().commit();
   
// 关闭EntityManager
   
em.close();
   
// 关闭EntityManagerFactory
   
factory.close();

}

}

```

3.persistence.xml
  
```xml
  
<?xml version="1.0" encoding="UTF-8"?>
  
<persistence xmlns="http://java.sun.com/xml/ns/persistence"
      
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0">

<persistence-unit name="oracle" transaction-type="RESOURCE_LOCAL">
          
<provider>
              
org.apache.openjpa.persistence.PersistenceProviderImpl
          
</provider>
          
<class>com.openjpa.entity.Animal</class>

<properties>
              
<property name="openjpa.ConnectionURL" value="jdbc:oracle:thin:@192.168.1.8:1521:test" />
              
<property name="openjpa.ConnectionDriverName" value="oracle.jdbc.OracleDriver" />
              
<property name="openjpa.ConnectionUserName" value="test" />
              
<property name="openjpa.ConnectionPassword" value="test" />
              
<property name="openjpa.Log" value="SQL=TRACE" />
          
</properties>
      
</persistence-unit>

<persistence-unit name="MySQL" transaction-type="RESOURCE_LOCAL">
          
<provider>
              
org.apache.openjpa.persistence.PersistenceProviderImpl
          
</provider>

<class>com.wiloon.openjpa.entity.Animal</class>

<properties>
              
<property name="openjpa.ConnectionURL" value="jdbc:MySQL://localhost:3306/tmp" />
              
<property name="openjpa.ConnectionDriverName" value="com.MySQL.jdbc.Driver" />
              
<property name="openjpa.ConnectionUserName" value="wiloon" />
              
<property name="openjpa.ConnectionPassword" value="xxx" />
              
<property name="openjpa.Log"
                  
value="DefaultLevel=WARN, Runtime=INFO, Tool=INFO, SQL=TRACE"/>
          
</properties>
      
</persistence-unit>
  
</persistence>
  
```

4.本人使用的是MySQL，Animal表的id为自增序列，开始前我们可在数据库中给id设置自增: 
  
```sql
  
alter table Animal modify column id integer not null auto_increment, add primary key (id);
  
```

创建Animal表:
  
```sql
  
create table Animal (id int not null,name varchar(256));
  
```

5.gradle配置文件:build.gradle
  
```java
  
apply plugin: 'java'
  
apply plugin: 'eclipse'

sourceCompatibility = 1.7

repositories{
      
mavenCentral( )
  
}

dependencies{
      
compile "MySQL:MySQL-connector-java:5.1.18"
      
compile "org.apache.openjpa:openjpa-persistence-jdbc:1.2.0"
      
testCompile group:'junit', name:'junit', version:'4.10'
  
}

```
  
5.运行TestAnimalDaoImpl.java测试即可见效果: 
  
```java
  
package com.wiloon.openjpa.dao;

import java.util.List;
  
import org.junit.Test;
  
import com.wiloon.openjpa.dao.impl.AnimalDaoImpl;
  
import com.wiloon.openjpa.entity.Animal;

public class TestAnimalDaoImpl {
      
@Test
      
public void testAnimal() {
      
AnimalDao animalDao = new AnimalDaoImpl();

// 新增
      
Animal a = new Animal();
      
a.setName("rabbit");
      
animalDao.persistAnimal(a);

// 查询
      
List animals = animalDao.findAnimalsByName("rabbit");
      
for (Animal animal : animals) {
          
System.out.println("name = " + animal.getName());
      
}

// 查询单个
      
Animal an = animalDao.getAnimalByPrimaryKey(2);
      
System.out.println("Aniaml id = " + a.getId() + " , name = " + an.getName());

// 删除
      
//animalDao.removeAnimal(a.getId());

// 查询
      
animals = animalDao.findAnimalsByName("rabbit");
      
for (Animal animal : animals) {
          
System.out.println("name = " + animal.getName());
      
}

}

}
  
```