---
title: JPA EntityManager的四个主要方法 ——persist,merge,refresh和remove
author: "-"
date: 2014-05-28T08:42:21+00:00
url: /?p=6676
categories:
  - Uncategorized
tags:
  - JPA

---
## JPA EntityManager的四个主要方法 ——persist,merge,refresh和remove
public void persist(Object entity)
  
persist 方法可以将实例转换为 managed( 托管 ) 状态。在调用 flush() 方法或提交事物后,实例将会被插入到数据库中。


对不同状态下的实例 A , persist 会产生以下操作 :

1. 如果 A 是一个 new 状态的实体,它将会转为 managed 状态；

2. 如果 A 是一个 managed 状态的实体,它的状态不会发生任何改变。但是系统仍会在数据库执行 INSERT 操作；

3. 如果 A 是一个 removed( 删除 ) 状态的实体,它将会转换为受控状态；

4. 如果 A 是一个 detached( 分离 ) 状态的实体,该方法会抛出 IllegalArgumentException 异常,具体异常根据不同的 JPA 实现有关。

public void merge(Object entity)
  
merge 方法的主要作用是将用户对一个 detached 状态实体的修改进行归档,归档后将产生一个新的 managed 状态对象。


对不同状态下的实例 A , merge 会产生以下操作 :

1. 如果 A 是一个 detached 状态的实体,该方法会将 A 的修改提交到数据库,并返回一个新的 managed 状态的实例 A2 ；

2. 如果 A 是一个 new 状态的实体,该方法会产生一个根据 A 产生的 managed 状态实体 A2 ;

3. 如果 A 是一个 managed 状态的实体,它的状态不会发生任何改变。但是系统仍会在数据库执行 UPDATE 操作；

4. 如果 A 是一个 removed 状态的实体,该方法会抛出 IllegalArgumentException 异常。

public void refresh(Object entity)
  
refresh 方法可以保证当前的实例与数据库中的实例的内容一致。


对不同状态下的实例 A , refresh 会产生以下操作 :

1. 如果 A 是一个 new 状态的实例,不会发生任何操作,但有可能会抛出异常,具体情况根据不同 JPA 实现有关；

2. 如果 A 是一个 managed 状态的实例,它的属性将会和数据库中的数据同步；

3. 如果 A 是一个 removed 状态的实例,不会发生任何操作 ;

4. 如果 A 是一个 detached 状态的实体,该方法将会抛出异常。

public void remove(Object entity)
  
remove 方法可以将实体转换为 removed 状态,并且在调用 flush() 方法或提交事物后删除数据库中的数据。


对不同状态下的实例 A , remove 会产生以下操作 :

1. 如果 A 是一个 new 状态的实例, A 的状态不会发生任何改变,但系统仍会在数据库中执行 DELETE 语句；

2. 如果 A 是一个 managed 状态的实例,它的状态会转换为 removed ；

3. 如果 A 是一个 removed 状态的实例,不会发生任何操作 ;

4. 如果 A 是一个 detached 状态的实体,该方法将会抛出异常。


http://yanchao90.blog.163.com/blog/static/1794602520112126051348/