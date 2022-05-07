---
title: Spring静态注入的三种方式
author: "-"
date: 2020-02-06T14:18:04+00:00
url: /?p=15495
categories:
  - Inbox
tags:
  - reprint
---
## Spring静态注入的三种方式
Spring静态注入的三种方式: 

(说明: MongoFileOperationUtil是自己封装的一个Mongodb文件读写工具类，里面需要依赖AdvancedDatastore对象实例，dsForRW用来获取Mongodb数据源)

在springframework里，我们不能@Autowired一个静态变量,使之成为一个spring bean，例如下面这种方式: 

@Autowired
  
private static AdvancedDatastore dsForRW;
  
可以试一下，dsForRW在这种状态下不能够被依赖注入，会抛出运行时异常java.lang.NullPointerException，为什么呢?静态变量/类变量不是对象的属性,而是一个类的属性,spring则是基于对象层面上的依赖注入。
  
但是自己比较喜欢封装工具类，并通过@Component注解成功能组件，但是功能组件中的方法一般都是静态方法，静态方法只能调用静态成员变量，于是就有了下面的问题。封有的时候封装功能组件会需要底层的service注入，怎么办呢？
  
去网上搜了下解决办法，简单总结一下几种实现方式；

1.xml方式实现；

<bean id="mongoFileOperationUtil" class="com.\*.\*.MongoFileOperationUtil" init-method="init"> <property name="dsForRW" ref="dsForRW"/> </bean>

public class MongoFileOperationUtil {

    private static AdvancedDatastore dsForRW;
    
    private static MongoFileOperationUtil mongoFileOperationUtil;
    
    public void init() {
        mongoFileOperationUtil = this;
        mongoFileOperationUtil.dsForRW = this.dsForRW;
    }
    

}
  
这种方式适合基于XML配置的WEB项目；

2.@PostConstruct方式实现；

import org.mongodb.morphia.AdvancedDatastore;
  
import org.springframework.beans.factory.annotation.Autowired;

@Component
  
public class MongoFileOperationUtil {
      
@Autowired
      
private static AdvancedDatastore dsForRW;

    private static MongoFileOperationUtil mongoFileOperationUtil;
    
    @PostConstruct
    public void init() {
        mongoFileOperationUtil = this;
        mongoFileOperationUtil.dsForRW = this.dsForRW;
    }
    

}
  
@PostConstruct 注解的方法在加载类的构造函数之后执行，也就是在加载了构造函数之后，执行init方法；(@PreDestroy 注解定义容器销毁之前的所做的操作)
  
这种方式和在xml中配置 init-method和 destory-method方法差不多，定义spring 容器在初始化bean 和容器销毁之前的所做的操作；

3.set方法上添加@Autowired注解，类定义上添加@Component注解；

import org.mongodb.morphia.AdvancedDatastore;
  
import org.springframework.beans.factory.annotation.Autowired;
  
import org.springframework.stereotype.Component;

@Component
  
public class MongoFileOperationUtil {

    private static AdvancedDatastore dsForRW;
    
    @Autowired
    public void setDatastore(AdvancedDatastore dsForRW) {
        MongoFileOperationUtil.dsForRW = dsForRW;
    }
    

}
  
首先Spring要能扫描到AdvancedDatastore的bean，然后通过setter方法注入；

然后注意: 成员变量上不需要再添加@Autowired注解；
  
————————————————
  
版权声明: 本文为CSDN博主「蓝色骨头_cqy」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/chen1403876161/article/details/53644024