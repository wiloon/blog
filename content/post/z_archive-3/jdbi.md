---
title: jdbi
author: "-"
date: 2019-10-29T02:20:23+00:00
url: jdbi
categories:
  - Inbox
tags:
  - reprint
---
## jdbi

[http://jdbi.org/](http://jdbi.org/)

jdbi
  
jdbi是我比较喜欢的一个数据库中间件，它是非ORM的，特别适合于数据库固定不变的场景，即不会对应多种数据库，以后也不会更换数据库的场景。如果不是这种场景，那么使用jdbc或者最好选择hibernate等对多种数据库兼容较好的中间件。
  
基于上述使用场景，jdbi的优点有:

和jdbci比较接近，使用和掌握非常简单。
  
与时俱进，例如说现在最新的jdbi3，增加了流式编程函数式等编程风格。  
源代码的实现思路非常清晰，有一种美感。使用jdbi封装出的数据库代码也非常清晰。  

jdbi的两种风格  
  
Fluent Api

handle.createUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")

.bind("id", 2)

.bind("name", "Clarice")

.execute();
  
这里就是java8的流式风格，用连贯式表达式将一个sql实现串在一起

Declarative Api
  
// Define your own declarative interface
  
public interface UserDao {

@SqlUpdate("CREATE TABLE user (id INTEGER PRIMARY KEY, name VARCHAR)")

void createTable();

    @SqlUpdate("INSERT INTO user(id, name) VALUES (?, ?)")
    void insertPositional(int id, String name);
    
    @SqlUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")
    void insertNamed(@Bind("id") int id, @Bind("name") String name);
    
    @SqlUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")
    void insertBean(@BindBean User user);
    
    @SqlQuery("SELECT * FROM user ORDER BY name")
    @RegisterBeanMapper(User.class)
    List<User> listUsers();

}
  
声明式的主要是使用注解来实现，在实际的面向对象风格的代码中，我个人觉得声明式的比较简洁，容易阅读和维护。所以下面都按照Declarative Api的方式。

[https://www.jianshu.com/p/1ee34c858cb9](https://www.jianshu.com/p/1ee34c858cb9)
