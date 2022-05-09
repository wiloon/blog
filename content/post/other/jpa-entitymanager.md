---
title: JPA EntityManager
author: "-"
date: 2014-04-30T03:21:18+00:00
url: /?p=6571
categories:
  - Inbox
tags:
  - JPA

---
## JPA EntityManager
1. 持久化上下文 (Persistence Context ) 


一个持久化单元 (Persistence Unit ) 就是关于一组Entity 类的命名配置。持久化单元是一个静态的概念。

一个持久化上下文 (Persistence Context ) 就是一个受管的Entity 实例的集合。每一个持久化上下文都关联一个持久化单元,持久化上下文不可能脱离持久化单元独立存在。持久化上下文中的Entity 实例就是相关联的持久化单元中的若干Entity 的实例。持久化上下文是一个动态的概念。

一个Entity 实例处于受管状态,其实质是: 该实例存在于某个持久化上下文中,并且可能被某个EntityManager 处理,也因为这个原因,所以我们说一个EntityManager 管理一个持久化上下文。

尽管持久化上下文非常重要,但是开发者不直接与之打交道,持久化上下文在应用程序中是透明的,我们需要通过EntityManager 间接管理它。


2. 容器管理的EntityManager(Container-Managed EntityManager)


通过将@PersistenceContext 注解标注在EntityManager 类型的字段上,这样得到的EntityManager 就是容器管理的EntityManager 。由于是容器管理的,所以我们不需要也不应该显式关闭注入的EntityManager 实例。

容器管理的EntityManager 又细分为两种类型: 事务范围 (Transaction ) 的和扩展的 (Extended ) 。

若@PersistenceContext 未指定type 属性,或者指定为PersistenContextType.TRANSACTION ,则表示该EntityManager 是事务范围的；若指定为PersistenContextType.EXTENDED 的,则表示该EntityManager 是扩展的。

事务范围: 事务范围的EntityManager 是无状态的,可用在无状态会话Bean 和有状态会话Bean 中。

事务范围的EntityManager 依赖于JTA 事务,每次调用EntityManager 实例的相关方法时,EntityManager 会查看是否有某个持久化上下文与当前事务关联,如果有,则使用该持久化上下文；如果没有,则EntityManager 将创建一个持久化上下文,并将该持久化上下文与当前事务关联。当事务结束,则持久化上下文消失。

扩展的: 扩展的EntityManager 只能用于有状态会话Bean 。

扩展的EntityManager 在有状态会话Bean 实例创建的时候创建一个持久化上下文,并且直到该有状态会话Bean 销毁,则相应的持久化上下文才被移除。

由于在扩展的EntityManager 中,每次方法调用都是使用的相同的持久化上下文,所以前一次方法调用时产生的受管实体在下一个方法访问时仍然为受管实体。


3. 应用程序管理的EntityManager (Application-Managed EntityManager) 


在JavaSE和JavaEE环境下创建应用程序管理的EntityManager的不同之处,并非创建EntityManager的方式不同,而是获得创建EntityManager的EntityManagerFactory的方式不同。

JavaSE环境: Persistence.createEntityManager("APU").createEntityManager();

JavaEE 环境: 使用@PersistenceUnit(unitName="APU")标注EntityManagerFactory属性。然后通过调用 emf.createEntityManager()获得EntityManager。由于EntityManager是开发者显式创建并管理的,因此需 要在用完之后调用em.close()方法将之关闭。EntityManagerFactory是容器注入的,不需要也不应该调用emf.close() 方法。

在JavaSE环境下,Persistence类有两个重载的createEntityManagerFactory()方法: 

有一个参数: 该参数表示PersistenceUnit的名字,然后使用persistence.xml中的属性创建一个EntityManagerFactory。

有两个参数: 第一个参数的作用同上,第二个参数可以让开发者设置额外的一些属性,可以作为persistence.xml中属性的扩充,如果属性的键与persistence.xml中相同,则代码中的设置覆盖persistence.xml中的配置值。

就 持久化上下文而言,应用程序管理的EntityManager就像扩展的容器管理的EntityManager。当创建应用程序管理的 EntityManager实例之后,该EntityManager实例立即创建一个属于它自己私有的持久化上下文,该持久化上下文将一直存活下去,直到 所属的EntityManager实例销毁才消失。

