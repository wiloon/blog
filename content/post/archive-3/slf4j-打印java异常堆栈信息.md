---
title: slf4j 打印java异常堆栈信息
author: "-"
date: 2019-08-23T07:03:16+00:00
url: /?p=14828
categories:
  - Uncategorized

tags:
  - reprint
---
## slf4j 打印java异常堆栈信息
SLF4J 1.6.0以前的版本，如果打印异常堆栈信息，必须用

log.error(String msg, Throwable t)

log.info等对应方法．

如果msg含有变量，一般用String.format方法格式化msg.

如果用

error(String format, Object... arguments)
  
等其它方法，异常堆栈信息会丢失．
  
幸好，SLF4J 1.6.0以后的版本对这个不友好的异常信息ｌｏｇ改进了．

error(String format, Object... arguments)这个方法也会打印异常堆栈信息，只不过规定throwable对象必须为

最后一个参数．如果不遵守这个规定，异常堆栈信息不会ｌｏｇ出来．

官方ＦAＱ: http://www.slf4j.org/faq.html

Can I log an exception without an accompanying message?
  
In short, no.

If e is an Exception, and you would like to log an exception at the ERROR level, you must add an accompanying message. For example,

logger.error("some accompanying message", e);
  
You might legitimately argue that not all exceptions have a meaningful message to accompany them. Moreover, a good exception should already contain a self explanatory description. The accompanying message may therefore be considered redundant.

While these are valid arguments, there are three opposing arguments also worth considering. First, on many, albeit not all occasions, the accompanying message can convey useful information nicely complementing the description contained in the exception. Frequently, at the point where the exception is logged, the developer has access to more contextual information than at the point where the exception is thrown. Second, it is not difficult to imagine more or less generic messages, e.g. "Exception caught", "Exception follows", that can be used as the first argument for error(String msg, Throwable t) invocations. Third, most log output formats display the message on a line, followed by the exception on a separate line. Thus, the message line would look inconsistent without a message.

In short, if the user were allowed to log an exception without an accompanying message, it would be the job of the logging system to invent a message. This is actually what the throwing(String sourceClass, String sourceMethod, Throwable thrown)method in java.util.logging package does. (It decides on its own that accompanying message is the string "THROW".)

It may initially appear strange to require an accompanying message to log an exception. Nevertheless, this is common practice in all log4j derived systems such as java.util.logging, logkit, etc. and of course log4j itself. It seems that the current consensus considers requiring an accompanying message as a good a thing (TM).

In the presence of an exception/throwable, is it possible to parameterize a logging statement?
  
Yes, as of SLF4J 1.6.0, but not in previous versions. The SLF4J API supports parametrization in the presence of an exception, assuming the exception is the last parameter. Thus,

String s = "Hello world";
  
try {
    
Integer i = Integer.valueOf(s);
  
} catch (NumberFormatException e) {
    
logger.error("Failed to format {}", s, e);
  
}
  
will print the NumberFormatException with its stack trace as expected. The java compiler will invoke the error method taking a String and two Object arguments. SLF4J, in accordance with the programmer's most probable intention, will interpret NumberFormatException instance as a throwable instead of an unused Object parameter. In SLF4J versions prior to 1.6.0, the NumberFormatException instance was simply ignored.

If the exception is not the last argument, it will be treated as a plain object and its stack trace will NOT be printed. However, such situations should not occur in practice.

版权声明: 本文为博主原创文章，遵循 CC 4.0 by-sa 版权协议，转载请附上原文出处链接和本声明。
  
本文链接: https://blog.csdn.net/doctor_who2004/article/details/43569407