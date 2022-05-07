---
title: Log4j 日志级别
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6788
categories:
  - Inbox
tags:
  - Java
  - logging

---
## Log4j 日志级别

log4j是apache基金会的一个项目,日志记录器(Logger)是日志处理的核心组件,log4j具有7种级别(Level).

    TRACE<DEBUG<INFO<WARN<ERROR<FATAL

日志记录器 (Logger) 的行为是分等级的。如下表所示:
  
分为OFF、FATAL、ERROR、WARN、INFO、DEBUG、TRACE、ALL或者您定义的级别。  
Log4j建议只使用四个级别，优先级从高到低分别是ERROR、WARN、INFO、DEBUG。通过在这里定义的级别，您可以控制到应用程序中相应级别的日志信息的开关。比如在这里定义了INFO级别，则应用程序中所有DEBUG级别的日志信息将不被打印出来。程序会打印高于或等于所设置级别的日志，设置的日志等级越高，打印出来的日志就越少。如果设置级别为INFO，则优先级高于等于INFO级别 (如: INFO、WARN、ERROR) 的日志信息将可以被输出,小于该级别的如DEBUG将不会被输出。

<http://blog.sina.com.cn/s/blog_9c7ba64d01012z02.html>

日志记录器(Logger)是日志处理的核心组件。
  
log4j具有5种正常级别(Level)。
  
日志记录器(Logger)的可用级别Level (不包括自定义级别 Level)， 以下内容就是摘自log4j API (<http://jakarta.apache.org/log4j/docs/api/index.html>):
  
public static final Level TRACE
  
TheTRACELevel designates finer-grained informational events than the DEBUG.Since:1.2.12

### ALL

最低等级的，用于打开所有日志记录。

### DEBUG

细粒度信息事件对调试应用程序是非常有帮助的。

### INFO

粗粒度级别上突出强调应用程序的运行过程。

### WARN

会出现潜在错误的情形。

### ERROR

虽然发生错误事件，但仍然不影响系统的继续运行。

### FATAL

每个严重的错误事件将会导致应用程序的退出。
另外，还有两个可用的特别的日志记录级别: (以下描述来自log4j API <http://jakarta.apache.org/log4j/docs/api/index.html>):

### OFF

最高等级的，用于关闭所有日志记录。

<http://blog.csdn.net/maxracer/article/details/7920997>

Log4j 日志级别
  
标签:  log4japache服务器
  
2012-08-29 16:40 9516人阅读 评论(0) 收藏 举报
  
分类:
  
log4j (1)
  
版权声明: 本文为博主原创文章，未经博主允许不得转载。
  
官方网址: <http://logging.apache.org/log4j/1.2/>
  
DEBUG Level: 细粒度信息事件对调试应用程序是非常有帮助.
  
INFO level: 在粗粒度级别上突出强调应用程序的运行过程.
  
WARN level: 会出现潜在错误的情形, 警告信息.
  
ERROR level: 虽然发生错误事件,但仍然不影响系统的继续运行.错误信息.
  
FATAL level: 严重的错误事件将会导致应用程序的退出.
  
ALL level: 是最低等级的,用于打开所有日志记录.
  
OFF level: 是最高等级的,用于关闭所有日志记录.

log4j 建议只使用五个级别,级别顺序(由低到高): DEBUG < INFO < WARN < ERROR < FATAL

windows下控制台效率比较差,输出的多了,非常影响服务器性能.
  
调试程序用debug或更低的优先级,这样开发的时候可以尽量输出,方便调试.
  
正式部署之后,可以提高日志的级别,只输出关键信息.
