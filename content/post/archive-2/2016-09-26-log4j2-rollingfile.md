---
title: 'log4j2  配置'
author: wiloon
type: post
date: 2016-09-26T10:42:01+00:00
url: /?p=9223
categories:
  - Uncategorized

---
简单使用可以这样

```java
BasicConfigurator.configure();
```

不需要配置文件
filePattern（注意使用.gz的后缀会自动压缩，若是.log则是原始文本）

### rollingfile

https://issues.apache.org/jira/browse/LOG4J2-435

```xml
<RollingFile
name="Rolling"
fileName="${sys:log.path}/${sys:project.name}/${sys:log.level}.log"
filePattern="${sys:log.path}/${sys:project.name}/${sys:log.level}-%d{yyyyMMdd}-%i.log.zip">
<PatternLayout charset="UTF-8">
<Pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %p %c{1.} - %m%n</Pattern>
</PatternLayout>
<Policies>
<TimeBasedTriggeringPolicy/>
<SizeBasedTriggeringPolicy size="1 MB"/>
</Policies>
<DefaultRolloverStrategy max="160">
<Delete basePath="${sys:log.path}/${sys:project.name}">
<IfAny>
<IfLastModified age="2d"/>
<IfAccumulatedFileSize exceeds="1 mb"/>
</IfAny>
</Delete>
</DefaultRolloverStrategy>
</RollingFile>
```