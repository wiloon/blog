---
title: java8 日期/date time
author: "-"
date: 2016-03-27T07:27:22+00:00
url: /?p=8834
categories:
  - Uncategorized

tags:
  - reprint
---
## java8 日期/date time
在java8中,java.time包下主要包含下面几个主要的类
  
### Instant: 
时间戳,含有时区信息, Instant与ZonedDateTime是等价的  
Instant是时间戳,是指世界标准时格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数,Instant本身实际上就指明时区了,0时区。
### ZonedDateTime
是含有时区信息的时间,本质上是根据时区对Instant的格式化显示。
### LocalDateTime: 
包含日期和时间,比如: 2016-10-20 23:14:21, 不含时区信息的时间, 没有偏移信息或者说时区。

  * Duration: 持续时间,时间差
  * LocalDate: 只包含日期,比如: 2016-10-20
  * LocalTime: 只包含时间,比如: 23:12:10

  * Period: 时间段
  * ZoneOffset: 时区偏移量,比如: +8:00
  * ZonedDateTime: 带时区的时间
  * Clock: 时钟,比如获取目前美国纽约的时间

### localdatetime > date

```java
public static void main(String[] args) {
    ZoneId zoneId = ZoneId.systemDefault();
    LocalDateTime localDateTime = LocalDateTime.now();
    ZonedDateTime zdt = localDateTime.atZone(zoneId);

    Date date = Date.from(zdt.toInstant());

    System.out.println("LocalDateTime = " + localDateTime);
    System.out.println("Date = " + date);
    }
```

```java
    String foo = "";
    DateTimeFormatter formatterCompact = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ssXXX");
    foo = ZonedDateTime.now().format(formatterCompact);
    System.out.println(foo);

    # String to LocalDateTime
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");
    LocalDateTime dateTime = LocalDateTime.parse("2016-09-21 13:43:27.000", formatter);

    # LocalDateTime to String
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
    LocalDateTime dateTime = LocalDateTime.of(1986, Month.APRIL, 8, 12, 30);
    String formattedDateTime = dateTime.format(formatter); // "1986-04-08 12:30"
```

### instant > Date
    Date myDate = Date.from(instant);

### 计算时间间隔

Java8之前,我们想要确定一个方法的运行时间长度,可以这样: 
```java
    long start = System.currentTimeMillis();
    doSomething();
    long end = System.currentTimeMillis();
    System.out.println(end-start);
```
Java8中,可以这样  
```java
    Instant start = Instant.now();
    // doSomething();
    Instant end = Instant.now();
    Duration time = Duration.between(start, end);
    long seconds = time.getSeconds(); //秒表示
    long millis = time.toMillis(); //毫秒表示
    System.out.println(seconds);
    System.out.println(millis);
```
可以轻松选择用纳秒、毫秒、秒、分钟、小时或者天来表示时间间隔的单位。

https://my.oschina.net/benhaile/blog/193956
  
### 格式化

```java
localDate date = LocalDate.now();
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy MM dd");
String text = date.format(formatter);
LocalDate parsedDate = LocalDate.parse(text, formatter);
http://it.deepinmind.com/java/2015/03/17/20-examples-of-date-and-time-api-from-Java8.html

//sql timestamp to local date time
timestamp.toLocalDateTime();

```

### Java8中计算日期时间差
在Java8中,我们可以使用以下类来计算日期时间差异: 
  
1. Period:  主要是Period类方法getYears () ,getMonths () 和getDays () 来计算.
2. Duration:  提供了使用基于时间的值 (如秒,纳秒) 测量时间量的方法。
3. ChronoUnit:  ChronoUnit类可用于在单个时间单位内测量一段时间,例如天数或秒。

#### java 8中的周期类Period
通过调用Period类的静态方法between,传入两个待比较的LocalDate对象today与oldDate,得到的Period的对象p中就包含了today与oldDate两个日期相差的年、月、日信息,可以通过p.getYears()等方法取出

```java
/**
 * 使用java 8的Period的对象计算两个LocalDate对象的时间差,严格按照年、月、日计算,如: 2018-03-12 与 2014-05-23 相差 3 年 9 个月 17 天
 * @param year
 * @param month
 * @param dayOfMonth
 */
public static void calculateTimeDifferenceByPeriod(int year, Month month, int dayOfMonth) {
    LocalDate today = LocalDate.now();
    System.out.println("Today: " + today);
    LocalDate oldDate = LocalDate.of(year, month, dayOfMonth);
    System.out.println("OldDate: " + oldDate);

    Period p = Period.between(oldDate, today);
    System.out.printf("目标日期距离今天的时间差: %d 年 %d 个月 %d 天\n", p.getYears(), p.getMonths(), p.getDays());
}
```

#### Duration类
Duration与Period相对应,Period用于处理日期,而Duration计算时间差还可以处理具体的时间,也是通过调用其静态的between方法,该方法的签名是between(Temporal startInclusive, Temporal endExclusive),因此可以传入两个Instant的实例 (Instant实现了Temporal接口) ,并可以以毫秒 (toMillis) 、秒 (getSeconds) 等多种形式表示得到的时间差

```java
public static void calculateTimeDifferenceByDuration() {
    Instant inst1 = Instant.now();  //当前的时间
    System.out.println("Inst1: " + inst1);
    Instant inst2 = inst1.plus(Duration.ofSeconds(10));     //当前时间+10秒后的时间
    System.out.println("Inst2: " + inst2);
    Instant inst3 = inst1.plus(Duration.ofDays(125));       //当前时间+125天后的时间
    System.out.println("inst3: " + inst3);

    System.out.println("以毫秒计的时间差: " + Duration.between(inst1, inst2).toMillis());
    System.out.println("以秒计的时间差: " + Duration.between(inst1, inst3).getSeconds());
}
```

https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html

Java 8新的时间日期库的20个使用示例

Published: 17 Mar 2015 Category: java
  
除了lambda表达式,stream以及几个小的改进之外,Java 8还引入了一套全新的时间日期API,在本篇教程中我们将通过几个简单的任务示例来学习如何使用Java 8的这套API。Java对日期,日历及时间的处理一直以来都饱受诟病,尤其是它决定将java.util.Date定义为可修改的以及将SimpleDateFormat实现成非线程安全的。看来Java已经意识到需要为时间及日期功能提供更好的支持了,这对已经习惯使用Joda时间日期库的社区而言也是件好事。关于这个新的时间日期库的最大的优点就在于它定义清楚了时间日期相关的一些概念,比方说,瞬时时间 (Instant) ,持续时间 (duration) ,日期 (date) ,时间 (time) ,时区 (time-zone) 以及时间段 (Period) 。同时它也借鉴了Joda库的一些优点,比如将人和机器对时间日期的理解区分开的。Java 8仍然延用了ISO的日历体系,并且与它的前辈们不同,java.time包中的类是不可变且线程安全的。新的时间及日期API位于java.time包中,下面是里面的一些关键的类: 

