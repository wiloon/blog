---
title: spring quartz
author: "-"
date: 2014-11-07T01:15:44+00:00
url: /?p=7002
categories:
  - Inbox
tags:
  - Java
  - Spring

---
## spring quartz
http://www.oschina.net/question/8676_9032

<bean class="org.springframework.scheduling.quartz.SchedulerFactoryBean">  
       <property name="triggers">  
             
              <ref bean="testTrigger"/>  
           </list>  
       </property>  
       <property name="autoStartup" value="true"/>  
</bean>

说明: Scheduler包含一个Trigger列表,每个Trigger表示一个作业。

**2、Trigger的配置**

<bean id="testTrigger" class="org.springframework.scheduling.quartz.CronTriggerBean">  
       <property name="jobDetail" ref="testJobDetail"/>  
       <property name="cronExpression" value="*/1 * * * * ?"/><!-- 每隔1秒钟触发一次 -->  
</bean>

说明: 

1) Cron表达式的格式: 秒 分 时 日 月 周 年(可选)。

字段名                 允许的值                        允许的特殊字符

秒                         0-59                               , - * /

分                         0-59                               , - * /

小时                   0-23                               , - * /

日                         1-31                               , - * ? / L W C

月                         1-12 or JAN-DEC          , - * /

周几                     1-7 or SUN-SAT            , - * ? / L C #

年 (可选字段)     empty, 1970-2099      , - * /

"?"字符: 表示不确定的值

","字符: 指定数个值

"-"字符: 指定一个值的范围

"/"字符: 指定一个值的增加幅度。n/m表示从n开始,每次增加m

"L"字符: 用在日表示一个月中的最后一天,用在周表示该月最后一个星期X

"W"字符: 指定离给定日期最近的工作日(周一到周五)

"#"字符: 表示该月第几个周X。6#3表示该月第3个周五

2) Cron表达式范例: 

每隔5秒执行一次: */5 \* \* \* * ?

每隔1分钟执行一次: 0 */1 \* \* \* ?

每天23点执行一次: 0 0 23 \* \* ?

每天凌晨1点执行一次: 0 0 1 \* \* ?

每月1号凌晨1点执行一次: 0 0 1 1 * ?

每月最后一天23点执行一次: 0 0 23 L * ?

每周星期天凌晨1点实行一次: 0 0 1 ? * L

在26分、29分、33分执行一次: 0 26,29,33 \* \* * ?

每天的0点、13点、18点、21点都执行一次: 0 0 0,13,18,21 \* \* ?

**3、JobDetail的配置**

<bean id="testJobDetail" class="org.springframework.scheduling.quartz.MethodInvokingJobDetailFactoryBean">   
        <property name="targetObject" ref="testJob"/>  
        <property name="targetMethod" value="execute"/>  
        <property name="concurrent" value="false"/>
        <!-- 是否允许任务并发执行。当值为false时,表示必须等到前一个线程处理完毕后才再启一个新的线程 -->  
</bean>

**4、业务类的配置**

<bean id="testJob" class="com.cjm.web.service.quartz.TestJob"/>

**5、业务类源代码**

public class TestJob {  
    public void execute(){  
        try{  
              //.......
         }catch(Exception ex){  
             ex.printStackTrace();  
         }  
     }  
}

说明: 业务类不需要继承任何父类,也不需要实现任何接口,只是一个普通的java类。

注意: 

在Spring配置和Quartz集成内容时,有两点需要注意

１、在<Beans>中不能够设置default-lazy-init="true",否则定时任务不触发,如果不明确指明default-lazy-init的值,默认是false。

２、在<Beans>中不能够设置default-autowire="byName"的属性,否则后台会报org.springframework.beans.factory.BeanCreationException错误,这样就不能通过Bean名称自动注入,必须通过明确引用注入

