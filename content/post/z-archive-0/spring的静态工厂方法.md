---
title: Spring的静态工厂方法
author: "-"
date: 2012-03-26T04:35:02+00:00
url: /?p=2629
categories:
  - Development
tags:
  - Java

---
## Spring的静态工厂方法
http://blog.csdn.net/chensugang/article/details/3357593
  
上一次写了一篇关于DI的三种方式，其中里面介绍了构造方法的方式，今天学习了一种替代构造器的方法，这就是静态工厂方法来返回对象，下面来看一下静态工厂方法的实现。

静态工厂方法: 
  
LoginAction类: 
  
package com.spring.test.di;

public class LoginAction {
      
private Logic logic;

private LoginAction(Logic logic){
         
this.logic = logic;
      
}
      
public static LoginAction createInstance(Logic logic){
         
LoginAction loginAction = new LoginAction (logic);
         
return loginAction;
      
}

public void execute() {
         
String name = logic.getName();
         
System.out.print("My Name Is " + name);
      
}
  
}

注意: 这里使用的构造方法是一个私有方法，createInstance这个就是我们的静态工厂方法
  
Logic接口: 
  
package com.spring.test.di;

public interface Logic {
      
public String getName();
  
}
  
这里只是做为一个简单的例子，所以我们在该接口中只有一个方法，并且在该接口的实现方法也超级简单
  
Logic接口实现: 
  
package com.spring.test.di;

public class LogicImpl implements Logic{

public String getName(){
         
return "fengyun";
      
}
  
}
  
下面我们来看一下配置文件，配置文件基本跟使用构造方法的配置差不多，不过多了一个factory-method方法，如下所示: 
  
<bean id="logic" class="com.spring.test.di.LogicImpl"/>
  
<bean id="loginAction" class="com.spring.test.di.LoginAction" factory-method="createInstance">
    
<constructor-arg ref="logic"></constructor-arg>
  
</bean>

做一个测试类来测试一下是否注入成功: 
  
TestMain.java

package com.spring.test.di;

import org.springframework.context.ApplicationContext;
  
import org.springframework.context.support.FileSystemXmlApplicationContext;

public class TestMain {
      
/**
       
* @param args
       
*/
      
public static void main(String[] args) throws Exception {
         
// 得到ApplicationContext对象
         
ApplicationContext ctx = new FileSystemXmlApplicationContext(
                
"applicationContext.xml");
         
// 得到Bean
         
if (ctx.containsBean("loginAction")) {
             
LoginAction loginAction = (LoginAction) ctx.getBean("loginAction");
             
loginAction.execute();
         
}
      
}
  
}
  
运行成功将在控制台看到: My Name Is fengyun

在createInstance方法中传给他的参数又constructor-arg元素提供，这与使用构造函数来注入是完全一样的。而且最重要的一点是，使用工厂方法所返回的实例并不一定是包含工厂方法的类，也就是说他可以返回任何别的类的实例。