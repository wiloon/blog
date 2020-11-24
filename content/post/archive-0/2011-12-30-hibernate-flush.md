---
title: Hibernate flush
author: w1100n
type: post
date: 2011-12-30T03:20:10+00:00
url: /?p=2049
categories:
  - DataBase
  - Java

---
**saveOrUpdateCopy，merge和update区别**

  <div id="content">
    
      首先说明merge是用来代替saveOrUpdateCopy的，然后比较update和merge,update的作用上边说了，这里说一下merge的,如果session中存在相同持久化标识（identifier）的实例，用用户给出的对象的状态覆盖旧有的持久实例,如果session没有相应的持久实例，则尝试从数据库中加载，或创建新的持久化实例，最后返回该持久实例,用户给出的这个对象没有被关联到session上，它依旧是脱管的。重点是最后一句：
    
    
    
      当我们使用update的时候，执行完成后，我们提供的对象A的状态变成持久化状态，但当我们使用merge的时候，执行完成，我们提供的对象A还是脱管状态，Hibernate或者new了一个B，或者检索到，一个持久对象B，并把我们提供的对象A的所有的值拷贝到这个B，执行完成后B是持久状态，而我们提供的A还是托管状态。
    
    
    
      flush和update区别
    
    
    
      这两个的区别好理解update操作的是在脱管状态的对象，而flush是操作的在持久状态的对象。
    
    
    
      默认情况下，一个持久状态的对象是不需要update的，只要你更改了对象的值，等待Hibernate flush就自动保存到数据库了。Hibernate flush发生再几种情况下：
    
    
    
      1，调用某些查询的时候
    
    
    
      2，transaction commit的时候
    
    
    
      3，手动调用flush的时候
    
    
    
      lock和update区别
    
    
    
      1.update是把一个已经更改过的脱管状态的对象变成持久状态
    
    
    
      2.lock是把一个没有更改过的脱管状态的对象变成持久状态
    
    
    
      对应更改一个记录的内容，两个的操作不同：
    
    
    
      1.update的操作步骤是：更改脱管的对象->调用update
    
    
    
      2.lock的操作步骤是：调用lock把对象从脱管状态变成持久状态——>更改持久状态的对象的内容——>等待flush或者手动flush
  
