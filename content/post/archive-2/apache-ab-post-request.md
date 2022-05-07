---
title: apache ab/Apache Bench
author: "-"
date: 2015-12-25T11:47:19+00:00
url: /?p=8602
categories:
  - Inbox
tags:
  - reprint
---
## apache ab/Apache Bench
ApacheBench

### install

```bash
yay -S apache-tools
sudo yum -y install httpd-tools
```

```bash格式: ab [options] [http://]hostname[:port]/path

# get 请求, 不带 -p参数时  发get请求
ab -n 1 -c 1   -T 'application/x-www-form-urlencoded' "http://127.0.0.1:7000/"
#post 请求
ab -n 1 -c 1 -p abpost.txt -T 'application/x-www-form-urlencoded' "http://127.0.0.1:7000/"
ab -n 1 -c 1 -p abpost.txt -T 'application/json' "http://127.0.0.1:8080/"
```

参数: 
  
-n requests Number of requests to perform
  
//在测试会话中所执行的请求个数 (本次测试总共要访问页面的次数) 。默认时,仅执行一个请求。

-c concurrency Number of multiple requests to make
  
//一次产生的请求个数 (并发数) 。默认是一次一个。

-t timelimit Seconds to max. wait for responses
  
//测试所进行的最大秒数。其内部隐含值是-n 50000。它可以使对服务器的测试限制在一个固定的总时间以内。默认时,没有时间限制。

-p postfile File containing data to POST
  
//包含了需要POST的数据的文件,文件格式如"p1=1&p2=2".使用方法是 -p 111.txt 。  (配合-T) 

-T content-type Content-type header for POSTing
  
//POST数据所使用的Content-type头信息,如 -T "application/x-www-form-urlencoded" 。  (配合-p) 

-v verbosity How much troubleshooting info to print
  
//设置显示信息的详细程度 – 4或更大值会显示头信息, 3或更大值可以显示响应代码(404, 200等), 2或更大值可以显示警告和其他信息。 -V 显示版本号并退出。

-w Print out results in HTML tables
  
//以HTML表的格式输出结果。默认时,它是白色背景的两列宽度的一张表。

-i Use HEAD instead of GET
  
// 执行HEAD请求,而不是GET。

-x attributes String to insert as table attributes
  
-y attributes String to insert as tr attributes
  
-z attributes String to insert as td or th attributes
  
-C attribute Add cookie, eg. -C "c1=1234,c2=2,c3=3" (repeatable)
  
//-C cookie-name=value 对请求附加一个Cookie:行。 其典型形式是name=value的一个参数对。此参数可以重复,用逗号分割。
  
提示: 可以借助session实现原理传递 JSESSIONID参数, 实现保持会话的功能,如

-C " c1=1234,c2=2,c3=3, JSESSIONID=FF056CD16DA9D71CB131C1D56F0319F8″ 。
  
-H attribute Add Arbitrary header line, eg. 'Accept-Encoding: gzip' Inserted after all normal header lines. (repeatable)
  
-A attribute Add Basic WWW Authentication, the attributes
  
are a colon separated username and password.
  
-P attribute Add Basic Proxy Authentication, the attributes
  
are a colon separated username and password.
  
//-P proxy-auth-username:password 对一个中转代理提供BASIC认证信任。用户名和密码由一个:隔开,并以base64编码形式发送。无论服务器是否需要(即, 是否发送了401认证需求代码),此字符串都会被发送。
  
-X proxy:port Proxyserver and port number to use
  
-V Print version number and exit
  
-k Use HTTP KeepAlive feature
  
-d Do not show percentiles served table.
  
-S Do not show confidence estimators and warnings.
  
-g filename Output collected data to gnuplot format file.
  
-e filename Output CSV file with percentages served
  
-h Display usage information (this message)
  
//-attributes 设置属性的字符串. 缺陷程序中有各种静态声明的固定长度的缓冲区。另外,对命令行参数、服务器的响应头和其他外部输入的解析也很简单,这可能会有不良后果。它没有完整地实现 HTTP/1.x; 仅接受某些'预想'的响应格式。 strstr(3)的频繁使用可能会带来性能问题,即你可能是在测试ab而不是服务器的性能。

参数很多,一般我们用 -c 和 -n 参数就可以了。例如:

# ab -c 5000 -n 600 http://127.0.0.1/index.php

ApacheBench用法详解: 

在Linux系统,一般安装好Apache后可以直接执行；

# ab -n 4000 -c 1000 http://www.ha97.com/

如果是Win系统下,打开cmd命令行窗口,cd到apache安装目录的bin目录下；

-n后面的4000代表总共发出4000个请求；-c后面的1000表示采用1000个并发 (模拟1000个人同时访问) ,后面的网址表示测试的目标URL。

 

 

 

使用ab发送post请求

ab -n 100000 -c 149  -H keywords:dt -p  /root/file/param.conf  -T 'application/x-www-form-urlencoded'  http://cc-tt.chinacloudapp.cn/restaurant

解释: -p:包含post请求的参数文件。文件内容类似: sk=1babb55a0b4b4dd2a&apitype=restaurant&p=tJoLaT4mon

-T:content-type 。请求内容类型

n:总请求数

c:并发客户端数

H:自定义消息头

http://nanchengru.com/2015/01/apache-ab%E5%8F%91%E9%80%81post%E8%AF%B7%E6%B1%82%E4%BB%A5%E5%8F%8A%E5%8F%82%E6%95%B0%E8%A7%A3%E9%87%8A/?replytocom=9

 


  
     (总结) Web性能压力测试工具之ApacheBench (ab) 详解
  


http://www.ha97.com/4617.html/embed#?secret=uK0hS4Tawl

 