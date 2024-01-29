---
title: MessageFormat
author: "-"
date: 2016-05-17T05:14:30+00:00
url: /?p=9004
categories:
  - Inbox
tags:
  - reprint
---
## MessageFormat
MessageFormat用法
  
博客分类: java
  
MessageFormatMessageFormat.format
  
MessageFormat用来格式化一个消息,通常是一个字符串,比如: 

String str = "I'm not a {0}, age is {1,number,short}", height is {2,number,#.#};


而MessageFormat可以格式化这样的消息,然后将格式化后的字符串插入到模式中的适当位置,比如: 

将str中的{0}用"pig"替换,{1,number,short}用数字8替换,{2,number,#.#}用数字1.2替换。

那么最终用户得到的是一个格式化好的字符串"I'm not a pig, age is 8, height is 1.2"。


MessageFormat本身与语言环境无关,而与用户提供给MessageFormat的模式和用于已插入参数的子格式模式有关,以生成适用于不同语言环境的消息。


MessageFormat模式 (主要部分) : 


FormatElement:
  
{ ArgumentIndex }
  
{ ArgumentIndex , FormatType }
  
{ ArgumentIndex , FormatType , FormatStyle }


FormatType:
  
number

date

time

choice (需要使用ChoiceFormat) 


FormatStyle:
  
short
  
medium
  
long
  
full
  
integer
  
currency
  
percent
  
SubformatPattern (子模式) 


还以str为例,在这个字符串中: 

1. {0}和{1,number,short}和{2,number,#.#};都属于FormatElement,0,1,2是ArgumentIndex。

2. {1,number,short}里面的number属于FormatType,short则属于FormatStyle。

3. {1,number,#.#}里面的#.#就属于子格式模式。


指定FormatType和FormatStyle是为了生成日期格式的值、不同精度的数字、百分比类型等等。


实例: 

1. ArgumentIndex必须是非负整数,它的个数不只限于0到9这10个,它可以用0到9的数字组成,因此可以有好多个,如: 

Java代码
  
String pig = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}";

Object[] array = new Object[]{"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: ABCDEFGHIJKLMNOPQ


2. 格式化字符串时,两个单引号才表示一个单引号,单个单引号会被省略,如: 

Java代码
  
String message = "oh, {0} is 'a' pig";

Object[] array = new Object[]{"ZhangSan"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, ZhangSan is a pig


给字母a加上单引号,如: 

Java代码
  
String message = "oh, {0} is "a" pig";

Object[] array = new Object[]{"ZhangSan"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, ZhangSan is 'a' pig


3. 单引号会使某个字符或串保持原形。

所以,假如没有特殊要求,一般都是要在正式格式化之前把单引号都去掉,否则会造成不必要的麻烦,如: 

Java代码
  
String message = "oh, '{0}' is a pig";

Object[] array = new Object[]{"ZhangSan"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, {0} is 'a' pig,此处ZhangSan无法显示。


又如,使用子格式模式,多了一个单引号: 

Java代码
  
String message = "oh, '{0,number,#.#} is a pig";

Object[] array = new Object[]{new Double(3.1415)};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, {0,number,#.#}  is 'a' pig。


如果像下面这样,就可以正确显示: 

Java代码
  
String message = "oh, {0,number,#.#} is a pig";

Object[] array = new Object[]{new Double(3.1415)};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, 3.1 is a pig


3. 无论是有引号字符串还是无引号字符串,左花括号都是不支持的,但支持右花括号显示,如: 

Java代码
  
String message = "oh, { is a pig";

Object[] array = new Object[]{"ZhangSan"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: 异常java.lang.IllegalArgumentException: Unmatched braces in the pattern


右花括号可以显示,如: 

Java代码
  
String message = "oh, } is a pig";

Object[] array = new Object[]{"ZhangSan"};

String value = MessageFormat.format(message, array);

System.out.println(value);
  
最终结果是: oh, } is a pig

关于MessageFormat.format方法: 

每调用一次MessageFormat.format方法,都会新创建MessageFormat的一个实例,相当于MessageFormat只使用了一次。MessageFormat类的format方法如下: 

Java代码
  
public static String format(String pattern, Object ... arguments)
  
{
  
MessageFormat temp = new MessageFormat(pattern);
  
return temp.format(arguments);
  
}
  
如果要重复使用某个MessageFormat实例,可以用如下方式: 

Java代码
  
String message = "oh, {0} is a pig";

MessageFormat messageFormat = new MessageFormat(message);

Object[] array = new Object[]{"ZhangSan"};

String value = messageFormat.format(array);

System.out.println(value);
  
最终结果是: oh, ZhangSan is a pig


//TODO

import org.slf4j.helpers.MessageFormatter;