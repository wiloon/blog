---
title: java 日期/date time
author: "-"
date: 2011-09-06T07:30:27+00:00
url: /?p=682

categories:
  - inbox
tags:
  - reprint
---
## java 日期/date time
日期计算

Calendar cal = Calendar.getInstance();//使用默认时区和语言环境获得一个日历。
  
cal.add(Calendar.DAY_OF_MONTH, -1);//取当前日期的前一天.
  
cal.add(Calendar.DAY_OF_MONTH, +1);//取当前日期的后一天.
  
//通过格式化输出日期
  
java.text.SimpleDateFormat format = new java.text.SimpleDateFormat("yyyy-MM-dd");
  
System.out.println("Today is:"+format.format(Calendar.getInstance().getTime()));
  
System.out.println("yesterday is:"+format.format(cal.getTime()));
  
得到2007-12-25日期:

y 年 Year 1996; 96
  
M 年中的月份 Month July; Jul; 07

d 月份中的天数 Number 10

H 一天中的小时数 (0-23)  Number 0

m 小时中的分钟数 Number 30

s 分钟中的秒数 Number 55
  
S 毫秒数 Number 978


  
    java 8 日期/date time
  


http://www.wiloon.com/?p=8834&embed=true#?secret=RA1Eqnm13T


  
    joda-time, ThreeTen Backport
  


 http://www.wiloon.com/?p=3269&embed=true#?secret=qXtE3cmQSt
  
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSS");
  
System.out.println(sdf.format(1318495528278l));

//date to string
  
new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSS").format(new Date())

//Timestamp -&amp;gt; Date
  
Timestamp ts = new Timestamp(System.currentTimeMillis());
   
Date date = new Date();
   
try {
   
date = ts;
   
System.out.println(date);
   
} catch (Exception e) {
   
e.printStackTrace();
   
}

Date -&amp;gt; Timestamp

&amp;nbsp;&amp;nbsp; 父类不能直接向子类转化，可借助中间的String~~~~

&amp;nbsp;&amp;nbsp; 注: 使用以下方式更简洁

&amp;nbsp;&amp;nbsp; Timestamp ts = new Timestamp(date.getTime());
   
日期转字符串

SimpleDateFormat sdf = new SimpleDateFormat( " yyyy年MM月dd日 " );
  
String datestr = sdf.format( new Date());

datestr便会依照我们设定的格式输出

附
  
SimpleDateFormat parser = new SimpleDateFormat("EEEE, MMMM dd, yyyy");
  
SimpleDateFormat formatter = new SimpleDateFormat("EEE. MM/dd");

long start = System.currentTimeMillis();
  
start = new Date().getTime();

在使用SimpleDateFormat时格式化时间的 yyyy.MM.dd 为年月日而如果希望格式化时间为12小时制的，则使用hh:mm:ss 如果希望格式化时间为24小时制的，则使用HH:mm:ss

JAVA字符串转日期或日期转字符串
  
文章中，用的API是SimpleDateFormat，它是属于java.text.SimpleDateFormat，所以请记得import进来！

用法: 

SimpleDateFormat sdf = new SimpleDateFormat( " yyyy-MM-dd HH:mm:ss " );

这一行最重要，它确立了转换的格式，yyyy是完整的公元年，MM是月份，dd是日期，至于HH:mm:ss就不需要我再解释了吧！

ps:为什么有的格式大写，有的格式小写，那是怕避免混淆，例如MM是月份，mm是分；HH是24小时制，而hh是12小时制

1.字符串转日期: 

2002-10-8 15:30:22要把它转成日期，可以用

Date date = sdf.parse( " 2002-10-8 15:30:22 " );

2.日期转字符串

假如把今天的日期转成字符串可用
  
String datestr = sdf.format( new Date());

这个字符串的内容便类似2002-10-08 14:55:38

透过这个API我们便可以随心所欲的将日期转成我们想要的字符串格式，例如希望将日期输出成2002年10月08日，

我们可以这么写: 

SimpleDateFormat sdf = new SimpleDateFormat( " yyyy年MM月dd日 " );
  
String datestr = sdf.format( new Date());

datestr便会依照我们设定的格式输出

附
  
SimpleDateFormat parser = new SimpleDateFormat("EEEE, MMMM dd, yyyy");
  
SimpleDateFormat formatter = new SimpleDateFormat("EEE. MM/dd");

http://blog.csdn.net/xymyeah/article/details/1654364
  
http://www.blogjava.net/lingyu/articles/86400.html
  
http://www.blogjava.net/lingyu/articles/86400.html