Instant——它代表的是时间戳
  
LocalDate——不包含具体时间的日期,比如2014-01-14。它可以用来存储生日,周年纪念日,入职日期等。
  
LocalTime——它代表的是不含日期的时间
ZonedDateTime——这是一个包含时区的完整的日期时间,偏移量是以UTC/格林威治时间为基准的。
  
新的库还增加了ZoneOffset及Zoned,可以为时区提供更好的支持。有了新的DateTimeFormatter之后日期的解析及格式化也变得焕然一新了。随便提一句,我是在去年这个时候Java正要推出这个新功能时写的这篇文章,所以你会发现示例中的时间都还是去年的。你运行下这些例子,它们返回的值肯定都是正确的。

Java 8是如何处理时间及日期的

有人问我学习一个新库的最佳途径是什么？我的回答是,就是在实际项目中那样去使用它。在一个真实的项目中会有各种各样的需求,这会促使开发人员去探索和研究这个新库。简言之,只有任务本身才会真正促使你去探索及学习。java 8的新的日期及时间API也是一样。为了学习Java 8的这个新库,这里我创建了20个以任务为导向的例子。我们先从一个简单的任务开始,比如说如何用Java 8的时间日期库来表示今天,接着再进一步生成一个带时间及时区的完整日期,然后再研究下如何完成一些更实际的任务,比如说开发一个提醒类的应用,来找出距离一些特定日期比如生日,周日纪念日,下一个帐单日,下一个溢价日或者信用卡过期时间还有多少天。

示例1 如何 在Java 8中获取当天的日期

Java 8中有一个叫LocalDate的类,它能用来表示今天的日期。这个类与java.util.Date略有不同,因为它只包含日期,没有时间。因此,如果你只需要表示日期而不包含时间,就可以使用它。

LocalDate today = LocalDate.now(); System.out.println("Today's Local date : " + today);

Output
  
Today's Local date : 2014-01-14
  
你可以看到它创建了今天的日期却不包含时间信息。它还将日期格式化完了再输出出来,不像之前的Date类那样,打印出来的数据都是未经格式化的。

示例2 如何在Java 8中获取当前的年月日

LocalDate类中提供了一些很方便的方法可以用于提取出年月日以及其它的日期属性。使用这些方法,你可以获取到任何你所需要的日期属性,而不再需要使用java.util.Calendar这样的类了: 

LocalDate today = LocalDate.now();
  
int year = today.getYear();
  
int month = today.getMonthValue();
  
int day = today.getDayOfMonth();
  
System.out.printf("Year : %d Month : %d day : %d \t %n", year, month, day);

Output
  
Today's Local date : 2014-01-14
  
Year : 2014 Month : 1 day : 14
  
可以看到,在Java 8中获取年月信息非常简单,只需使用对应的getter方法就好了,无需记忆,非常直观。你可以拿它和Java中老的获取当前年月日的写法进行一下比较。

示例3 在Java 8中如何获取某个特定的日期

在第一个例子中,我们看到通过静态方法now()来生成当天日期是非常简单的,不过通过另一个十分有用的工厂方法LocalDate.of(),则可以创建出任意一个日期,它接受年月日的参数,然后返回一个等价的LocalDate实例。关于这个方法还有一个好消息就是它没有再犯之前API中的错,比方说,年只能从1900年开始,月必须从0开始,等等。这里的日期你写什么就是什么,比如说,下面这个例子中它代表的就是1月14日,没有什么隐藏逻辑。

LocalDate dateOfBirth = LocalDate.of(2010, 01, 14);
  
System.out.println("Your Date of birth is : " + dateOfBirth);

Output : Your Date of birth is : 2010-01-14
  
可以看出,创建出来的日期就是我们所写的那样,2014年1月14日。

示例4 在Java 8中如何检查两个日期是否相等

如果说起现实中实际的处理时间及日期的任务,有一个常见的就是要检查两个日期是否相等。你可能经常会碰到要判断今天是不是某个特殊的日子,比如生日啊,周年纪念日啊,或者假期之类。有的时候,会给你一个日期,让你检查它是不是某个日子比方说假日。下面这个例子将会帮助你在Java 8中完成这类任务。正如你所想的那样,LocalDate重写了equals方法来进行日期的比较,如下所示: 

LocalDate date1 = LocalDate.of(2014, 01, 14); if(date1.equals(today)){
      
System.out.printf("Today %s and date1 %s are same date %n", today, date1);
  
}

Output
  
today 2014-01-14 and date1 2014-01-14 are same date
  
在本例中我们比较的两个日期是相等的。同时,如果在代码中你拿到了一个格式化好的日期串,你得先将它解析成日期然后才能比较。你可以将这个例子与Java之前比较日期的方式进行下比较,你会发现它真是爽多了。

示例5 在Java 8中如何检查重复事件,比如说生日

在Java中还有一个与时间日期相关的实际任务就是检查重复事件,比如说每月的帐单日,结婚纪念日,每月还款日或者是每年交保险费的日子。如果你在一家电商公司工作的话,那么肯定会有这么一个模块,会去给用户发送生日祝福并且在每一个重要的假日给他们捎去问候,比如说圣诞节,感恩节,在印度则可能是万灯节 (Deepawali) 。如何在Java中判断是否是某个节日或者重复事件？使用MonthDay类。这个类由月日组合,不包含年信息,也就是说你可以用它来代表每年重复出现的一些日子。当然也有一些别的组合,比如说YearMonth类。它和新的时间日期库中的其它类一样也都是不可变且线程安全的,并且它还是一个值类 (value class) 。我们通过一个例子来看下如何使用MonthDay来检查某个重复的日期: 

LocalDate dateOfBirth = LocalDate.of(2010, 01, 14);
  
MonthDay birthday = MonthDay.of(dateOfBirth.getMonth(), dateOfBirth.getDayOfMonth());
  
MonthDay currentMonthDay = MonthDay.from(today);
  
if(currentMonthDay.equals(birthday)){
      
System.out.println("Many Many happy returns of the day !!");
  
}else{
      
System.out.println("Sorry, today is not your birthday");
  
}

Output: Many Many happy returns of the day !!
  
虽然年不同,但今天就是生日的那天,所以在输出那里你会看到一条生日祝福。你可以调整下系统的时间再运行下这个程序看看它是否能提醒你下一个生日是什么时候,你还可以试着用你的下一个生日来编写一个JUnit单元测试看看代码能否正确运行。

