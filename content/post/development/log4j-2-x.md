---
title: Log4j 2.x
author: "-"
date: 2013-12-27T03:29:31+00:00
url: /?p=6079
categories:
  - Inbox
tags:
  - logging

---
## Log4j 2.x

## Log4j2.x

log4j-api:log4j2 定义的API
log4j-core:log4j2 上述API的实现

```xml
<properties>
    <log4j.version>2.17.2</log4j.version>
</properties>

<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-api</artifactId>
    <version>${log4j.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>${log4j.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-slf4j-impl</artifactId>
    <version>${log4j.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-jcl</artifactId>
    <version>${log4j.version}</version>
</dependency>
```

log4j2里面日志有8个等级，由低到高是:  

    all<trace<debug<info<warn<error<fatal<off

看下面的配置，这个配置会输出error及以上的日志级别，也就是onMatch匹配的是 大于等于 该等级的日志，输出的就是error,fatal

```xml
<ThresholdFilter level="error" onMatch="ACCEPT" onMismatch="DENY" />

```

然后是一个相反的配置，这个配置会输出error以下的日志级别，也就是onMismatch匹配的是 小于 该等级的日志，输出的就是warn,info,debug,trace

```xml
<ThresholdFilter level="error" onMatch="DENY" onMismatch="ACCEPT" />
```

```xml
<loggers>
         
             
             
         </AsyncLogger>
     </loggers>
```

loggers标签，用于定义logger的lever和所采用的appender，其中appender-ref必须为先前定义的 appenders的名称，例如，此处为Console。那么log就会以appender所定义的输出格式来输出log。

root标签为log的默认输出形式，如果一个类的log没有在loggers中明确指定其输出lever与格式，那么就会采用root中定义的格式。
  
private static Logger logger = LogManager.getLogger(Foo.class.getName());
  
gradle

compile 'org.apache.logging.log4j:log4j-api:2.0-beta9'
  
compile 'org.apache.logging.log4j:log4j-core:2.0-beta9'
  
The name of the configuration file should be log4j2.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
    <Properties>
        <Property name="log.path">/data/logs</Property>
        <Property name="log.level">debug</Property>
        <Property name="project.name">nettyx</Property>
    </Properties>
    
        <File name="File" fileName="foo.log" append="false">
            <PatternLayout pattern="%highlight{%d{ISO8601} %-5level [%t] %C{3} (%F:%L) - %m}%n"/>
        </File>
        <Console name="STDOUT" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{ABSOLUTE} %level{length=1} [%t] %C{2} (%F:%L) - %m%n"/>
        </Console>
    </Appenders>
    <Loggers>
        <Logger name="org.apache.log4j.xml" level="debug">
            
        </Logger>
        <Root level="debug">
            
            
        </Root>
    </Loggers>
</Configuration>
```

```java
    private final static Logger logger = LoggerFactory.getLogger(Class0.class);

```

### log4j2按日志级别输出到指定文件

[https://www.cnblogs.com/jessezeng/p/5144317.html](https://www.cnblogs.com/jessezeng/p/5144317.html)
[http://stackoverflow.com/questions/24177601/difference-between-asynclogger-and-asyncappender-in-log4j2](http://stackoverflow.com/questions/24177601/difference-between-asynclogger-and-asyncappender-in-log4j2)
[http://www.cnblogs.com/backpacker/archive/2012/12/10/2812100.html](http://www.cnblogs.com/backpacker/archive/2012/12/10/2812100.html)

简单使用可以这样

```java
BasicConfigurator.configure();
```

不需要配置文件
filePattern (注意使用.gz的后缀会自动压缩，若是.log则是原始文本)

### rollingfile

[https://issues.apache.org/jira/browse/LOG4J2-435](https://issues.apache.org/jira/browse/LOG4J2-435)

```xml
<RollingFile name="Rolling" fileName="${sys:log.path}/${sys:project.name}/${sys:log.level}.log" filePattern="${sys:log.path}/${sys:project.name}/${sys:log.level}-%d{yyyyMMdd}-%i.log.zip">
    <PatternLayout charset="UTF-8">
        <Pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %p %c{1.} - %m%n</Pattern>
    </PatternLayout>
    <Policies>
        <TimeBasedTriggeringPolicy />
        <SizeBasedTriggeringPolicy size="1 MB" />
    </Policies>
    <DefaultRolloverStrategy max="160">
        <Delete basePath="${sys:log.path}/${sys:project.name}">
            <IfAny>
                <IfLastModified age="2d" />
                <IfAccumulatedFileSize exceeds="1 mb" />
            </IfAny>
        </Delete>
    </DefaultRolloverStrategy>
</RollingFile>
```