4. 容器管理的事务 之 容器管理的持久化上下文


JPA支持两种事务类型: 

本地资源事务 (RESOURCE_LOCAL) : 使用JDBC驱动管理的本地事务。

Java事务API (JTA) : 可用于管理分布式事务,管理多数据源的情况。

容器管理的EntityManager总是使用JTA事务。应用程序管理的EntityManager可以使用本地资源事务,也可以使用JTA事务。

在JavaSE环境下,默认的事务类型是RESOURCE_LOCAL,而在JavaEE环境下,默认的事务类型是JTA。

事务类型在persistence.xml中定义。

只能有一个持久化上下文与JTA关联,并且只能有一个持久化上下文在事务中传播。

对于容器管理的EntityManager,在同一事务中必须使用相同的持久化上下文。

事 务范围内的持久化上下文: 事务范围内的持久化上下文将其生命周期绑定到某个事务,在需要的时候,事务范围内的持久化上下文由事务范围内的 EntityManager负责创建,之所以说"在需要的时候",是因为事务范围内的持久化上下文是"懒加载"的,只有在EntityManager实例 调用相关的数据访问方法并且当前不存在可用的持久化上下文的时候,才会创建持久化上下文。

扩展的持久化上下文: 扩展的持久化上下文与有状态会 话Bean绑定。不同于事务范围内的持久化上下文为每一个事务创建一个新的持久化上下文,有状态会话Bean中扩展的EntityManager总是使用 相同的持久化上下文。有状态会话Bean总是只和一个持久化上下文绑定,并且在有状态会话Bean创建时创建该持久化上下文,在有状态会话Bean销毁时 注销该持久化上下文。也就是说,不同于事务范围内的持久化上下文,扩展的持久化上下文不是"懒加载"的。

持久化上下文的冲突: 当调用某个方法 时有若干个持久化上下文,则会出现持久化上下文冲突,抛出异常。有个特殊情况,即在一个有状态会话Bean的扩展持久化上下文中调用另一个有状态会话 Bean的方法,并且被调用的会话Bean也使用扩展持久化上下文,这样当调用被调用的会话Bean中方法时虽有两个持久化上下文可用,但并不会出现冲 突。被调用的会话Bean继承调用者的持久化上下文。

3. 容器管理的事务 之 应用程序管理的持久化上下文


应用程序管理的持久化上下文与容器管理的持久化上下文的一个最大的区别是: 只能有一个容器管理的持久化上下文与事务关联,但是可以有任意多个应用程序管理的持久化上下文与当前事务关联。


应用程序管理的持久化上下文有两种方式加入JTA 事务: 

如果持久化上下文是在事务内部创建的,则持久化提供者自动将该持久化上下文关联到当前事务；

如果持久化上下文不是在本事务内部创建的 (比如在另一个已经结束的事务中创建的) ,则需要调用EntityManager.joinTransaction() 方法手动将持久化上下文与事务绑定。

由于应用程序管理的EntityManager 不会自动传播,唯一与其他组件共享受管实例的方法是共享EntityManager 实例。并且在不同的事务当中使用EntityManager 时必须先要调用joinTransaction() 方法。

对于应用程序管理的EntityManager 而言,可以在事务结束前关闭EntityManager ,这样EntityManager 实例就无法使用了,但是之前做的操作在事务结束时仍然会同步到数据库。因为持久化上下文会存活到事务结束。

由于在同一个JTA 事务当中可以存在多个持久化上下文,所以当事务提交时,可能若干持久化上下文同时执行flush 操作,这样会存在隐性问题,比如,如果一个实例存在于多个持久化上下文中,flush 的结果会如何？结果是无法预料的。因此应该避免在同一事务中将一个实例加入多个持久化上下文。


4. 本地资源事务 (RESOURCE_LOCAL Transaction ) 


本地资源事务是指通过调用EntityManager.getTransaction() 管理的事务。其实质是使用Connection 来管理事务。


5. 其他


当事务回滚时,持久化上下文会将所有托管对象清空,亦即调用EntityManager.clear() 方法。如果持久化上下文是事务范围的,那么该持久化上下文将被销毁。