示例6 如何在Java 8中获取当前时间

这与第一个例子中获取当前日期非常相似。这次我们用的是一个叫LocalTime的类,它是没有日期的时间,与LocalDate是近亲。这里你也可以用静态工厂方法now()来获取当前时间。默认的格式是hh:mm:ss:nnn,这里的nnn是纳秒。可以和Java 8以前如何获取当前时间做一下比较。

LocalTime time = LocalTime.now(); System.out.println("local time now : " + time);

Output
  
local time now : 16:33:33.369 // in hour, minutes, seconds, nano seconds
  
可以看到,当前时间是不包含日期的,因为LocalTime只有时间,没有日期。

示例7 如何增加时间里面的小时数
  
很多时候我们需要增加小时,分或者秒来计算出将来的时间。Java 8不仅提供了不可变且线程安全的类,它还提供了一些更方便的方法譬如plusHours()来替换原来的add()方法。顺便说一下,这些方法返回的是一个新的LocalTime实例的引用,因为LocalTime是不可变的,可别忘了存储好这个新的引用。

LocalTime time = LocalTime.now();
  
LocalTime newTime = time.plusHours(2); // adding two hours
  
System.out.println("Time after 2 hours : " + newTime);

Output :
  
Time after 2 hours : 18:33:33.369
  
可以看到当前时间2小时后是16:33:33.369。现在你可以将它和Java中增加或者减少小时的老的方式进行下比较。一看便知哪种方式更好。

示例8 如何获取1周后的日期

这与前一个获取2小时后的时间的例子类似,这里我们将学会如何获取到1周后的日期。LocalDate是用来表示无时间的日期的,它有一个plus()方法可以用来增加日,星期,或者月,ChronoUnit则用来表示这个时间单位。由于LocalDate也是不可变的,因此任何修改操作都会返回一个新的实例,因此别忘了保存起来。

LocalDate nextWeek = today.plus(1, ChronoUnit.WEEKS);
  
System.out.println("Today is : " + today);
  
System.out.println("Date after 1 week : " + nextWeek);

Output:
  
Today is : 2014-01-14
  
Date after 1 week : 2014-01-21
  
可以看到7天也就是一周后的日期是什么。你可以用这个方法来增加一个月,一年,一小时,一分钟,甚至是十年,查看下Java API中的ChronoUnit类来获取更多选项。

示例9 一年前后的日期

这是上个例子的续集。上例中,我们学习了如何使用LocalDate的plus()方法来给日期增加日,周或者月,现在我们来学习下如何用minus()方法来找出一年前的那天。

LocalDate previousYear = today.minus(1, ChronoUnit.YEARS);
  
System.out.println("Date before 1 year : " + previousYear);
  
LocalDate nextYear = today.plus(1, YEARS);
  
System.out.println("Date after 1 year : " + nextYear);

Output:
  
Date before 1 year : 2013-01-14
  
Date after 1 year : 2015-01-14
  
可以看到现在一共有两年,一个是2013年,一个是2015年,分别是2014的前后那年。

示例10 在Java 8中使用时钟
  
Java 8中自带了一个Clock类,你可以用它来获取某个时区下当前的瞬时时间,日期或者时间。可以用Clock来替代System.currentTimeInMillis()与 TimeZone.getDefault()方法。

// Returns the current time based on your system clock and set to UTC.
  
Clock clock = Clock.systemUTC();
  
System.out.println("Clock : " + clock);

// Returns time based on system clock zone Clock defaultClock =
  
Clock.systemDefaultZone();
  
System.out.println("Clock : " + clock);

Output:
  
Clock : SystemClock[Z]
  
Clock : SystemClock[Z]
  
你可以用指定的日期来和这个时钟进行比较,比如下面这样: 

