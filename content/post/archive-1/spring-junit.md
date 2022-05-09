---
title: spring junit
author: "-"
date: 2014-02-24T07:49:28+00:00
url: /?p=6279
categories:
  - Inbox
tags:
  - Junit
  - Spring

---
## spring junit
**一.首先讲下注解,autowire 与 resource的区别**
  
@Autowired是按类型装配依赖对象，默认情况下，要求依赖对象必须存在，若允许null值，可以设置它的required属性为false。如果想使用按名称装配，可以结合@Qualifier注解一起使用。如: 
  
@Autowired @Qualifier("xmlBean1")
  
private XMLBean xmlBean;

@Resource和@Autowired一样，也可以标注在字段或属性的setter方法上，但它默认是按名称装配。名称可以通过@Resource的name属性指定，如果没有指定name属性，当注解标注在字段上，即默认取字段的名称作为bean名称寻找对象，当注解标注在属性的setter方法上，即默认取属性名作为bean名称寻找依赖对象。当没有使用name属性时，如果按照字段名找不到bean，就会转而使用按类型装配的方式进行查找；但当使用了name属性，只能按照指定的name查找bean，当找不到相应的bean时，就会抛异常。
  
@Resource(name="xmlBeanx")
  
private XMLBean xmlBean;//用于字段上

**二.讲解spring测试套件的好处:**
  
在开发基于Spring的应用时，如果你还直接使用Junit进行单元测试，那你就错过了Spring为我们所提供的饕餮大餐了。使用Junit直接进行单元测试有以下四大不足: 

1) 导致多次Spring容器初始化问题

根据JUnit测试方法的调用流程，每执行一个测试方法都会创建一个测试用例的实例并调用setUp()方法。由于一般情况下，我们在setUp()方法中初始化Spring容器，这意味着如果测试用例有多少个测试方法，Spring容器就会被重复初始化多次。虽然初始化Spring容器的速度并不会太慢，但由于可能会在Spring容器初始化时执行加载Hibernate映射文件等耗时的操作，如果每执行一个测试方法都必须重复初始化Spring容器，则对测试性能的影响是不容忽视的；

－－>使用Spring测试套件，Spring容器只会初始化一次！

2) 需要使用硬编码方式手工获取Bean

在测试用例类中我们需要通过ctx.getBean()方法从Spirng容器中获取需要测试的目标Bean，并且还要进行强制类型转换的造型操作。这种乏味的操作迷漫在测试用例的代码中，让人觉得烦琐不堪；

－－>使用Spring测试套件，测试用例类中的属性会被自动填充Spring容器的对应Bean
  
，无须在手工设置Bean！

3) 数据库现场容易遭受破坏

测试方法对数据库的更改操作会持久化到数据库中。虽然是针对开发数据库进行操作，但如果数据操作的影响是持久的，可能会影响到后面的测试行为。举个例子，用户在测试方法中插入一条ID为1的User记录，第一次运行不会有问题，第二次运行时，就会因为主键冲突而导致测试用例失败。所以应该既能够完成功能逻辑检查，又能够在测试完成后恢复现场，不会留下"后遗症"；

－－>使用Spring测试套件，Spring会在你验证后，自动回滚对数据库的操作，保证数据库的现场不被破坏，因此重复测试不会发生问题！

4) 不方便对数据操作正确性进行检查

假如我们向登录日志表插入了一条成功登录日志，可是我们却没有对t_login_log表中是否确实添加了一条记录进行检查。一般情况下，我们可能是打开数据库，肉眼观察是否插入了相应的记录，但这严重违背了自动测试的原则。试想在测试包括成千上万个数据操作行为的程序时，如何用肉眼进行检查？

－－>只要你继承Spring的测试套件的用例类，你就可以通过jdbcTemplate在同一事务中访问数据库，查询数据的变化，验证操作的正确性！

Spring提供了一套扩展于Junit测试用例的测试套件，使用这套测试套件完全解决了以上四个问题，让我们测试Spring的应用更加方便。现在我的项目中已经完成摒弃Junit，而采用Spring的测试套件，确实带来了很大的便利。严重推荐Springer使用这个测试套件。这个测试套件主要由org.springframework.test包下的若干类组成，使用简单快捷，方便上手。

**
  
最后讲spring 的 测试套件:**
  
1.显示基类,其实就是用来加载配置文件的

@RunWith(SpringJUnit4ClassRunner.class)

//使用junit4进行测试@ContextConfiguration({"/app\*.xml","/spring/app\*.xml","/spring/service/app*.xml"})

//加载配置文件

public class BaseJunit4Test {

}

接着是我们自己的测试类

public class UserAssignServiceTest extends BaseJunit4Test{


  
    
          @Resource  //自动注入,默认按名称
    
    
          private UserAssignService userAssignService;
    
    
    
    
          @Test   //标明是测试方法
    
    
          @Transactional   //标明此方法需使用事务
    
    
          @Rollback(false)  //标明使用完此方法后事务不回滚,true时为回滚
    
    
          public void testInsertUserAssign() {
    
    
              for(int i=0;i<10;i++){
    
    
                  UserAssign u=new UserAssign();
    
    
                  u.setAmount("7");
    
    
                  u.setCity(2);
    
    
                  u.setProvince(1);
    
    
                  u.setCompany("宜信");
    
    
                  u.setCreate_date(DateUtil.getCurrentTimeSecond());
    
    
                  u.setCreator(0);
    
    
                  u.setEmail("1133@163.com");
    
    
                  u.setOper_date(DateUtil.getCurrentTimeSecond());
    
    
                  u.setPosition("工人");
    
    
                  u.setOperator(0);
    
    
                  u.setQudao("2");
    
    
                  u.setUsername("张"+i);
    
    
                  userAssignService.insertUserAssign(u);
    
    
                  Assert.assertNotNull(u.getId());
    
    
              }
    
    
          }
    
    
    
    
      }
    
  
