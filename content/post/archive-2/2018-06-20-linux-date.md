---
title: linux date
author: wiloon
type: post
date: 2018-06-20T07:38:39+00:00
url: /?p=12334
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers"># output date and time in RFC 5322 format.  Example: Mon, 14 Aug 2006 02:34:56 -0600
date -R

# 设置时间和日期
sudo date -s "04/12/2019 09:03:00"
sudo date -s "2019-04-12 09:04:00"

# 将系统日期设定成2009年11月3日的命令
date -s 11/03/2009

# 将系统时间设定成下午5点55分55秒的命令
date -s 17:55:55
</code></pre>

http://jerrybear.blog.51cto.com/629421/393097
  
https://blog.csdn.net/BalterNotz/article/details/52949493

BASH SHELL中可以定义变量显示当前日期

显示当前日期是

DATE=`date +%Y%m%d` +号后面是定义格式为年月日

显示前一天为

DATE1=`date -d '1 days ago' +%Y%m%d` 加-d参数可以设置与当前日期的计算时间，同样，前2天为&#8217;2 days ago&#8217;，去掉ago则为当前日期之后多少天

以下内容就是网上看到的一篇不错的文章，出自http://www.labri.fr/perso/strandh/Teaching/USI/Common/Sh-utils/sh-utils_65.html

Here are a few examples. Also see the documentation for the \`-d&#8217; option in the previous section.

To print the date of the day before yesterday:
  
date &#8211;date=&#8217;2 days ago&#8217;
  
To print the date of the day three months and one day hence:
  
date &#8211;date=&#8217;3 months 1 day&#8217;
  
To print the day of year of Christmas in the current year:
  
date &#8211;date=&#8217;25 Dec&#8217; +%j
  
To print the current full month name and the day of the month:
  
date &#8216;+%B %d&#8217;
  
But this may not be what you want because for the first nine days of the month, the `%d' expands to a zero-padded two-digit field, for example`date -d 1may &#8216;+%B %d&#8221; will print `May 01'.<br />
To print a date without the leading zero for one-digit days of the month, you can use the (GNU extension) - modifier to suppress the padding altogether.<br />
date -d=1may '+%B %-d'<br />
To print the current date and time in the format required by many non-GNU versions of date when setting the system clock:<br />
date +%m%d%H%M%Y.%S<br />
To set the system clock forward by two minutes:<br />
date --set='+2 minutes'<br />
To print the date in the format specified by RFC-822, use`date &#8211;rfc&#8217;. I just did and saw this:
  
Mon, 25 Mar 1996 23:34:17 -0600
  
To convert a date string to the number of seconds since the epoch (which is 1970-01-01 00:00:00 UTC), use the `--date' option with the`%s&#8217; format. That can be useful in sorting and/or graphing and/or comparing data by date. The following command outputs the number of the seconds since the epoch for the time one second later than the epoch, but in time zone five hours later (Cambridge, Massachusetts), thus a total of five hours and one second after the epoch:
  
date &#8211;date=&#8217;1970-01-01 00:00:01 UTC +5 hours&#8217; +%s
  
18001
  
Suppose you had not specified time zone information in the example above. Then, date would have used your computer&#8217;s idea of the time zone when interpreting the string. Here&#8217;s what you would get if you were in Greenwich, England:

# local time zone used

date &#8211;date=&#8217;1970-01-01 00:00:01&#8242; +%s
  
1
  
If you&#8217;re sorting or graphing dated data, your raw date values may be represented as seconds since the epoch. But few people can look at the date \`946684800&#8242; and casually note &#8220;Oh, that&#8217;s the first second of the year 2000.&#8221;
  
date &#8211;date=&#8217;2000-01-01 UTC&#8217; +%s
  
946684800
  
To convert such an unwieldy number of seconds back to a more readable form, use a command like this:
  
date -d &#8216;1970-01-01 946684800 sec&#8217; +&#8221;%Y-%m-%d %T %z&#8221;
  
2000-01-01 00:00:00 +0000