---
title: java spi, ServiceLoader
author: "-"
date: 2017-11-07T09:24:25+00:00
url: /?p=11372
categories:
  - Inbox
tags:
  - reprint
---
## java spi, ServiceLoader
ServiceLoader与ClassLoader是Java中2个即相互区别又相互联系的加载器.JVM利用ClassLoader将类载入内存,这是一个类声明周期的第一步 (一个java类的完整的生命周期会经历加载、连接、初始化、使用、和卸载五个阶段,当然也有在加载或者连接之后没有被初始化就直接被使用的情况) 。详情请参阅: 详解Java类的生命周期

那ServiceLoader又是什么呢？ServiceLoader: 一个简单的服务提供者加载设施。服务 是一个熟知的接口和类 (通常为抽象类) 集合。服务提供者 是服务的特定实现。提供者中的类通常实现接口,并子类化在服务本身中定义的子类。服务提供者可以以扩展的形式安装在 Java 平台的实现中,也就是将 jar 文件放入任意常用的扩展目录中。也可通过将提供者加入应用程序类路径,或者通过其他某些特定于平台的方式使其可用。……唯一强制要求的是,提供者类必须具有不带参数的构造方法,以便它们可以在加载中被实例化。

通过在资源目录META-INF/services中放置提供者配置文件 来标识服务提供者。文件名称是服务类型的完全限定二进制名称。该文件包含一个具体提供者类的完全限定二进制名称列表,每行一个。忽略各名称周围的空格、制表符和空行。注释字符为'#'('\u0023', NUMBER SIGN)；忽略每行第一个注释字符后面的所有字符。文件必须使用 UTF-8 编码。

以延迟方式查找和实例化提供者,也就是说根据需要进行。服务加载器维护到目前为止已经加载的提供者缓存。每次调用 iterator 方法返回一个迭代器,它首先按照实例化顺序生成缓存的所有元素,然后以延迟方式查找和实例化所有剩余的提供者,依次将每个提供者添加到缓存。可以通过 reload 方法清除缓存。

……

以上来源于Java API里的说明,也许说的很专业,让我们有点晕头转向,我们可以简单的认为: ServiceLoader也像ClassLoader一样,能装载类文件,但是使用时有区别,具体区别如下:  (1)  ServiceLoader装载的是一系列有某种共同特征的实现类,而ClassLoader是个万能加载器； (2) ServiceLoader装载时需要特殊的配置,使用时也与ClassLoader有所区别； (3) ServiceLoader还实现了Iterator接口。[如有错误或不到的地方敬请指出,互相学习: ) ]

SPI 和 ServiceLoader

1 SPI: Service Provider Interface

一个服务(Service)通常指的是已知的接口或者抽象类,服务提供方就是对这个接口或者抽象类的实现,然后按照SPI 标准存放到资源路径META-INF/services目录下,文件的命名为该服务接口的全限定名

许多开发框架都使用了Java的SPI机制,如java.sql.Driver的SPI实现 (MySQL驱动、oracle驱动等) 、common-logging的日志接口实现、dubbo的扩展实现等等。

我们系统里抽象的各个模块,往往有很多不同的实现方案,比如日志模块的方案,xml解析模块、jdbc模块的方案等。面向的对象的设计里,我们一般推荐模块之间基于接口编程,模块之间不对实现类进行硬编码。一旦代码里涉及具体的实现类,就违反了可拔插的原则,如果需要替换一种实现,就需要修改代码。

为了实现在模块装配的时候能不在程序里动态指明,这就需要一种服务发现机制。java spi就是提供这样的一个机制: 为某个接口寻找服务实现的机制。有点类似IOC的思想,就是将装配的控制权移到程序之外,在模块化设计中这个机制尤其重要。

java spi的具体约定如下: 当服务的提供者,提供了服务接口的一种实现之后,在jar包的META-INF/services/目录里同时创建一个以服务接口命名的文件。该文件里就是实现该服务接口的具体实现类。而当外部程序装配这个模块的时候,就能通过该jar包META-INF/services/里的配置文件找到具体的实现类名,并装载实例化,完成模块的注入

1.例子

第一步: 提供一个接口和它的若干个实现: 
  
有一个接口

package com.xihe.api;

public interface XiheInterface {
      
public void sayHi();
  
}
  
该接口有两个实现

package com.xihe.api;

public class XiheBJ implements XiheInterface {

    public void sayHi() {
         System.out.println("xihe in beijing "); 
    } 
    

}
  
public class XiheZZ implements XiheInterface {

    public void sayHi() {
        System.out.println("xihe in zhengzhou");
    }
    

}
  
第二步:  在src下创建META-INF/services/目录 (maven工程META-INF放在src/main/resources里)
  
目录中创建一个名为com.xihe.api.XiheInterface 的文件,文件的内容是实现类的全名。
  
如果该Service有多个服务实现,则每一行写一个服务实现,如: 

com.xihe.api.XiheZZ
  
com.xihe.api.XiheBJ
  
第三步: 加载

public class Demo {

    public static void main(String[] args) {
        ServiceLoader<XiheInterface> serviceLoader = ServiceLoader.load(XiheInterface.class);
        Iterator<XiheInterface> it = serviceLoader.iterator();
        while (it!=null && it.hasNext()) {
            XiheInterface demoService = it.next();
            System.out.println("class:"+demoService.getClass().getName());
            demoService.sayHi();
        }
    }
    

}
  
运行结果: 
  
class:com.xihe.api.XiheZZ
  
xihe in zhengzhou
  
class:com.xihe.api.XiheBJ
  
xihe in beijing

http://www.jianshu.com/p/32d3e108f30a
  
https://my.oschina.net/hanzhankang/blog/109794
  
http://mogu.io/serviceloader-106
  
http://shmilyaw-hotmail-com.iteye.com/blog/1926513
  
http://www.voidcn.com/blog/FX_SKY/article/p-6102785.html
  
https://yq.aliyun.com/articles/32452
  
http://blog.5ibc.net/p/40779.html