public class MyClass {
      
private Clock clock; // dependency inject ...
      
public void process(LocalDate eventDate) {
          
if(eventDate.isBefore(LocalDate.now(clock)) {
              
...
          
}
      
}
  
}
  
如果你需要对不同时区的日期进行处理的话这是相当方便的。

示例11 在Java中如何判断某个日期是在另一个日期的前面还是后面

这也是实际项目中常见的一个任务。你怎么判断某个日期是在另一个日期的前面还是后面,或者正好相等呢？在Java 8中,LocalDate类有一个isBefore()和isAfter()方法可以用来比较两个日期。如果调用方法的那个日期比给定的日期要早的话,isBefore()方法会返回true。

LocalDate tomorrow = LocalDate.of(2014, 1, 15); 、if(tommorow.isAfter(today)){
      
System.out.println("Tomorrow comes after today");
  
}
  
LocalDate yesterday = today.minus(1, DAYS);
  
if(yesterday.isBefore(today)){
      
System.out.println("Yesterday is day before today");
  
}

Output:
  
Tomorrow comes after today
  
Yesterday is day before today
  
可以看到在Java 8中进行日期比较非常简单。不需要再用像Calendar这样的另一个类来完成类似的任务了。

示例12 在Java 8中处理不同的时区

Java 8不仅将日期和时间进行了分离,同时还有时区。现在已经有好几组与时区相关的类了,比如ZonId代表的是某个特定的时区,而ZonedDateTime代表的是带时区的时间。它等同于Java 8以前的GregorianCalendar类。使用这个类,你可以将本地时间转换成另一个时区中的对应时间,比如下面这个例子: 

// Date and time with timezone in Java 8 ZoneId america = ZoneId.of("America/New_York");
  
LocalDateTime localtDateAndTime = LocalDateTime.now();
  
ZonedDateTime dateAndTimeInNewYork = ZonedDateTime.of(localtDateAndTime, america );
  
System.out.println("Current date and time in a particular timezone : " + dateAndTimeInNewYork);

Output :
  
Current date and time in a particular timezone : 2014-01-14T16:33:33.373-05:00[America/New_York]
  
可以拿它跟之前将本地时间转换成GMT时间的方式进行下比较。顺便说一下,正如Java 8以前那样,对应时区的那个文本可别弄错了,否则你会碰到这么一个异常: 

Exception in thread "main" java.time.zone.ZoneRulesException: Unknown time-zone ID: ASIA/Tokyo
          
at java.time.zone.ZoneRulesProvider.getProvider(ZoneRulesProvider.java:272)
          
at java.time.zone.ZoneRulesProvider.getRules(ZoneRulesProvider.java:227)
          
at java.time.ZoneRegion.ofId(ZoneRegion.java:120)
          
at java.time.ZoneId.of(ZoneId.java:403)
          
at java.time.ZoneId.of(ZoneId.java:351)
  
示例13 如何表示固定的日期,比如信用卡过期时间

正如MonthDay表示的是某个重复出现的日子的,YearMonth又是另一个组合,它代表的是像信用卡还款日,定期存款到期日,options到期日这类的日期。你可以用这个类来找出那个月有多少天,lengthOfMonth()这个方法返回的是这个YearMonth实例有多少天,这对于检查2月到底是28天还是29天可是非常有用的。

YearMonth currentYearMonth = YearMonth.now(); System.out.printf("Days in month year %s: %d%n", currentYearMonth, currentYearMonth.lengthOfMonth());
  
YearMonth creditCardExpiry = YearMonth.of(2018, Month.FEBRUARY);
  
System.out.printf("Your credit card expires on %s %n", creditCardExpiry);

Output:
  
Days in month year 2014-01: 31
  
Your credit card expires on 2018-02
  
示例14 如何在Java 8中检查闰年

这并没什么复杂的,LocalDate类有一个isLeapYear()的方法能够返回当前LocalDate对应的那年是否是闰年。如果你还想重复造轮子的话,可以看下这段代码,这是纯用Java编写的判断某年是否是闰年的逻辑。

if(today.isLeapYear()){
      
System.out.println("This year is Leap year");
  
}else {
      
System.out.println("2014 is not a Leap year");
  
}

Output: 2014 is not a Leap year
  
你可以多检查几年看看结果是否正确,最好写一个单元测试来对正常年份和闰年进行下测试。

示例15 两个日期之间包含多少天,多少个月

还有一个常见的任务就是计算两个给定的日期之间包含多少天,多少周或者多少年。你可以用java.time.Period类来完成这个功能。在下面这个例子中,我们将计算当前日期与将来的一个日期之前一共隔着几个月。

LocalDate java8Release = LocalDate.of(2014, Month.MARCH, 14);
  
Period periodToNextJavaRelease =
  
Period.between(today, java8Release);
  
System.out.println("Months left between today and Java 8 release : " + periodToNextJavaRelease.getMonths() );

Output:
  
Months left between today and Java 8 release : 2
  
可以看到,本月是1月,而Java 8的发布日期是3月,因此中间隔着2个月。

示例16 带时区偏移量的日期与时间

在Java 8里面,你可以用ZoneOffset类来代表某个时区,比如印度是GMT或者UTC5: 30,你可以使用它的静态方法ZoneOffset.of()方法来获取对应的时区。只要获取到了这个偏移量,你就可以拿LocalDateTime和这个偏移量创建出一个OffsetDateTime。

LocalDateTime datetime = LocalDateTime.of(2014, Month.JANUARY, 14, 19, 30);
  
ZoneOffset offset = ZoneOffset.of("+05:30");
  
OffsetDateTime date = OffsetDateTime.of(datetime, offset);
  
System.out.println("Date and Time with timezone offset in Java : " + date);

Output :
  
Date and Time with timezone offset in Java : 2014-01-14T19:30+05:30
  
可以看到现在时间日期与时区是关联上了。还有一点就是,OffSetDateTime主要是给机器来理解的,如果是给人看的,可以使用ZoneDateTime类。

示例17 在Java 8中如何获取当前时间戳

如果你还记得在Java 8前是如何获取当前时间戳的,那现在这简直就是小菜一碟了。Instant类有一个静态的工厂方法now()可以返回当前时间戳,如下: 

Instant timestamp = Instant.now();
  
System.out.println("What is value of this instant " + timestamp);

Output :
  
What is value of this instant 2014-01-14T08:33:33.379Z
  
可以看出,当前时间戳是包含日期与时间的,与java.util.Date很类似,事实上Instant就是Java 8前的Date,你可以使用这两个类中的方法来在这两个类型之间进行转换,比如Date.from(Instant)是用来将Instant转换成java.util.Date的,而Date.toInstant()是将Date转换成Instant的。

示例18 如何在Java 8中使用预定义的格式器来对日期进行解析/格式化

在Java 8之前,时间日期的格式化可是个技术活,我们的好伙伴SimpleDateFormat并不是线程安全的,而如果用作本地变量来格式化的话又显得有些笨重。多亏了线程本地变量,这使得它在多线程环境下也算有了用武之地,但Java维持这一状态也有很长一段时间了。这次它引入了一个全新的线程安全的日期与时间格式器。它还自带了一些预定义好的格式器,包含了常用的日期格式。比如说,本例 中我们就用了预定义的BASICISODATE格式,它会将2014年2月14日格式化成20140114。

String dayAfterTommorrow = "20140116";
  
LocalDate formatted = LocalDate.parse(dayAfterTommorrow,
  
DateTimeFormatter.BASIC_ISO_DATE);
  
System.out.printf("Date generated from String %s is %s %n", dayAfterTommorrow, formatted);

Output :
  
Date generated from String 20140116 is 2014-01-16
  
你可以看到生成的日期与指定字符串的值是匹配的,就是日期格式上略有不同。

示例19 如何在Java中使用自定义的格式器来解析日期

在上例中,我们使用了内建的时间日期格式器来解析日期字符串。当然了,预定义的格式器的确不错但有时候你可能还是需要使用自定义的日期格式,这个时候你就得自己去创建一个自定义的日期格式器实例了。下面这个例子中的日期格式是"MMM dd yyyy"。你可以给DateTimeFormatter的ofPattern静态方法()传入任何的模式,它会返回一个实例,这个模式的字面量与前例中是相同的。比如说M还是代表月,而m仍是分。无效的模式会抛出DateTimeParseException异常,但如果是逻辑上的错误比如说该用M的时候用成m,这样就没办法了。

String goodFriday = "Apr 18 2014";
  
try {
      
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM dd yyyy");
      
LocalDate holiday = LocalDate.parse(goodFriday, formatter);
      
System.out.printf("Successfully parsed String %s, date is %s%n", goodFriday, holiday);
  
} catch (DateTimeParseException ex) {
      
System.out.printf("%s is not parsable!%n", goodFriday);
      
ex.printStackTrace();
  
}

Output :
  
Successfully parsed String Apr 18 2014, date is 2014-04-18
  
可以看到日期的值与传入的字符串的确是相符的,只是格式不同。

示例20 如何在Java 8中对日期进行格式化,转换成字符串

在上两个例子中,尽管我们用到了DateTimeFormatter类但我们主要是进行日期字符串的解析。在这个例子中我们要做的事情正好相反。这里我们有一个LocalDateTime类的实例,我们要将它转换成一个格式化好的日期串。这是目前为止Java中将日期转换成字符串最简单便捷的方式了。下面这个例子将会返回一个格式化好的字符串。与前例相同的是,我们仍需使用指定的模式串去创建一个DateTimeFormatter类的实例,但调用的并不是LocalDate类的parse方法,而是它的format()方法。这个方法会返回一个代表当前日期的字符串,对应的模式就是传入的DateTimeFormatter实例中所定义好的。

LocalDateTime arrivalDate = LocalDateTime.now();
  
try {
      
DateTimeFormatter format = DateTimeFormatter.ofPattern("MMM dd yyyy hh:mm a");
      
String landing = arrivalDate.format(format);
      
System.out.printf("Arriving at : %s %n", landing);
      
} catch (DateTimeException ex) {
      
System.out.printf("%s can't be formatted!%n", arrivalDate);
      
ex.printStackTrace();
  
}

Output : Arriving at : Jan 14 2014 04:33 PM
  
可以看到,当前时间是用给定的"MMM dd yyyy hh:mm a"模式来表示的,它包含了三个字母表示的月份以及用AM及PM来表示的时间。

Java 8中日期与时间API的几个关键点

看完了这些例子后,我相信你已经对Java 8这套新的时间日期API有了一定的了解了。现在我们来回顾下关于这个新的API的一些关键的要素。

它提供了javax.time.ZoneId用来处理时区。
  
它提供了LocalDate与LocalTime类
  
Java 8中新的时间与日期API中的所有类都是不可变且线程安全的,这与之前的Date与Calendar API中的恰好相反,那里面像java.util.Date以及SimpleDateFormat这些关键的类都不是线程安全的。
  
新的时间与日期API中很重要的一点是它定义清楚了基本的时间与日期的概念,比方说,瞬时时间,持续时间,日期,时间,时区以及时间段。它们都是基于ISO日历体系的。
  
每个Java开发人员都应该至少了解这套新的API中的这五个类: 
  
Instant 它代表的是时间戳,比如2014-01-14T02:20:13.592Z,这可以从java.time.Clock类中获取,像这样:  Instant current = Clock.system(ZoneId.of("Asia/Tokyo")).instant();
  
LocalDate 它表示的是不带时间的日期,比如2014-01-14。它可以用来存储生日,周年纪念日,入职日期等。
  
LocalTime – 它表示的是不带日期的时间
  
LocalDateTime – 它包含了时间与日期,不过没有带时区的偏移量
  
ZonedDateTime – 这是一个带时区的完整时间,它根据UTC/格林威治时间来进行时区调整
  
这个库的主包是java.time,里面包含了代表日期,时间,瞬时以及持续时间的类。它有两个子package,一个是java.time.foramt,这个是什么用途就很明显了,还有一个是java.time.temporal,它能从更低层面对各个字段进行访问。
  
时区指的是地球上共享同一标准时间的地区。每个时区都有一个唯一标识符,同时还有一个地区/城市(Asia/Tokyo)的格式以及从格林威治时间开始的一个偏移时间。比如说,东京的偏移时间就是+09:00。
  
OffsetDateTime类实际上包含了LocalDateTime与ZoneOffset。它用来表示一个包含格林威治时间偏移量 (+/-小时: 分,比如+06:00或者 -08: 00) 的完整的日期 (年月日) 及时间 (时分秒,纳秒) 。
  
DateTimeFormatter类用于在Java中进行日期的格式化与解析。与SimpleDateFormat不同,它是不可变且线程安全的,如果需要的话,可以赋值给一个静态变量。DateTimeFormatter类提供了许多预定义的格式器,你也可以自定义自己想要的格式。当然了,根据约定,它还有一个parse()方法是用于将字符串转换成日期的,如果转换期间出现任何错误,它会抛出DateTimeParseException异常。类似的,DateFormatter类也有一个用于格式化日期的format()方法,它出错的话则会抛出DateTimeException异常。
  
再说一句,"MMM d yyyy"与"MMm dd yyyy"这两个日期格式也略有不同,前者能识别出"Jan 2 2014″与"Jan 14 2014″这两个串,而后者如果传进来的是"Jan 2 2014″则会报错,因为它期望月份处传进来的是两个字符。为了解决这个问题,在天为个位数的情况下,你得在前面补0,比如"Jan 2 2014″应该改为"Jan 02 2014″。
  
关于Java 8这个新的时间日期API就讲到这了。这几个简短的示例 对于理解这套新的API中的一些新增类已经足够了。由于它是基于实际任务来讲解的,因此后面再遇到Java中要对时间与日期进行处理的工作时,就不用再四处寻找了。我们学习了如何创建与修改日期实例。我们还了解了纯日期,日期加时间,日期加时区的区别,知道如何比较两个日期,如何找到某天到指定日期比如说下一个生日,周年纪念日或者保险日还有多少天。我们还学习了如何在Java 8中用线程安全的方式对日期进行解析及格式化,而无需再使用线程本地变量或者第三方库这种取巧的方式。新的API能胜任任何与时间日期相关的任务。
  
英文原文链接

