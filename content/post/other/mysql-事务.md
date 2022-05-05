---
title: DB 事务
author: "-"
date: 2014-05-21T03:09:21+00:00
url: /?p=6645
categories:
  - Uncategorized
tags:
  - Database

---
## DB 事务

  
    事务(Transaction):
  
  
    是并发控制的单元，是用户定义的一个操作序列。这些操作要么都做，要么都不做，是一个不可分割的工作单位。通过事务，sql server 能将逻辑相关的一组操作绑定在一起，以便服务器 保持数据的完整性。事务通常是以begin transaction开始，以commit或rollback结束。Commint表示提交，即提交事务的所有操作。具体地说就是将事务中所有对数据的更新写回到磁盘上的物理数据库中去，事务正常结束。Rollback表示回滚，即在事务运行的过程中发生了某种故障，事务不能继续进行，系统将事务中对数据库的所有已完成的操作全部撤消，滚回到事务开始的状态。
  
  
  
  
    1、事务的特性  (ACID): 
  
  
    原一隔持
  
  
    1) 原子性 (Atomic) : 即事务是不可分割的最小工作单元，事务内的操作，要么全部执行，要么全部不执行。
  
  
    2) 一致性 (Consistency) : 事务在完成时，必须是所有的数据都保持一致状态。
  
  
    在事务执行前数据库的数据处于正确的状态，而事务执行完成后数据库的数据还是处于正确的状态，即数据完整性约束没有被破坏；如银行转帐，A转帐给B，必须保证A的钱一定转给B，一定不会出现A的钱转了但B没收到，否则数据库的数据就处于不一致 (不正确) 的状态。
  
  
    3) 隔离性 (Isolation) : 一个事务的执行不能被其他事务所影响。
  
  
    并发事务执行之间无影响，在一个事务内部的操作对其他事务是不产生影响，这需要事务隔离级别来指定隔离性；
  
  
    事务必须是互相隔离的，防止并发读写同一个数据的情况发生 。
  
  
    4) 持久性 (Durable) : 一个事务一旦提交，事物的操作便永久性的保存在DB中。即使此时再执行回滚操作也不能撤消所做的更改。
  
  
  
  
    事务类型
  
  
    数据库事务类型有本地事务和分布式事务: 
  
  
    
      本地事务: 就是普通事务，能保证单台数据库上的操作的ACID，被限定在一台数据库上；
    
    
      分布式事务: 涉及两个或多个数据库源的事务，即跨越多台同类或异类数据库的事务 (由每台数据库的本地事务组成的) ，分布式事务旨在保证这些本地事务的所有操作的ACID，使事务可以跨越多台数据库；
    
  
  
    Java事务类型有JDBC事务和JTA事务: 
  
  
    
      JDBC事务: 就是数据库事务类型中的本地事务，通过Connection对象的控制来管理事务；
    
    
      JTA事务: JTA指Java事务API(Java Transaction API)，是Java EE数据库事务规范， JTA只提供了事务管理接口，由应用程序服务器厂商 (如WebSphere Application Server) 提供实现，JTA事务比JDBC更强大，支持分布式事务。
    
  
  
    Java EE事务类型有本地事务和全局事务: 
  
  
    
      本地事务: 使用JDBC编程实现事务；
    
    
      全局事务: 由应用程序服务器提供，使用JTA事务；
    
  
  
    按是否通过编程实现事务有声明式事务和编程式事务；
  
  
    
      声明式事务:  通过注解或XML配置文件指定事务信息；
    
    
      编程式事务: 通过编写代码实现事务。
    
  
  
  


  
    
      
    
    
    
      隐式事务: 当连接以隐式事务模式进行操作时，sql server数据库引擎实例将在提交或回滚当前事务后自动启动新事务。无须描述事物的开始，只需提交或回滚每个事务。但每个事务仍以commit或rollback显式结束。连接将隐性事务模式设置为打开之后，当数据库引擎实例首次执行下列任何语句时，都会自动启动一个隐式事务: alter table，insert，create，open ，delete，revoke ，drop，select， fetch ，truncate table，grant，update在发出commit或rollback语句之前，该事务将一直保持有效。在第一个事务被提交或回滚之后，下次当连接执行以上任何语句时，数据库引擎实例都将自动启动一个新事务。该实例将不断地生成隐性事务链，直到隐性事务模式关闭为止。
    
    
    
      
    
    
    
       Java事务的类型
    
    
    
      Java事务的类型有三种: JDBC事务、JTA (Java Transaction API) 事务、容器事务。
    
    
    
      1、JDBC事务
    
    
    
      JDBC 事务是用 Connection 对象控制的。JDBC Connection 接口 ( java.sql.Connection ) 提供了两种事务模式: 自动提交和手工提交。 java.sql.Connection 提供了以下控制事务的方法: 
    
    
    
      public void setAutoCommit(boolean)
 public boolean getAutoCommit()
 public void commit()
 public void rollback()
 使用 JDBC 事务界定时，您可以将多个 SQL 语句结合到一个事务中。JDBC 事务的一个缺点是事务的范围局限于一个数据库连接。一个 JDBC 事务不能跨越多个数据库。
    
    
    
      
    
    
    
      2、JTA (Java Transaction API) 事务
    
    
    
      JTA是一种高层的，与实现无关的，与协议无关的API，应用程序和应用服务器可以使用JTA来访问事务。
    
    
    
      JTA允许应用程序执行分布式事务处理——在两个或多个网络计算机资源上访问并且更新数据，这些数据可以分布在多个数据库上。JDBC驱动程序的JTA支持极大地增强了数据访问能力。
    
    
    
      如果计划用 JTA 界定事务，那么就需要有一个实现 javax.sql.XADataSource 、 javax.sql.XAConnection 和 javax.sql.XAResource 接口的 JDBC 驱动程序。一个实现了这些接口的驱动程序将可以参与 JTA 事务。一个 XADataSource 对象就是一个 XAConnection 对象的工厂。 XAConnection s 是参与 JTA 事务的 JDBC 连接。
    
    
    
      您将需要用应用服务器的管理工具设置 XADataSource .从应用服务器和 JDBC 驱动程序的文档中可以了解到相关的指导。
    
    
    
      J2EE应用程序用 JNDI 查询数据源。一旦应用程序找到了数据源对象，它就调用 javax.sql.DataSource.getConnection ()  以获得到数据库的连接。
    
    
    
      XA 连接与非 XA 连接不同。一定要记住 XA 连接参与了 JTA 事务。这意味着 XA 连接不支持 JDBC 的自动提交功能。同时，应用程序一定不要对 XA 连接调用 java.sql.Connection.commit ()  或者 java.sql.Connection.rollback ()  .
    
    
    
      相反，应用程序应该使用 UserTransaction.begin () 、 UserTransaction.commit ()  和 serTransaction.rollback ()  .
    
    
    
      
    
    
    
      3、容器事务
    
    
    
      容器事务主要是J2EE应用服务器提供的，容器事务大多是基于JTA完成，这是一个基于JNDI的，相当复杂的API实现。相对编码实现JTA事务管理， 我们可以通过EJB容器提供的容器事务管理机制 (CMT) 完成同一个功能，这项功能由J2EE应用服务器提供。这使得我们可以简单的指定将哪个方法加入事 务，一旦指定，容器将负责事务管理任务。这是我们土建的解决方式，因为通过这种方式我们可以将事务代码排除在逻辑编码之外，同时将所有困难交给J2EE容 器去解决。使用EJB CMT的另外一个好处就是程序员无需关心JTA API的编码，不过，理论上我们必须使用EJB.
    
    
    
      四、三种Java事务差异
    
    
    
      1、JDBC事务控制的局限性在一个数据库连接内，但是其使用简单。
    
    
    
      2、JTA事务的功能强大，事务可以跨越多个数据库或多个DAO，使用也比较复杂。
    
    
    
      3、容器事务，主要指的是J2EE应用服务器提供的事务管理，局限于EJB应用使用。
    
    
    
      五、总结
    
    
    
      Java事务控制是构建J2EE应用不可缺少的一部分，合理选择应用何种事务对整个应用系统来说至关重要。一般说来，在单个JDBC 连接连接的情况下可以选择JDBC事务，在跨多个连接或者数据库情况下，需要选择使用JTA事务，如果用到了EJB，则可以考虑使用EJB容器事务
    
    
    
      
    
    
    
      Java JDBC事务机制
    
    
    
      
    
    
    
      首先，我们来看看现有JDBC操作会给我们打来什么重大问题，比如有一个业务: 当我们修改一个信息后再去查询这个信息，看是这是一个简单的业务，实现起来也非常容易，但当这个业务放在多线程高并发的平台下，问题自然就出现了，比如当我们执行了一个修改后，在执行查询之前有一个线程也执行了修改语句，这是我们再执行查询，看到的信息就有可能与我们修改的不同，为了解决这一问题，我们必须引入JDBC事务机制，其实代码实现上很简单，一下给出一个原理实现例子供大家参考: 
    
    
    
      private Connection conn = null;
    
    
    
      private PreparedStatement ps = null;
    
    
    
      try {
    
    
    
      
    
    
    
      conn.setAutoCommit(false);  //将自动提交设置为false
    
    
    
      ps.executeUpdate("修改SQL"); //执行修改操作
    
    
    
      ps.executeQuery("查询SQL");  //执行查询操作
    
    
    
      conn.commit();      //当两个操作成功后手动提交
    
    
    
      } catch (Exception e) {
    
    
    
      conn.rollback();    //一旦其中一个操作出错都将回滚，使两个操作都不成功
    
    
    
      e.printStackTrace();
    
    
    
      }
    
    
    
      
    
    
    
      JDBC对事务的支持体现在三个方面: 
    
    
    
      
    
    
    
      1.自动提交模式(Auto-commit mode)
    
    
    
      Connection提供了一个auto-commit的属性来指定事务何时结束。
    
    
    
      a.当auto-commit为true时，当每个独立SQL操作的执行完毕，事务立即自动提交，也就是说每个SQL操作都是一个事务。
    
    
    
      一个独立SQL操作什么时候算执行完毕，JDBC规范是这样规定的: 
    
    
    
      对数据操作语言(DML，如insert,update,delete)和数据定义语言(如create,drop)，语句一执行完就视为执行完毕。
    
    
    
      对select语句，当与它关联的ResultSet对象关闭时，视为执行完毕。
    
    
    
      对存储过程或其他返回多个结果的语句，当与它关联的所有ResultSet对象全部关闭，所有update count(update,delete等语句操作影响的行数)和output parameter(存储过程的输出参数)都已经获取之后，视为执行完毕。
    
    
    
      b. 当auto-commit为false时，每个事务都必须显示调用commit方法进行提交，或者显示调用rollback方法进行回滚。auto-commit默认为true。
    
    
    
      JDBC提供了5种不同的事务隔离级别，在Connection中进行了定义。
    
    
    
      
    
    
    
      
    
    
    
      
    
    
    
      
        当创建Connection对象时，其事务隔离级别取决于驱动程序，但通常是所涉及的数据库的缺省值。用户可通过调用setIsolationLevel方法来更改事务隔离级别。新的级别将在该连接过程的剩余时间内生效。要想只改变一个事务的事务隔离级别，必须在该事务开始前进行设置，并在该事务结束后进行复位。我们不提倡在事务的中途对事务隔离级别进行更改，因为这将立即触发commit方法的调用，使在此之前所作的任何更改变成永久性的。
      
      
      
        JDBC的数据隔离级别设置: 
      
      
      
        <img class="magplus" title="点击查看原始大小图片" src="http://dl.iteye.com/upload/attachment/0064/4669/2e643cb3-3ecc-3cda-ba88-d90d12e7e8c2.jpg" alt="" width="700" height="329" />
      
      
      
                 为了解决与"多个线程请求相同数据"相关的问题，事务之间用锁相互隔开。多数主流的数据库支持不同类型的锁；因此，JDBC API 支持不同类型的事务，它们由 Connection 对象指派或确定。
      
      
      
        
          
                    为了在性能与一致性之间寻求平衡才出现了上面的几种级别。事务保护的级别越高，性能损失就越大。
          
          
          
                    假定您的数据库和 JDBC 驱动程序支持这个特性，则给定一个 Connection 对象，您可以明确地设置想要的事务级别: 
          
          
          
                    conn.setTransactionLevel(TRANSACTION_SERIALIZABLE) ;
          
          
          
                    可以通过下面的方法确定当前事务的级别: 
 int level = conn.getTransactionIsolation();
          
        
      
    
    
    
      
    
    
    
      3.保存点(SavePoint)
    
    
    
      JDBC定义了SavePoint接口，提供在一个更细粒度的事务控制机制。当设置了一个保存点后，可以rollback到该保存点处的状态，而不是rollback整个事务。Connection接口的setSavepoint和releaseSavepoint方法可以设置和释放保存点。
    
    
    
      
    
    
    
      JDBC规范虽然定义了事务的以上支持行为，但是各个JDBC驱动，数据库厂商对事务的支持程度可能各不相同。如果在程序中任意设置，可能得不到想要的效果。为此，JDBC提供了DatabaseMetaData接口，提供了一系列JDBC特性支持情况的获取方法。比如，通过DatabaseMetaData.supportsTransactionIsolationLevel方法可以判断对事务隔离级别的支持情况，通过DatabaseMetaData.supportsSavepoints方法可以判断对保存点的支持情况。
    
    
    
      来源: http://blog.csdn.net/yuejingjiahong/article/details/6663577
    
    
    
      http://blog.csdn.net/applehoney/article/details/2270732
    
    
    
      
    
    
    
      JDBC连接数据库步骤: 
    
    
    
      http://wenku.baidu.com/view/cb66dffc910ef12d2af9e7e2.html
    
    
    
      接口 ResultSet: 
    
    
    
      http://www.cjsdn.net/doc/jdk50/java/sql/ResultSet.html (插入、更新、删除RS和数据库中的行) 
  

