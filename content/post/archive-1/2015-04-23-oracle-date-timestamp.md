---
title: oracle date timestamp
author: wiloon
type: post
date: 2015-04-23T01:02:43+00:00
url: /?p=7481
categories:
  - Uncategorized

---
http://wenku.baidu.com/view/9c73c0d349649b6648d747fc.html



oracle中TIMESTAMP与DATE比较
  
oracle数据库中timestamp数据类型精度

DATE数据类型
  
这个数据类型我们实在是太熟悉了，当我们需要表示日期和时间的话都会想到date类型。它可以存储月，年，日，世纪，时，分和秒。它典型地用来表示什么时候事情已经发生或将要发生。DATE数据类型的问题在于它表示两个事件发生时间间隔的度量粒度是秒。这个问题将在文章稍后讨论timestamp的时候被解决。可以使用TO_CHAR函数把DATE数据进行传统地包装，达到表示成多种格式的目的。

我见到的大多数人陷入的麻烦就是计算两个时间的间隔年数、月数、天数、小时数和秒数。你需要明白的是，当你进行两个日期的相减运算的时候，得到的是天数。你需要乘上每天的秒数（1天=86400秒），然后，你可以再次计算得到你想要的间隔数。下面就是我的解决方法，可以精确计算出两个时间的间隔。我明白这个例子可以更简短些，但是我是为了显示所有的数字来强调计算方式。
  
SELECT TO\_CHAR(date1,'MMDDYYYY:HH24:MI:SS') date1, TO\_CHAR(date2,'MMDDYYYY:HH24:MI:SS') date2,
  
trunc(86400\*(date2-date1))-60\*(trunc((86400\*(date2-date1))/60))  seconds,   trunc((86400\*(date2-date1))/60)-60\*(trunc(((86400\*(date2-date1))/60)/60)) minutes,   trunc(((86400\*(date2-date1))/60)/60)-24\*(trunc((((86400\*(date2-date1))/60)/60)/24)) hours,   trunc((((86400\*(date2-date1))/60)/60)/24) days,   trunc(((((86400*(date2-date1))/60)/60)/24)/7) weeks   FROM date_table
  
DATE1  DATE2  SECONDS  MINUTES  HOURS   DAYS  WEEKS     ------ ------ ---- ---- ---- ---- ---- 06202003:16:55:14 07082003:11:22:57   43  27  18     17  2 06262003:11:16:36 07082003:11:22:57   21   6  0    12  1

TIMESTAMP 数据类型
  
DATE数据类型的主要问题是它粒度不能足够区别出两个事件哪个先发生。ORACLE已经在DATE数据类型上扩展出来了TIMESTAMP数据类型，它包括了所有DATE数据类型的年月日时分秒的信息，而且包括了小数秒的信息。如果你想把DATE类型转换成TIMESTAMP类型，就使用CAST函数。

正如你看到的，在转换后的时间段尾部有了一段“.000000”。这是因为从date转换过来的时候，没有小数秒的信息，缺省为0。而且显示格式是按照参数NLS\_TIMESTAMP\_FORMAT定的缺省格式显示。当你把一个表中date类型字段的数据移到另一个表的timestamp类型字段中去的时候，可以直接写INSERT SELECT语句，oracle会自动为你做转换的。
  
TIMESTAMP数据的格式化显示和DATE 数据一样。注意，to_char函数支持date和timestamp，但是trunc却不支持TIMESTAMP数据类型。这已经清楚表明了在当两个时间的差别极度重要的情况下，使用TIMESTAMP数据类型要比DATE数据类型更确切     如果你想显示TIMESTAMP的小数秒信息，参考下面：

在上例中，我只现实了小数点后3位的内容。
  
计算timestamp间的数据差别要比老的date数据类型更容易。当你直接相减的话，看看会发生什么。结果将更容易理解，第一行的17天，18小时，27分钟和43秒。

SELECT time1,  time2,
  
substr((time2-time1),instr((time2-time1),' ')+7,2)   seconds,   substr((time2-time1),instr((time2-time1),' ')+4,2)   minutes,   substr((time2-time1),instr((time2-time1),' ')+1,2)   hours,
  
trunc(to\_number(substr((time2-time1),1,instr(time2-time1,' '))))  days,   trunc(to\_number(substr((time2-time1),1,instr(time2-time1,' ')))/7) weeks FROM date_table
  
TIME1  TIME2   SECONDS   MINUTES   HOURS   DAYS   WEEKS   ---------  --------- --- --- -- -- --
  
06/20/2003:16:55:14:000000 07/08/2003:11:22:57:000000 43   27   18  17  2 06/26/2003:11:16:36:000000 07/08/2003:11:22:57:000000 21   06   00  12  1   这就意味着不再需要关心一天有多少秒在麻烦的计算中。因此，得到天数、月数、天数、时数、分钟数和秒数就成为用substr函数摘取出数字的事情了
  
系统日期和时间
  
为了得到系统时间，返回成date数据类型。你可以使用sysdate函数。

为了得到系统时间，返回成timestamp数据类型。你可以使用systimestamp函数。

你可以设置初始化参数FIXED\_DATE指定sysdate函数返回一个固定值。这用在测试日期和时间敏感的代码。注意，这个参数对于systimestamp函数无效。   SQL> ALTER SYSTEM SET fixed\_date = '2003-01-01-10:00:00';

System altered.
  
SQL> select sysdate from dual;
  
SYSDATE   ---   01-JAN-03
  
SQL> select systimestamp from dual;
  
SYSTIMESTAMP
  
-------------------   09-JUL-03 11.05.02.519000 AM -06:00
  
当使用date和timestamp类型的时候，选择是很清楚的。你可以随意处置date和timestamp类型。当你试图转换到更强大的timestamp的时候，需要注意，它们既有类似的地方，更有不同的地方，而足以造成破坏。两者在简洁和间隔尺寸方面各有优势，请合理选择。另外，date类型一般很少用，建议大家在产品里面所有的date数据类型全部改为timestamp。





http://www.cnblogs.com/linximf/archive/2011/11/21/2257036.html