  1. Instant 与 Duration

1) Instant表示某一个时间点的时间戳,可以类比于java.uti.Date。支持各种运算操作: 

Instant begin = Instant.now();
  
begin.plus(5, ChronoUnit.SECONDS);
  
begin.minusMillis(50);
  
begin.isBefore(Instant.now());

begin.toEpochMilli();
  
2) Duration表示Instant之间的时间差,可以用来统计任务的执行时间,也支持各种运算操作,比如: 

Instant begin = Instant.now();
  
// do some work
  
Instant end = Instant.now();
  
Duration elapsed = Duration.between(begin, end);
  
elapsed.toMillis()

elapsed.dividedBy(10).minus(Duration.ofMillis(10)).isNegative();
  
elapsed.isZero();
  
elapsed.plusHours(3);
  
2. LocalDate 与 Period

1) LocalDate用于表示日期,与时区(TimeZone)无关。

创建LocalDate: 

LocalDate now = LocalDate.now();
  
LocalDate today = LocalDate.of(2016, 1, 31);
  
LocalDate today2 = LocalDate.of(2016, Month.JANUARY, 31); // JANUARY = 1, ..., DECEMBER = 12
  
支持的操作: 

today2.getDayOfWeek().getValue(); // Monday = 1, ..., Sunday = 7
  
LocalDate dayOfYear = Year.now().atDay(220);
  
YearMonth april = Year.of(2016).atMonth(Month.APRIL);
  
注意,有些操作得到的日期可能是不存在的,比如2016-01-31增加1个月后为2016-02-31,该日期是不存在的,返回值为该月的最后一天,即2016-02-29:

LocalDate nextMonth = LocalDate.of(2016, 1, 31).plusMonths(1); // 2016-02-29
  
2) Period用来表示两个LocalDate之间的时间差,支持各种运算操作: 