MySQL 事务

ACID:Atomic、Consistent、Isolated、Durable
  
存储程序提供了一个绝佳的机制来定义、封装和管理事务。

1，MySQL的事务支持
  
MySQL的事务支持不是绑定在MySQL服务器本身，而是与存储引擎相关: 
  
Java代码 收藏代码
  
MyISAM: 不支持事务，用于只读程序提高性能
  
InnoDB: 支持ACID事务、行级锁、并发
  
Berkeley DB: 支持事务
  
隔离级别: 
  
隔离级别决定了一个session中的事务可能对另一个session的影响、并发session对数据库的操作、一个session中所见数据的一致性
  
ANSI标准定义了4个隔离级别，MySQL的InnoDB都支持: 
  
Java代码 收藏代码
  
READ UNCOMMITTED: 最低级别的隔离，通常又称为dirty read，它允许一个事务读取还没commit的数据，这样可能会提高性能，但是dirty read可能不是我们想要的
  
READ COMMITTED: 在一个事务中只允许已经commit的记录可见，如果session中select还在查询中，另一session此时insert一条记录，则新添加的数据不可见
  
REPEATABLE READ: 在一个事务开始后，其他session对数据库的修改在本事务中不可见，直到本事务commit或rollback。在一个事务中重复select的结果一样，除非本事务中update数据库。
  
