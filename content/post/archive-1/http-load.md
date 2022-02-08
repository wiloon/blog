---
title: http load
author: "-"
date: 2015-09-16T02:58:08+00:00
url: /?p=8265
categories:
  - Uncategorized

tags:
  - reprint
---
## http load
http://blog.chinaunix.net/uid-488742-id-2113649.html

http://www.acme.com/software/http_load/

Web测试工具 http_load 一个httpd 压力测试工具 2007-12-02 09:42:15
  
分类:  LINUX
  
到http://www.acme.com/software/http_load/ 下载http_load ,安装也很简单直接make;make instlall 就行。
  
http_load的标准的两个例子是: 
  
http_load -parallel 5 -fetches 1000 urls.txt
  
http_load -rate 2 -seconds 300 urls.txt
  
例子只是个参考,参数其实可以自由组合,参数之间的选择并没有什么限制。比如你写成http_load -parallel 5 -seconds 300 urls.txt也是可以的。我们把参数给大家简单说明一下。-parallel 简写-p : 含义是并发的用户进程数。
  
-fetches 简写-f : 含义是总计的访问次数
  
-rate    简写-p : 含义是每秒的访问频率

-seconds简写-s : 含义是总计的访问时间

urls.txt 是一个url 列表,每个url 单独的一行。当然也可以直接跟一个url 而不是url 列表文件。
  
实例: 
  
http_load -rate 5 -seconds 10 urls
  
49 fetches, 2 max parallel, 289884 bytes, in 10.0148 seconds
  
5916 mean bytes/connection
  
4.89274 fetches/sec, 28945.5 bytes/sec
  
msecs/connect: 28.8932 mean, 44.243 max, 24.488 min
  
msecs/first-response: 63.5362 mean, 81.624 max, 57.803 min
  
HTTP response codes:
  
code 200 - 49
  
分析: 
  
1．49 fetches, 2 max parallel, 289884 bytes, in 10.0148 seconds
  
说明在上面的测试中运行了49个请求,最大的并发进程数是2,总计传输的数据是289884bytes,运行的时间是10.0148秒

2．5916 mean bytes/connection
  
说明每一连接平均传输的数据量289884/49=5916

3．4.89274 fetches/sec, 28945.5 bytes/sec
  
说明每秒的响应请求为4.89274,每秒传递的数据为28945.5 bytes/sec

4．msecs/connect: 28.8932 mean, 44.243 max, 24.488 min
  
说明每连接的平均响应时间是28.8932 msecs,最大的响应时间44.243 msecs,最小的响应时间24.488 msecs

5．msecs/first-response: 63.5362 mean, 81.624 max, 57.803 min

6. HTTP response codes: code 200 - 49
  
说明打开响应页面的类型,如果403的类型过多,那可能要注意是否系统遇到了瓶颈。
  
特殊说明: 这里,我们一般会关注到的指标是fetches/sec、msecs/connect
  
他们分别对应的常用性能指标参数Qpt-每秒响应用户数和response time,每连接响应用户时间。测试的结果主要也是看这两个值。当然仅有这两个指标并不能完成对性能的分析,我们还需要对服务器的cpu、men进行分析,才能得出结论

Sample run:
  
% ./http_load -rate 5 -seconds 10 urls
  
49 fetches, 2 max parallel, 289884 bytes, in 10.0148 seconds
  
5916 mean bytes/connection
  
4.89274 fetches/sec, 28945.5 bytes/sec
  
msecs/connect: 28.8932 mean, 44.243 max, 24.488 min
  
msecs/first-response: 63.5362 mean, 81.624 max, 57.803 min
  
HTTP response codes:
  
code 200 - 49
  