LocalDate fiveDaysLater = LocalDate.now().plusDays(5);
  
Period period = LocalDate.now().until(fiveDaysLater).plusMonths(2);
  
period.isNegative();
  
3) TemporalAdjusters用于表示某个月第一天、下个周一等日期: 

LocalDate.now().with(TemporalAdjusters.firstDayOfMonth());
  
LocalDate.now().with(TemporalAdjusters.lastInMonth(DayOfWeek.SUNDAY));
  
LocalDate.now().with(TemporalAdjusters.nextOrSame(DayOfWeek.MONDAY));
  
3. LocalTime

1) LocalTime表示时间,没有日期,与时区(TimeZone)无关: 

LocalTime.now().isBefore(LocalTime.of(16, 2, 1));
  
LocalTime.now().plusHours(2).getHour();
  
2) LocalDateTime表示日期和时间,适用于时区固定不变的场合(LocalDateTime使用系统默认的时区),如果需要根据时区调整日期和时间,应该使用ZonedDateTime:

LocalDateTime.now().plusDays(3).minusHours(5).isAfter(LocalDateTime.of(2016, 1, 30, 10, 20, 30));
  
4. ZonedDateTime

1) ZonedDateTime表示带时区的日期和时间,支持的操作与LocalDateTime非常类似: 

Set<String> zones = ZoneId.getAvailableZoneIds();
  
ZonedDateTime.now(ZoneId.of("Asia/Shanghai")).plusMonths(1).minusHours(3)
      
.isBefore(ZonedDateTime.now());
  
2) ZonedDateTime与LocalDateTime、Instant之间可以相互转换: 

ZonedDateTime nowOfShanghai = LocalDateTime.now().atZone(ZoneId.of("Asia/Shanghai"));
  
ZonedDateTime.now(ZoneId.of("UTC")).toLocalDate();
  
ZonedDateTime nowOfShanghai2 = Instant.now().atZone(ZoneId.of("Asia/Shanghai"));
  
ZonedDateTime.of(LocalDate.now(), LocalTime.now(), ZoneId.of("UTC")).toInstant();
  
5. Formatting 与 Parsing

1) 要格式化或者解析日期时,需要使用到DateTimeFormatter,用来定义日期或时间的格式: 

// 2016-01-31T15:39:31.481
  
DateTimeFormatter.ISO_LOCAL_DATE_TIME.format(LocalDateTime.now());
  
// Jan 31, 2016 3:50:04 PM
  
DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM).format(LocalDateTime.now());
  
// Sun 2016-01-31 15:50:04
  
DateTimeFormatter.ofPattern("E yyyy-MM-dd HH:mm:ss").format(LocalDateTime.now());

LocalDateTime.parse("2016-01-31 15:51:00-0400",
      
DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ssxx"));
  
LocalDate.parse("2016-01-31");
  
2) 日期和时间格式化的常见格式: 

年 yy: 16 yyyy: 2016
  
月 M: 1 MM: 01
  
日 d: 3 dd: 03
  
周 e: 3 E: Web
  
时 H: 9 HH: 09
  
钟 mm: 02
  
秒 ss: 00
  
纳秒 nnnnnn:000000
  
时区偏移 x: -04 xx:-0400

  1. 前言: 
  
    时间格式: 

//世界标准时间,其中T表示时分秒的开始 (或者日期与时间的间隔) ,Z表示这是一个世界标准时间
  
2017-12-13T01:47:07.081Z

//本地时间,也叫不含时区信息的时间,末尾没有Z
  
2017-12-13T09:47:07.153

//含有时区信息的时间,+08:00表示该时间是由世界标准时间加了8个小时得到的,[Asia/Shanghai]表示时区
  
2017-12-13T09:47:07.153+08:00[Asia/Shanghai]
  
其中最难理解的是本地时间,2017-12-13T09:47:07.153时间本身是不含有时区信息的,但是"本地"这两个字含有时间信息。所以我认为这个翻译并不好,不应该叫做"本地时间",应该直接翻译为"不含时区信息的时间"。

协调世界时,又称世界统一时间、世界标准时间、国际协调时间。由于英文(CUT)和法文(TUC)的缩写不同,作为妥协,简称UTC。
  
世界时UT即格林尼治平太阳时间,是指格林尼治所在地的标准时间,也是表示地球自转速率的一种形式。以地球自转为基础的时间计量系统。

  1. 先来看Java8: 
  
    表示时间的主要有4类String、Instant、LocalDateTime、ZonedDateTime。

String是格式化的时间,Instant是时间戳,LocalDateTime是不含时区信息的时间,ZonedDateTime是含有时区信息的时间。

1.1 它们之间的关系是: 
  
1.1.1 String与LocalDateTime是等价的
  
符合格式的String可以直接解析为LocalDateTime,如下: 

System.out.println(LocalDateTime.parse("2017-12-13 10:10:10",DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));

输出: 
  
2017-12-13T10:10:10
  
辨析LocalDateTime最好的办法就是不要把它当成"本地时间",它就是"不含时区信息的时间"。它只是存储了年月日时分秒,没有存储任何时区信息,具体表示哪里的时间全靠输入和输出时进行解释。与String完全等价,本质上是对String的解析,只是年月日时分秒格式化的存储到了对象当中,方便取用。

1.1.2 Instant与ZonedDateTime是等价的
  
Instant是时间戳,是指世界标准时格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数,Instant本身实际上就指明时区了,0时区。
  
ZonedDateTime是含有时区信息的时间,本质上是根据时区对Instant的格式化显示。

ZonedDateTime ztime1=ZonedDateTime.ofInstant(Instant.now(),ZoneId.systemDefault());
  
System.out.println(ztime1);
  
System.out.println(ztime1.toInstant()); //1
  
System.out.println(ztime1.toLocalDateTime()); //3
  
ZonedDateTime ztime2=ZonedDateTime.ofInstant(Instant.now(),ZoneId.of("Australia/Darwin"));
  
System.out.println(ztime2);
  
System.out.println(ztime2.toInstant()); //2
  
System.out.println(ztime2.toLocalDateTime()); //4

输出: 
  
2017-12-13T13:24:55.932+08:00[Asia/Shanghai]
  
2017-12-13T05:24:55.932Z
  
2017-12-13T13:24:55.932
  
2017-12-13T14:54:55.933+09:30[Australia/Darwin]
  
2017-12-13T05:24:55.933Z
  
2017-12-13T14:54:55.933
  
注释1、2输出相同,说明ZonedDateTime的存储本质是Instant；
  
注释3、4输出不同,说明ZonedDateTime会根据创建ZonedDateTime对象时传入的时区,进行格式化显示。