SERIALIZABLE: 最高级别的隔离，只允许事务串行执行。为了达到此目的，数据库会锁住每行已经读取的记录，其他session不能修改数据直到前一事务结束，事务commit或取消时才释放锁。
  
可以使用如下语句设置MySQL的session隔离级别: 
  
Java代码 收藏代码
  
SET TRANSACTION ISOLATION LEVEL {READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE}
  
MySQL默认的隔离级别是REPEATABLE READ，在设置隔离级别为READ UNCOMMITTED或SERIALIZABLE时要小心，READ UNCOMMITTED会导致数据完整性的严重问题，而SERIALIZABLE会导致性能问题并增加死锁的机率

事务管理语句: 
  
Java代码 收藏代码
  
START TRANSACTION: 开始事务，autocommit设为0，如果已经有一个事务在运行，则会触发一个隐藏的COMMIT
  
COMMIT: 提交事务，保存更改，释放锁
  
ROLLBACK: 回滚本事务对数据库的所有更改，然后结束事务，释放锁
  
SAVEPOINT savepoint_name: 创建一个savepoint识别符来ROLLBACK TO SAVEPOINT
  
ROLLBACK TO SAVEPOINT savepoint_name: 回滚到从savepoint_name开始对数据库的所有更改，这样就允许回滚事务中的一部分，保证更改的一个子集被提交
  
