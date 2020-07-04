---
title: PropertyPlaceholderConfigurer
author: wiloon
type: post
date: 2012-12-08T11:42:57+00:00
url: /?p=4865
categories:
  - Java

---
<http://callan.iteye.com/blog/161540>

关于PropertyPlaceholderConfigurer与PropertyOverrideConfigurer

PropertyPlaceholderConfigurer，允许在spring的配置文件中加入properties文件，可以将一些动态参数移到properties中．

<div id="">
  
    [java]
 
 <bean id="propertyConfigurer"
 class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
 <property name="location" value="classpath:config/jdoserver.properties"/>
 </bean>
 [/java]
  

但是好像在属性文件定义中却不支持多个属性文件的定义，比如不能这样用config/*.properties。

经过查看源码，发现可以使用locations属性定义多个配置文件：

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol start="1">
    <li>
      <property name="locations">
    </li>
    <li>
                  <list>
    </li>
    <li>
                      <value>classpath:config/maxid.properties</value>
    </li>
    <li>
                      <value>classpath:config/jdoserver.properties</value>
    </li>
    <li>
                  </list>
    </li>
    <li>
      </property>
    </li>
  </ol>

使用外部属性后如下：

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol start="1">
    <li>
      <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    </li>
    <li>
              <property name="driverClassName" value="${jdbc.agent.driver}"/>
    </li>
    <li>
              <property name="url" value="${jdbc.agent.main.url}"/>
    </li>
    <li>
          </bean>
    </li>
  </ol>

PropertyOverrideConfigurer：在spring所有的bean初使化以后，将bean的值强行改变

<div id="">
  
    
      Xml代码  <a title="收藏这段代码"><img src="http://callan.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol start="1">
    <li>
      <bean id="configBean"
    </li>
    <li>
         class="org.springframework.beans.factory.config.PropertyOverrideConfigurer">
    </li>
    <li>
               <property name="location">
    </li>
    <li>
                   <value>hello.properties</value>
    </li>
    <li>
               </property>
    </li>
    <li>
           </bean>
    </li>
    <li>
    </li>
    <li>
           <bean id="helloBean" class="com.HelloBean">
    </li>
    <li>
               <property name="word">
    </li>
    <li>
                   <value>Hello!</value>
    </li>
    <li>
               </property>
    </li>
    <li>
           </bean>
    </li>
  </ol>

定义HelloBean,注入word的值为hello.

在hello.properties中

helloBean.word=Welcome!

word初使为hello后，当bean全加载完,PropertyOverrideConfigurer将helloBean.word的值改成为welcome.