相同的Instant,在不同的时区有不同的展示时间,所以在用Instant构造ZonedDateTime的时候需要传入时区；ZonedDateTime可以直接转化为Instant,并且不同的ZonedDateTime可能会生成同样的Instant。

1.2 如何构造时间对象: 
  
1.2.1 直接定义
  
System.out.println(Instant.ofEpochMilli(System.currentTimeMillis()));
  
System.out.println(LocalDateTime.of(2017,12,13,10,0,0,0));
  
System.out.println(ZonedDateTime.of(2017,12,13,10,0,0,0,ZoneId.systemDefault()));

输出: 
  
2017-12-13T06:22:06.581Z
  
2017-12-13T10:00
  
2017-12-13T10:00+08:00[Asia/Shanghai]
  
1.2.2 获取系统当前时间now()
  
System.out.println(Instant.now()); //世界标准时间
  
System.out.println(LocalDateTime.now()); //会把世界标准时间转换为本时区的时间,但是时区信息会被丢弃
  
System.out.println(ZonedDateTime.now()); //会把世界标准时间转换为本时区的时间,但是时区信息会被保留

System.out.println(LocalDateTime.now(ZoneId.of("+00:00"))); //0时区的现在时间
  
System.out.println(ZonedDateTime.now(ZoneId.of("+00:00"))); //0时区的现在时间

输出: 
  
2017-12-14T02:53:05.830Z
  
2017-12-14T10:53:05.904
  
2017-12-14T10:53:05.906+08:00[Asia/Shanghai]
  
2017-12-14T02:53:05.906
  
2017-12-14T02:53:05.906Z
  
1.2.3 解析String
  
System.out.println(Instant.parse("2007-12-03T10:15:30Z")); //只能解析这种格式,不能自己指定
  