SET TRANSACTION: 允许设置事务的隔离级别
  
LOCK TABLES: 允许显式的锁住一个或多个table，会隐式的关闭当前打开的事务，建议在执行LOCK TABLES语句之前显式的commit或rollback。我们一般所以一般在事务代码里不会使用LOCK TABLES
  
2，定义事务
  
MySQL默认的行为是在每条SQL语句执行后执行一个COMMIT语句，从而有效的将每条语句独立为一个事务。
  
在复杂的应用场景下这种方式就不能满足需求了。
  
为了打开事务，允许在COMMIT和ROLLBACK之前多条语句被执行，我们需要做以下两步: 
  
1, 设置MySQL的autocommit属性为0，默认为1
  
2，使用START TRANSACTION语句显式的打开一个事务

如果已经打开一个事务，则SET autocommit=0不会起作用，因为START TRANSACTION会隐式的提交session中所有当前的更改，结束已有的事务，并打开一个新的事务。

使用SET AUTOCOMMIT语句的存储过程例子: 
  
Java代码 收藏代码
  
CREATE PROCEDURE tfer_funds
  
(from_account int, to_account int, tfer_amount numeric(10,2))
  
BEGIN
  
SET autocommit=0;

UPDATE account_balance SET balance=balance-tfer_amount WHERE account_id=from_account;

