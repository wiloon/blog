---
title: date command
author: "-"
date: 2018-06-20T07:38:39+00:00
url: date
categories:
  - linux
tags:
  - command
  - reprint
  - remix


---
## date command

    date [OPTION]... [+FORMAT]

### 日期格式化
    date '+%Y-%m-%d %H:%M:%S'

## 纳秒，毫秒
使用 date +%s%N 可以获得一个纳秒级的unix时间戳(当前时间)，然后根据需要截取一部分即可得到毫秒级的精度
```bash
# 纳秒
date +%s%N
# 毫秒
$(($(date +%s%N)/1000000))
# 毫秒, 另外一种作废的不再建议使用的语法
echo $[$(date +%s%N)/1000000]
```

## 参数

    %s     seconds since 1970-01-01 00:00:00 UTC
    %N     nanoseconds (000000000..999999999)

```bash
# output date and time in RFC 5322 format.  Example: Mon, 14 Aug 2006 02:34:56 -0600
date -R

# 设置时间和日期
sudo date -s "04/12/2019 09:03:00"
sudo date -s "2019-04-12 09:04:00"

# 将系统日期设定成2009年11月3日的命令
date -s 11/03/2009

# 将系统时间设定成下午5点55分55秒的命令
date -s 17:55:55
```

>http://jerrybear.blog.51cto.com/629421/393097
>https://blog.csdn.net/BalterNotz/article/details/52949493

BASH SHELL中可以定义变量显示当前日期

显示当前日期是

DATE=`date +%Y%m%d` +号后面是定义格式为年月日

显示前一天为

DATE1=`date -d '1 days ago' +%Y%m%d` 加-d参数可以设置与当前日期的计算时间,同样,前2天为'2 days ago',去掉ago则为当前日期之后多少天

以下内容就是网上看到的一篇不错的文章,出自http://www.labri.fr/perso/strandh/Teaching/USI/Common/Sh-utils/sh-utils_65.html

Here are a few examples. Also see the documentation for the \`-d' option in the previous section.

To print the date of the day before yesterday:
  
date -date='2 days ago'
  
To print the date of the day three months and one day hence:
  
date -date='3 months 1 day'
  
To print the day of year of Christmas in the current year:
  
date -date='25 Dec' +%j
  
To print the current full month name and the day of the month:
  
date '+%B %d'
  
But this may not be what you want because for the first nine days of the month, the `%d' expands to a zero-padded two-digit field, for example`date -d 1may '+%B %d" will print `May 01'.

To print a date without the leading zero for one-digit days of the month, you can use the (GNU extension) - modifier to suppress the padding altogether.

date -d=1may '+%B %-d'

To print the current date and time in the format required by many non-GNU versions of date when setting the system clock:

date +%m%d%H%M%Y.%S

To set the system clock forward by two minutes:

date --set='+2 minutes'

To print the date in the format specified by RFC-822, use`date -rfc'. I just did and saw this:
  
Mon, 25 Mar 1996 23:34:17 -0600
  
To convert a date string to the number of seconds since the epoch (which is 1970-01-01 00:00:00 UTC), use the `--date' option with the`%s' format. That can be useful in sorting and/or graphing and/or comparing data by date. The following command outputs the number of the seconds since the epoch for the time one second later than the epoch, but in time zone five hours later (Cambridge, Massachusetts), thus a total of five hours and one second after the epoch:
  
date -date='1970-01-01 00:00:01 UTC +5 hours' +%s
  
18001
  
Suppose you had not specified time zone information in the example above. Then, date would have used your computer's idea of the time zone when interpreting the string. Here's what you would get if you were in Greenwich, England:

# local time zone used

date -date='1970-01-01 00:00:01' +%s
  
If you're sorting or graphing dated data, your raw date values may be represented as seconds since the epoch. But few people can look at the date \`946684800' and casually note "Oh, that's the first second of the year 2000."
  
date -date='2000-01-01 UTC' +%s
  
946684800
  
To convert such an unwieldy number of seconds back to a more readable form, use a command like this:
  
date -d '1970-01-01 946684800 sec' +"%Y-%m-%d %T %z"
  
2000-01-01 00:00:00 +0000

---

https://blog.csdn.net/shanliangliuxing/article/details/16821175
>https://man7.org/linux/man-pages/man1/date.1.html