System.out.println(LocalDateTime.parse("2017-12-13 11:51:12.083", DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS")));
  
System.out.println(ZonedDateTime.parse("2017-12-13 11:51:12.083 +04:30", DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS ZZZZZ")));

输出: 
  
2007-12-03T10:15:30Z
  
2017-12-13T11:51:12.083
  
2017-12-13T11:51:12.083+04:30
  
1.3 时间对象之间的转换: 
  
1.3.1 Instant与LocalDateTime、ZonedDateTime之间的转换
  
Instant instant=Instant.now();
  
LocalDateTime localDateTime=LocalDateTime.ofInstant(instant,ZoneId.systemDefault());
  
ZonedDateTime zonedDateTime=ZonedDateTime.ofInstant(instant,ZoneId.systemDefault());

System.out.println(instant);
  
System.out.println(localDateTime);
  
System.out.println(zonedDateTime);

System.out.println(ZoneOffset.systemDefault());
  
System.out.println(ZoneOffset.UTC);
  
System.out.println(ZoneOffset.MIN);
  
System.out.println(ZoneOffset.of("+08:00"));
  
System.out.println(localDateTime.toInstant(ZoneOffset.UTC)); //在把LocalDateTime转换为Instant时,需要明确指定当前这个时间指的是那个时区的时间
  
System.out.println(localDateTime.toInstant(ZoneOffset.of("+08:00")));
  
System.out.println(zonedDateTime.toInstant());

输出: 
  
2017-12-14T01:50:26.098Z
  
2017-12-14T09:50:26.098
  
2017-12-14T09:50:26.098+08:00[Asia/Shanghai]
  
Asia/Shanghai
  
Z
  
-18:00
  
+08:00
  
2017-12-14T09:50:26.098Z
  
2017-12-14T01:50:26.098Z
  
2017-12-14T01:50:26.098Z
  
1.3.2 LocalDateTime、ZonedDateTime之间的转换
  
Instant instant=Instant.now();
  
LocalDateTime localDateTime=LocalDateTime.ofInstant(instant,ZoneId.systemDefault());
  
ZonedDateTime zonedDateTime=ZonedDateTime.ofInstant(instant,ZoneId.systemDefault());

System.out.println(instant);
  
System.out.println(localDateTime);
  
System.out.println(zonedDateTime);

System.out.println(ZonedDateTime.of(localDateTime,ZoneId.systemDefault())); //LocalDateTime转ZonedDateTime
  
System.out.println(zonedDateTime.toLocalDateTime()); //ZonedDateTime转LocalDateTime

输出: 
  
2017-12-14T02:01:45.145Z
  
2017-12-14T10:01:45.145
  
2017-12-14T10:01:45.145+08:00[Asia/Shanghai]
  
2017-12-14T10:01:45.145+08:00[Asia/Shanghai]
  
2017-12-14T10:01:45.145
  
1.4 时区之间的转换
  
时区转换时要特别注意的是: 用户输入的String类型的时间是没有时区信息的,需要人为指定解析。
  
解析的步骤分2步: 

先结合语境,分析用户时区,把用户输入的时间转化为世界标准时间；
  
再把世界标准时间转为需要的时区。
  
1.5 关于时间的陷阱
  
1.5.1 问题
  
因为存在时区的概念,所以会造成2个问题: 

不同时区的用户,对时间的理解不同,不同时区的同一个时间String不是同一个时间戳；
  
不同时区的服务器,对时间的理解也不同,比如,同一份程序运行在不同时区的服务器上,当这些程序同时调用LocalDateTime.now()时,返回的结果并不同,如果操作不当很容易出现问题；
  
如果前台和后台程序分别部署在不同时区的服务器上,情况会更加复杂。如果用户、前台和后台程序都不在相同时区,……。
  
1.5.2 解决办法
  
建议在系统当中统一使用时间戳,包括前后台传输和数据库存储,只有在展示的时候再转化为字符串；
  
如果为了处理方便建议把所有的时间都转化到0时区进行处理。
  
2. Java8以前的时间API
  
JAVA API系列--日期和时间相关的类
  
【总结】java.util.Date vs. java.sql.Date
  
java.util.Date、java.sql.Date、java.sql.Time、java.sql.Timestamp区别和总结
  
时区转换: java new Date() 变成GMT&& GMT时间与CST时间转换

2.1 Date与时区
  
Date对象中,有一个默认时区,取得是操作系统的默认时区。可以通过下面的代码进行修改: 

TimeZone.setDefault(TimeZone.getTimeZone("GMT")); // 将默认时区转化为GMT时区
  
TimeZone.setDefault(TimeZone.getTimeZone("Asia/Shanghai"));// 将默认时区转化为东八区时区
  
3. 新旧时间API的转换
  
新旧时间API连接的桥梁是Date类和Instant类,这两个都是世界标准时间,但是Date打印的时候会转化为本地时间。

Date date=Date.from(Instant.now());
  
Instant instant=date.toInstant();
  
System.out.println(date);
  
System.out.println(date.getTime()); //1
  
System.out.println(instant);
  
System.out.println(instant.toEpochMilli()); //2

输出: 
  
Thu Dec 14 11:45:58 CST 2017
  
1513223158588
  
2017-12-14T03:45:58.588Z
  
1513223158588
  
注释1、2输出相同,说明Date类和Instant类是等价的；

后台接口中的时间参数
5.1 无配置接收
yyyy-[m]m-[d]d hh:mm:ss[.f…]
可以使用java.sql.Timestamp接收
yyyy-[m]m-[d]d
可以使用java.sql.Date接收
Sat, 12 Aug 1995 13:30:00 GMT
可以使用java.util.Date接收
5.2 有配置接收
自己编写convert类,并注册到spring框架中
参见: 
[1] springboot Date解析String类型的参数
[2] @DateTimeFormat格式化JSON日期时间(Date或timestamp)无效的原因 / Spring格式化json日期时间(Date或timestamp)的方法

5.3 自定义时间类
  
自己编写可以作为参数的时间类
  
参见: Annotation Type QueryParam

被@QueryParam注解的参数,必须满足一下条件中的一个: 

原始类型
  
有一个构造函数接受一个String参数
  
有一个名为valueOf或fromString的静态方法,它接受一个String参数(例如,参见Integer.valueOf(String))
  
列表< T>,< T>或SortedSet T,其中T满足上述2或3。生成的集合是只读的。
  
————————————————
  
版权声明: 本文为CSDN博主「frcoder」的原创文章,遵循 CC 4.0 BY-SA 版权协议,转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/u012107143/java/article/details/78790378

介绍java 8 的 Period 和 Duration 类
  
本文我们学习java 8 中引入的两个与日期相关的新类: Period 和 Duration。两个类看表示时间量或两个日期之间的差,两者之间的差异为: Period基于日期值,而Duration基于时间值。

Period 类
  
Period 类表示一段时间的年、月、日,开使用between()方法获取两个日期之间的差作为Period 对象返回: 

LocalDate startDate = LocalDate.of(2015, 2, 20);
  
LocalDate endDate = LocalDate.of(2017, 1, 15);

Period period = Period.between(startDate, endDate);
  
然后,我们或从Period对象中货位日期单元,使用getYears(),getMonhs(),getDays()方法:

LOG.info("Years:" + period.getYears() +
    
" months:" + period.getMonths() +
    
" days:"+period.getDays());
  
这种情况下,任何一个时间单元为负数,则isNegative()方法返回true,因此可以用于判断endDate是否大于startDate: 

assertFalse(period.isNegative());
  
如果isNegative()返回false,那么startDate早于endDate。

另一个创建Period类型对象是基于年、月、日和周,通过下面方法: 

Period fromUnits = Period.of(3, 10, 10);
  
Period fromDays = Period.ofDays(50);
  
Period fromMonths = Period.ofMonths(5);
  
Period fromYears = Period.ofYears(10);
  
Period fromWeeks = Period.ofWeeks(40);

assertEquals(280, fromWeeks.getDays());
  
如果仅一个值表示,如使用ofDays()方法,那么其他值为0；当使用ofWeeks()方法时,则其参数值可以设置天数为参数乘以7。

我们也可以通过解析文本序列来创建Period,其格式为"PnYnMnD":

Period fromCharYears = Period.parse("P2Y");
  
assertEquals(2, fromCharYears.getYears());

Period fromCharUnits = Period.parse("P2Y3M5D");
  
assertEquals(5, fromCharUnits.getDays());
  
period的值可以通过plusX()、minusX()方法进行增加或减少,其中X表示日期单元: 

assertEquals(56, period.plusDays(50).getDays());
  
assertEquals(9, period.minusMonths(2).getMonths());
  
Duration 类
  
Duration类表示秒或纳秒时间间隔,适合处理较短的时间,需要更高的精确性。我们能使用between()方法比较两个瞬间的差: 

Instant start = Instant.parse("2017-10-03T10:15:30.00Z");
  
Instant end = Instant.parse("2017-10-03T10:16:30.00Z");

Duration duration = Duration.between(start, end);
  
那么我们能使用getSeconds() 或 getNanoseconds() 方法获取时间单元的值: 

assertEquals(60, duration.getSeconds());
  
我们也可以通过LocalDateTime 类获取获取Duration对象: 

LocalTime start = LocalTime.of(1, 20, 25, 1024);
  
LocalTime end = LocalTime.of(3, 22, 27, 1544);

Duration.between(start, end).getSeconds();
  
isNegative()方法能用于验证后面时间是否大于前面时间: 

assertFalse(duration.isNegative());
  
我们能基于下面的方法获得Duration对象,ofDays(), ofHours(), ofMillis(), ofMinutes(), ofNanos(), ofSeconds():

Duration fromDays = Duration.ofDays(1);
  
assertEquals(86400, fromDays.getSeconds());

Duration fromMinutes = Duration.ofMinutes(60);
  
当然也可以通过文本序列创建Duration对象,格式为 "PnDTnHnMn.nS":

Duration fromChar1 = Duration.parse("P1DT1H10M10.5S");
  
Duration fromChar2 = Duration.parse("PT10M");

可以使用toDays(), toHours(), toMillis(), toMinutes()方法把Duration对象可以转成其他时间单元: 

assertEquals(1, fromMinutes.toHours());
  
也可以通过 plusX()、minusX()方法增加或减少Duration对象,其中X表示days, hours, millis, minutes, nanos 或 seconds:

assertEquals(120, duration.plusSeconds(60).getSeconds());
  
assertEquals(30, duration.minusSeconds(30).getSeconds());
  
也可以使用plus()和minus()方法带TemporalUnit 类型参数进行加减: 

assertEquals(120, duration.plus(60, ChronoUnit.SECONDS).getSeconds());
  
assertEquals(30, duration.minus(30, ChronoUnit.SECONDS).getSeconds());
  
总结
  
本文我们介绍了java 8 中Period 和 Duration类,并通过实例介绍了其常用方法。


版权声明: 本文为CSDN博主「neweastsun」的原创文章,遵循 CC 4.0 BY-SA 版权协议,转载请附上原文出处链接及本声明。  
原文链接: https://blog.csdn.net/neweastsun/java/article/details/88770592  
http://www.importnew.com/15637.html  
https://nkcoder.github.io/2016/01/31/java-8-date-time-api/  
https://my.oschina.net/kolbe/blog/507974  
<https://blog.csdn.net/u012107143/java/article/details/78790378>  

版权声明: 本文为CSDN博主「sy793314598」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/sy793314598/java/article/details/79544796