UPDATE account_balance SET balance=balance+tfer_amount WHERE account_id=to_account;

COMMIT;
  
END;

使用START TRANSACITON打开事务的例子: 
  
Java代码 收藏代码
  
CREATE PROCEDURE tfer_funds
  
(from_account int, to_account int, tfer_amount numeric(10,2))
  
BEGIN
  
START TRANSACTION;

UPDATE account_balance SET balance=balance-tfer_amount WHERE account_id=from_account;

UPDATE account_balance SET balance=balance+tfer_amount WHERE account_id=to_account;

COMMIT;
  
END;
  
通常COMMIT或ROLLBACK语句执行时才完成一个事务，但是有些DDL语句等会隐式触发COMMIT，所以应该在事务中尽可能少用或注意一下: 
  
Java代码 收藏代码
  
ALTER FUNCTION
  
ALTER PROCEDURE
  
ALTER TABLE
  
BEGIN
  
CREATE DATABASE
  
CREATE FUNCTION
  
CREATE INDEX
  
CREATE PROCEDURE
  
CREATE TABLE
  
DROP DATABASE
  
DROP FUNCTION
  
DROP INDEX
  
DROP PROCEDURE
  
DROP TABLE
  
UNLOCK TABLES
  
LOAD MASTER DATA
  
LOCK TABLES
  
RENAME TABLE
  
TRUNCATE TABLE
  
SET AUTOCOMMIT=1
  
