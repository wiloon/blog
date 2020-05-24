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

<pre><code class="language-java line-numbers">BasicConfigurator.configure();
```

不需要配置文件

filePattern（注意使用.gz的后缀会自动压缩，若是.log则是原始文本）

### rollingfile

https://issues.apache.org/jira/browse/LOG4J2-435<pre data-language=XML>

<code class="language-markup line-numbers">&lt;RollingFile
name="Rolling"
fileName="${sys:log.path}/${sys:project.name}/${sys:log.level}.log"
filePattern="${sys:log.path}/${sys:project.name}/${sys:log.level}-%d{yyyyMMdd}-%i.log.zip"&gt;
&lt;PatternLayout charset="UTF-8"&gt;
&lt;Pattern&gt;%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %p %c{1.} - %m%n&lt;/Pattern&gt;
&lt;/PatternLayout&gt;
&lt;Policies&gt;
&lt;TimeBasedTriggeringPolicy/&gt;
&lt;SizeBasedTriggeringPolicy size="1 MB"/&gt;
&lt;/Policies&gt;
&lt;DefaultRolloverStrategy max="160"&gt;
&lt;Delete basePath="${sys:log.path}/${sys:project.name}"&gt;
&lt;IfAny&gt;
&lt;IfLastModified age="2d"/&gt;
&lt;IfAccumulatedFileSize exceeds="1 mb"/&gt;
&lt;/IfAny&gt;
&lt;/Delete&gt;
&lt;/DefaultRolloverStrategy&gt;
&lt;/RollingFile&gt;
```