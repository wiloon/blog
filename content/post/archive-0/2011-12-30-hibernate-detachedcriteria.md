---
title: Hibernate DetachedCriteria
author: wiloon
type: post
date: 2011-12-30T03:53:00+00:00
url: /?p=2054
categories:
  - DataBase
  - Java

---
Hibernate DetachedCriteria，这是一个非常有意义的特性！我们知道，在常规的Web编程中，有大量的动态条件查询，即用户在网页上面自由选择某些条件，程序根据用户的选择条件，动态生成SQL语句，进行查询。

针对这种需求，对于分层应用程序来说，Web层需要传递一个查询的条件列表给业务层对象，业务层对象获得这个条件列表之后，然后依次取出条件，构造查询语句。这里的一个难点是条件列表用什么来构造？传统上使用Map，但是这种方式缺陷很大，Map可以传递的信息非常有限，只能传递name和value，无法传递究竟要做怎样的条件运算，究竟是大于，小于，like，还是其它的什么，业务层对象必须确切掌握每条entry的隐含条件。因此一旦隐含条件改变，业务层对象的查询构造算法必须相应修改，但是这种查询条件的改变是隐式约定的，而不是程序代码约束的，因此非常容易出错。

DetachedCriteria可以解决这个问题，即在web层，程序员使用DetachedCriteria来构造查询条件，然后将这个DetachedCriteria作为方法调用参数传递给业务层对象。而业务层对象获得DetachedCriteria之后，可以在session范围内直接构造Criteria，进行查询。就此，查询语句的构造完全被搬离到web层实现，而业务层则只负责完成持久化和查询的封装即可，与查询条件构造完全解耦，非常完美！这恐怕也是以前很多企图在web层代码中构造HQL语句的人想实现的梦想吧！

示例代码片段如下：

  1. DetachedCriteria <span style="color: #ff0000;">detachedCriteria</span> = <span style="color: #0000ff;">DetachedCriteria</span>.forClass(Department.class);
  2. detachedCriteria.add(Restrictions.eq("name", "department")).
  
    createAlias("employees", "e").add(Restrictions.gt(("e.age"), new Integer(20)));

Department和Employee是一对多关联，查询条件为：名称是“department”开发部门；部门里面的雇员年龄大于20岁；

业务层对象使用该条件执行查询：

  1. detachedCriteria.getExecutableCriteria(session).list();

最大的意义在于，业务层代码是固定不变的，所有查询条件的构造都在web层完成，业务层只负责在session内执行之。这样代码就可放之四海而皆准，都无须修改了。然而Spring和Hibernate DetachedCriteria有不兼容的问题，因此在Spring环境下面使用Hibernate3需要注意：

Spring的HibernateTemplate提供了Hibernate的完美封装，即通过匿名类实现回调，来保证Session的自动资源管理和事务的管理。其中核心方法是：

  1. HibernateTemplate.execute(new HibernateCallback() {
  2. public Object doInHibernate(Session session) throws HibernateException {
  3. &#8230;.
  4. }
  5. }

回调方法提供了session作为参数，有了session，就可以自由的使用Hibernate API编程了。使用了spring的之后，代码修改如下：

  1. DetachedCriteria <span style="color: #ff0000;">detachedCriteria</span> = <span style="color: #0000ff;">DetachedCriteria</span>.forClass(Department.class);
  2. detachedCriteria.createAlias("employees", "e").
  
    add(Restrictions.eq("name", "department")).
  
    add(Restrictions.gt(("e.age"), new Integer(20)));
  3. departmentManager.findByCriteria(detachedCriteria);