START TRANSACTION
  
3，使用Savepoint
  
使用savepoint回滚难免有些性能消耗，一般可以用IF改写
  
savepoint的良好使用的场景之一是"嵌套事务"，你可能希望程序执行一个小的事务，但是不希望回滚外面更大的事务: 
  
Java代码 收藏代码
  
CREATE PROCEDURE nested_tfer_funds
  
(in_from_acct INTEGER,
  
in_to_acct INTEGER,
  
in_tfer_amount DECIMAL(8,2))
  
BEGIN
  
DECLARE txn_error INTEGER DEFAULT 0;

DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN
  
SET txn_error=1;
  
END

SAVEPINT savepint_tfer;

UPDATE account_balance
  
SET balance=balance-in_tfer_amount
  
WHERE account_id=in_from_acct;

IF txn_error THEN
  
ROLLBACK TO savepoint_tfer;
  
SELECT 'Transfer aborted';
  
ELSE
  
UPDATE account_balance
  
SET balance=balance+in_tfer_amount
  
WHERE account_id=in_to_acct;

IF txn_error THEN
  
ROLLBACK TO savepoint_tfer;
  
SELECT 'Transfer aborted';

END IF:
  
END IF;
  
END;
  
4，事务和锁
  
事务的ACID属性只能通过限制数据库的同步更改来实现，从而通过对修改数据加锁来实现。
  
直到事务触发COMMIT或ROLLBACK语句时锁才释放。
  
缺点是后面的事务必须等前面的事务完成才能开始执行，吞吐量随着等待锁释放的时间增长而递减。
  
MySQL/InnoDB通过行级锁来最小化锁竞争。这样修改同一table里其他行的数据没有限制，而且读数据可以始终没有等待。
  
可以在SELECT语句里使用FOR UPDATE或LOCK IN SHARE MODE语句来加上行级锁
  
Java代码 收藏代码
  
SELECT select_statement options [FOR UPDATE|LOCK IN SHARE MODE]

FOR UPDATE会锁住该SELECT语句返回的行，其他SELECT和DML语句必须等待该SELECT语句所在的事务完成
  
LOCK IN SHARE MODE同FOR UPDATE，但是允许其他session的SELECT语句执行并允许获取SHARE MODE锁

死锁: 
  
死锁发生于两个事务相互等待彼此释放锁的情景
  
当MySQL/InnoDB检查到死锁时，它会强制一个事务rollback并触发一条错误消息
  
对InnoDB而言，所选择的rollback的事务是完成工作最少的事务 (所修改的行最少) 
  
Java代码 收藏代码
  
MySQL > CALL tfer_funds(1,2,300);
  
ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction

死锁在任何数据库系统里都可能发生，但是对MySQL/InnoDB这种行级锁数据库而言可能性相对较少。
  
可以通过使用一致的顺序来锁row或table以及让事务保持尽可能短来减少死锁的频率。
  
如果死锁不容易debug，你可以向你的程序中添加一些逻辑来处理死锁并重试事务，但这部分代码多了以后很难维护
  
所以，比较好的避免死锁的方式是在做任何修改之前按一定的顺序添加行级锁，这样就能避免死锁:
  
Java代码 收藏代码
  
CREATE PROCEDURE tfer_funds3
  
(from_account INT, to_account INT, tfer_amount NUMERIC(10,2))
  
BEGIN
  
DECLARE local_account_id INT;
  
DECLARE lock_cursor CURSOR FOR
  
SELECT account_id
  
FROM account_balance
  
WHERE account_id IN (from_account, to_account)
  
ORDER BY account_id
  
FOR UPDATE;

START TRANSACTION;

OPEN lock_cursor;
  
FETCH lock_cursor INTO local_account_id;

UPDATE account_balance
  
SET balance=balance-tfer_amount
  
WHERE account_id=from_account;

UPDATE account_balance
  
SET balance=balance+tfer_amount
  
WHERE account_id=to_account;

