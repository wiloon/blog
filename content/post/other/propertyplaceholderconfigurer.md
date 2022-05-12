---
title: PropertyPlaceholderConfigurer
author: "-"
date: 2012-12-08T11:42:57+00:00
url: /?p=4865
categories:
  - Java
tags:$
  - reprint
---
# PropertyPlaceholderConfigurer
<http://callan.iteye.com/blog/161540>

关于PropertyPlaceholderConfigurer与PropertyOverrideConfigurer

PropertyPlaceholderConfigurer,允许在spring的配置文件中加入properties文件,可以将一些动态参数移到properties中．

```xml
<bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
<property name="location" value="classpath:config/jdoserver.properties"/>
</bean>
```

但是好像在属性文件定义中却不支持多个属性文件的定义,比如不能这样用config/*.properties。

经过查看源码,发现可以使用locations属性定义多个配置文件: 

Java代码  <img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      <property name="locations">
    
    
                  
    
    
                      <value>classpath:config/maxid.properties</value>
    
    
                      <value>classpath:config/jdoserver.properties</value>
    
    
                  </list>
    
    
      </property>
    
  

使用外部属性后如下: 


  
    
      Java代码  <img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    
    
              <property name="driverClassName" value="${jdbc.agent.driver}"/>
    
    
              <property name="url" value="${jdbc.agent.main.url}"/>
    
    
          </bean>
    
  

PropertyOverrideConfigurer: 在spring所有的bean初使化以后,将bean的值强行改变


  
    
      Xml代码  <img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" />
  
  
  
    
      <bean id="configBean"
    
    
         class="org.springframework.beans.factory.config.PropertyOverrideConfigurer">
    
    
               <property name="location">
    
    
                   <value>hello.properties</value>
    
    
               </property>
    
    
           </bean>
    
    
    
    
           <bean id="helloBean" class="com.HelloBean">
    
    
               <property name="word">
    
    
                   <value>Hello!</value>
    
    
               </property>
    
    
           </bean>
    
  

定义HelloBean,注入word的值为hello.

在hello.properties中

helloBean.word=Welcome!

word初使为hello后,当bean全加载完,PropertyOverrideConfigurer将helloBean.word的值改成为welcome.