CLOSE lock_cursor;

COMMIT;
  
END;
  
设置死锁ttl: innodb_lock_wait_timeout，默认为50秒
  
如果你在一个事务中混合使用InnoDB和非InnoDB表，则MySQL不能检测到死锁，此时会抛出"lock wait timeuot"1205错误

乐观所和悲观锁策略: 
  
悲观锁: 在读取数据时锁住那几行，其他对这几行的更新需要等到悲观锁结束时才能继续
  
乐观所: 读取数据时不锁，更新时检查是否数据已经被更新过，如果是则取消当前更新
  
一般在悲观锁的等待时间过长而不能接受时我们才会选择乐观锁
  
悲观锁的例子: 
  
Java代码 收藏代码
  
CREATE PROCEDURE tfer_funds
  
(from_account INT, to_account INT,tfer_amount NUMERIC(10,2),
  
OUT status INT, OUT message VARCHAR(30))
  
BEGIN
  
DECLARE from_account_balance NUMERIC(10,2);

START TRANSACTION;

SELECT balance
  
INTO from_account_balance
  
FROM account_balance
  
WHERE account_id=from_account
  
FOR UPDATE;

IF from_account_balance>=tfer_amount THEN

UPDATE account_balance
  
SET balance=balance-tfer_amount
  
WHERE account_id=from_account;

UPDATE account_balance
  
SET balance=balance+tfer_amount
  
WHERE account_id=to_account;
  
COMMIT;

SET status=0;
  
SET message='OK';
  
ELSE
  
ROLLBACK;
  
SET status=-1;
  
SET message='Insufficient funds';
  
END IF;
  
END;

乐观锁的例子: 
  
Java代码 收藏代码
  
CREATE PROCEDURE tfer_funds
  
(from_account INT, to_account INT, tfer_amount NUMERIC(10,2),
  
OUT status INT, OUT message VARCHAR(30) )

BEGIN

DECLARE from_account_balance NUMERIC(8,2);
  
DECLARE from_account_balance2 NUMERIC(8,2);
  
DECLARE from_account_timestamp1 TIMESTAMP;
  
DECLARE from_account_timestamp2 TIMESTAMP;

SELECT account_timestamp,balance
  
INTO from_account_timestamp1,from_account_balance
  
FROM account_balance
  
WHERE account_id=from_account;

IF (from_account_balance>=tfer_amount) THEN

- Here we perform some long running validation that
  
- might take a few minutes */
  
CALL long_running_validation(from_account);

START TRANSACTION;

- Make sure the account row has not been updated since
  
- our initial check
  
SELECT account_timestamp, balance
  
INTO from_account_timestamp2,from_account_balance2
  
FROM account_balance
  
WHERE account_id=from_account
  
FOR UPDATE;

IF (from_account_timestamp1 <> from_account_timestamp2 OR
  
from_account_balance <> from_account_balance2) THEN
  
ROLLBACK;
  
SET status=-1;
  
SET message=CONCAT("Transaction cancelled due to concurrent update",
  
" of account" ,from_account);
  
ELSE
  
UPDATE account_balance
  
SET balance=balance-tfer_amount
  
WHERE account_id=from_account;

UPDATE account_balance
  
SET balance=balance+tfer_amount
  
WHERE account_id=to_account;

COMMIT;

SET status=0;
  
SET message="OK";
  
END IF;

ELSE
  
ROLLBACK;
  
SET status=-1;
  
SET message="Insufficient funds";
  
END IF;
  
END$$
  
5，事务设计指南
  
Java代码 收藏代码
  
1，保持事务短小
  
2，尽量避免事务中rollback
  
3，尽量避免savepoint
  
4，默认情况下，依赖于悲观锁
  
5，为吞吐量要求苛刻的事务考虑乐观锁
  
6，显示声明打开事务
  
7，锁的行越少越好，锁的时间越短越好


http://www.infoq.com/cn/articles/Isolation-Levels?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global