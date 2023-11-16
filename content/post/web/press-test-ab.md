---
title: Web服务 压力测试工具,goreplay gor, http_load、webbench、apabhe ab、siege
author: "-"
date: 2015-09-15T07:13:48+00:00
url: /?p=8261
categories:
  - Inbox
tags:
  - reprint
---
## Web服务 压力测试工具,goreplay gor, http_load、webbench、apabhe ab、siege

### goreplay, Gor

[https://github.com/buger/goreplay](https://github.com/buger/goreplay)

一、http_load
  
程序非常小,解压后也不到100K
  
http_load以并行复用的方式运行,用以测试web服务器的吞吐量与负载。但是它不同于大多数压力测试工具,它可以以一个单一的进程运行,一般不会把客户机搞死。还可以测试HTTPS类的网站请求。

下载地址: [http://soft.vpser.net/test/http_load/http_load-12mar2006.tar.gz](http://soft.vpser.net/test/http_load/http_load-12mar2006.tar.gz)

安装
  
tar zxvf http_load-12mar2006.tar.gz

cd http_load-12mar2006

make && make install

<!--more-->

命令格式: http_load  -p 并发访问进程数  -s 访问时间  需要访问的URL文件
  
参数其实可以自由组合,参数之间的选择并没有什么限制。比如你写成http_load -parallel 5 -seconds
  
300 urls.txt也是可以的。我们把参数给大家简单说明一下。
  
-parallel 简写-p : 含义是并发的用户进程数。
  
-fetches 简写-f : 含义是总计的访问次数
  
-rate    简写-p : 含义是每秒的访问频率
  
-seconds简写-s : 含义是总计的访问时间
  
准备URL文件: urllist.txt,文件格式是每行一个URL,URL最好超过50－100个测试效果比较好.文件格式如下:

    VPS服务器的选择
  
[https://www.vpser.net/other/choose-vps.html/embed#?secret=iAUiVVmnMv](https://www.vpser.net/other/choose-vps.html/embed#?secret=iAUiVVmnMv)

    HyperVM使用教程/手册
  
[https://www.vpser.net/vps-cp/hypervm-tutorial.html/embed#?secret=cLrZu8rncf](https://www.vpser.net/vps-cp/hypervm-tutorial.html/embed#?secret=cLrZu8rncf)

    DiaVPS 4月最新优惠
  
[https://www.vpser.net/coupons/diavps-april-coupons.html/embed#?secret=aK3vT9Oj6d](https://www.vpser.net/coupons/diavps-april-coupons.html/embed#?secret=aK3vT9Oj6d)

    VPS主机上备份网站和数据库
  
[https://www.vpser.net/security/vps-backup-web-MySQL.html/embed#?secret=GisBcCy5FH](https://www.vpser.net/security/vps-backup-web-MySQL.html/embed#?secret=GisBcCy5FH)
  
例如:
  
http_load -p 30 -s 60  urllist.txt
  
参数了解了,我们来看运行一条命令来看看它的返回结果
  
命令: % ./http_load -rate 5 -seconds 10 urls说明执行了一个持续时间10秒的测试,每秒的频率为5。
  
49 fetches, 2 max parallel, 289884 bytes, in 10.0148 seconds5916 mean bytes/connection4.89274
  
fetches/sec, 28945.5 bytes/secmsecs/connect: 28.8932 mean, 44.243 max, 24.488 minmsecs/first
  
-response: 63.5362 mean, 81.624 max, 57.803 minHTTP response codes: code 200 — 49

结果分析:
  
1．49 fetches, 2 max parallel, 289884 bytes, in 10.0148 seconds
  
说明在上面的测试中运行了49个请求,最大的并发进程数是2,总计传输的数据是289884bytes,运行的时间是10.0148秒
  
2．5916 mean bytes/connection说明每一连接平均传输的数据量289884/49=5916
  
3．4.89274 fetches/sec, 28945.5 bytes/sec
  
说明每秒的响应请求为4.89274,每秒传递的数据为28945.5 bytes/sec
  
4．msecs/connect: 28.8932 mean, 44.243 max, 24.488 min说明每连接的平均响应时间是28.8932 msecs,最大的响应时间44.243 msecs,最小的响应时间24.488 msecs
  
5．msecs/first-response: 63.5362 mean, 81.624 max, 57.803 min
  
6. HTTP response codes: code 200 — 49     说明打开响应页面的类型,如果403的类型过多,那可能

要注意是否系统遇到了瓶颈。
  
特殊说明:
  
测试结果中主要的指标是 fetches/sec、msecs/connect 这个选项,即服务器每秒能够响应的查询次数,用这个指标来衡量性能。似乎比 apache的ab准确率要高一些,也更有说服力一些。
  
Qpt-每秒响应用户数和response time,每连接响应用户时间。
  
测试的结果主要也是看这两个值。当然仅有这两个指标并不能完成对性能的分析,我们还需要对服务器的cpu、men进行分析,才能得出结论

二、webbench

webbench是Linux下的一个网站压力测试工具,最多可以模拟3万个并发连接去测试网站的负载能力。下载地址可以到google搜,我这里给出一个
  
下载地址: [http://soft.vpser.net/test/webbench/webbench-1.5.tar.gz](http://soft.vpser.net/test/webbench/webbench-1.5.tar.gz)
  
这个程序更小,解压后不到50K,呵呵

安装
  
# tar zxvf webbench-1.5.tar.gz
  
# cd webbench-1.5
  
# make && make install
  
会在当前目录生成webbench可执行文件,直接可以使用了

用法:
  
webbench -c 并发数 -t 运行测试时间 URL
  
如:
  
webbench -c 5000 -t 120 [http://www.163.com](http://www.163.com)

三、ab

选项

-A auth-username:password
  
对服务器提供BASIC认证信任。 用户名和密码由一个:隔开,并以base64编码形式发送。 无论服务器是否需要(即, 是否发送了401认证需求代码),此字符串都会被发送。
  
-c concurrency
  
一次产生的请求个数。默认是一次一个。
  
-C cookie-name=value
  
对请求附加一个Cookie:行。 其典型形式是name=value的一个参数对。 此参数可以重复。
  
-d
  
不显示"percentage served within XX [ms] table"的消息(为以前的版本提供支持)。
  
-e csv-file
  
产生一个以逗号分隔的(CSV)文件, 其中包含了处理每个相应百分比的请求所需要(从1%到100%)的相应百分比的(以微妙为单位)时间。 由于这种格式已经"二进制化",所以比'gnuplot'格式更有用。
  
-g gnuplot-file
  
把所有测试结果写入一个'gnuplot'或者TSV (以Tab分隔的)文件。 此文件可以方便地导入到Gnuplot, IDL, Mathematica, Igor甚至Excel中。 其中的第一行为标题。
  
-h
  
显示使用方法。
  
-H custom-header
  
对请求附加额外的头信息。 此参数的典型形式是一个有效的头信息行,其中包含了以冒号分隔的字段和值的对 (如, "Accept-Encoding: zip/zop;8bit").
  
-i
  
执行HEAD请求,而不是GET。
  
-k
  
启用HTTP KeepAlive功能,即, 在一个HTTP会话中执行多个请求。 默认时,不启用KeepAlive功能.
  
-n requests
  
在测试会话中所执行的请求个数。 默认时,仅执行一个请求,但通常其结果不具有代表意义。
  
-p POST-file
  
包含了需要POST的数据的文件.
  
-P proxy-auth-username:password
  
对一个中转代理提供BASIC认证信任。 用户名和密码由一个:隔开,并以base64编码形式发送。 无论服务器是否需要(即, 是否发送了401认证需求代码),此字符串都会被发送。
  
-q
  
如果处理的请求数大于150, ab每处理大约10%或者100个请求时,会在stderr输出一个进度计数。 此-q标记可以抑制这些信息。
  
-s
  
用于编译中(ab -h会显示相关信息)使用了SSL的受保护的https, 而不是http协议的时候。此功能是实验性的,也是很简陋的。最好不要用。
  
-S
  
不显示中值和标准背离值, 而且在均值和中值为标准背离值的1到2倍时,也不显示警告或出错信息。 默认时,会显示 最小值/均值/最大值等数值。(为以前的版本提供支持).
  
-t timelimit
  
测试所进行的最大秒数。其内部隐含值是-n 50000。 它可以使对服务器的测试限制在一个固定的总时间以内。默认时,没有时间限制。
  
-T content-type
  
POST数据所使用的Content-type头信息。
  
-v verbosity
  
设置显示信息的详细程度 - 4或更大值会显示头信息, 3或更大值可以显示响应代码(404, 200等), 2或更大值可以显示警告和其他信息。
  
-V
  
显示版本号并退出。
  
-w
  
以HTML表的格式输出结果。默认时,它是白色背景的两列宽度的一张表。
  
-x

<

table>-attributes
  
设置

<

table>属性的字符串。 此属性被填入

<

table 这里 >.
  
-X proxy[:port]
  
对请求使用代理服务器。
  
-y

-attributes
  
设置

属性的字符串.
  
-z -attributes
  
设置

属性的字符串.

缺陷
  
程序中有各种静态声明的固定长度的缓冲区。 另外,对命令行参数、服务器的响应头和其他外部输入的解析也很简单,这可能会有不良后果。

它没有完整地实现HTTP/1.x; 仅接受某些'预想'的响应格式。 strstr(3)的频繁使用可能会带来性能问题,即, 你可能是在测试ab而不是服务器的性能。

参数很多,一般我们用 -c 和 -n 参数就可以了. 例如:

./ab -c 1000 -n 1000 [http://127.0.0.1/index.php](http://127.0.0.1/index.php)

这个表示同时处理1000个请求并运行1000次index.php文件.
  
# /usr/local/xiaobai/apache2054/bin/ab -c 1000 -n 1000 [http://127.0.0.1/index.html.zh-cn.gb2312](http://127.0.0.1/index.html.zh-cn.gb2312)
  
This is ApacheBench, Version 2.0.41-dev <$Revision: 1.121.2.12 $> apache-2.0
  
Copyright (c) 1996 Adam Twiss, Zeus Technology Ltd, [http://www.zeustech.net/](http://www.zeustech.net/)
  
Copyright (c) 1998-2002 The Apache Software Foundation, [http://www.apache.org/](http://www.apache.org/)

Benchmarking 127.0.0.1 (be patient)
  
Completed 100 requests
  
Completed 200 requests
  
Completed 300 requests
  
Completed 400 requests
  
Completed 500 requests
  
Completed 600 requests
  
Completed 700 requests
  
Completed 800 requests
  
Completed 900 requests
  
Finished 1000 requests
  
Server Software: Apache/2.0.54
  
//平台apache 版本2.0.54
  
Server Hostname: 127.0.0.1
  
//服务器主机名
  
Server Port: 80
  
//服务器端口

Document Path: /index.html.zh-cn.gb2312
  
//测试的页面文档
  
Document Length: 1018 bytes
  
//文档大小

Concurrency Level: 1000
  
//并发数
  
Time taken for tests: 8.188731 seconds
  
//整个测试持续的时间
  
Complete requests: 1000
  
//完成的请求数量
  
Failed requests: 0
  
//失败的请求数量
  
Write errors: 0

Total transferred: 1361581 bytes
  
//整个场景中的网络传输量
  
HTML transferred: 1055666 bytes
  
//整个场景中的HTML内容传输量
  
Requests per second: 122.12 [#/sec] (mean)
  
//大家最关心的指标之一,相当于 LR 中的 每秒事务数 ,后面括号中的 mean 表示这是一个平均值
  
Time per request: 8188.731 [ms] (mean)
  
//大家最关心的指标之二,相当于 LR 中的 平均事务响应时间 ,后面括号中的 mean 表示这是一个平均值
  
Time per request: 8.189 [ms] (mean, across all concurrent requests)
  
//每个请求实际运行时间的平均值
  
Transfer rate: 162.30 [Kbytes/sec] received
  
//平均每秒网络上的流量,可以帮助排除是否存在网络流量过大导致响应时间延长的问题

Connection Times (ms)
  
min mean[+/-sd] median max
  
Connect: 4 646 1078.7 89 3291
  
Processing: 165 992 493.1 938 4712
  
Waiting: 118 934 480.6 882 4554
  
Total: 813 1638 1338.9 1093 7785
  
//网络上消耗的时间的分解,各项数据的具体算法还不是很清楚

Percentage of the requests served within a certain time (ms)
  
50% 1093
  
66% 1247
  
75% 1373
  
80% 1493
  
90% 4061
  
95% 4398
  
98% 5608
  
99% 7368
  
100% 7785 (longest request)
  
//整个场景中所有请求的响应情况。在场景中每个请求都有一个响应时间,其中50％的用户响应时间小于1093 毫秒,60％ 的用户响应时间小于1247 毫秒,最大的响应时间小于7785 毫秒

由于对于并发请求,cpu实际上并不是同时处理的,而是按照每个请求获得的时间片逐个轮转处理的,所以基本上第一个Time per request时间约等于第二个Time per request时间乘以并发请求数

四、Siege
  
一款开源的压力测试工具,可以根据配置对一个WEB站点进行多用户的并发访问,记录每个用户所有请求过程的相应时间,并在一定数量的并发访问下重复进行。
  
官方: [http://www.joedog.org/](http://www.joedog.org/)
  
Siege下载: [http://soft.vpser.net/test/siege/siege-2.67.tar.gz](http://soft.vpser.net/test/siege/siege-2.67.tar.gz)
  
解压:

# tar -zxf siege-2.67.tar.gz

进入解压目录:

# cd siege-2.67/

安装:
  
# ./configure ; make
  
# make install

使用
  
siege -c 200 -r 10 -f example.url
  
-c是并发量,-r是重复次数。 url文件就是一个文本,每行都是一个url,它会从里面随机访问的。

example.url内容:

[http://www.licess.cn](http://www.licess.cn)
  
[http://www.vpser.net](http://www.vpser.net)
  
[http://soft.vpser.net](http://soft.vpser.net)

结果说明
  
Lifting the server siege… done.
  
Transactions: 3419263 hits //完成419263次处理
  
Availability: 100.00 % //100.00 % 成功率
  
Elapsed time: 5999.69 secs //总共用时
  
Data transferred: 84273.91 MB //共数据传输84273.91 MB
  
Response time: 0.37 secs //相应用时1.65秒: 显示网络连接的速度
  
Transaction rate: 569.91 trans/sec //均每秒完成 569.91 次处理: 表示服务器后
  
Throughput: 14.05 MB/sec //平均每秒传送数据
  
Concurrency: 213.42 //实际最高并发数
  
Successful transactions: 2564081 //成功处理次数
  
Failed transactions: 11 //失败处理次数
  
Longest transaction: 29.04 //每次传输所花最长时间
  
Shortest transaction: 0.00 //每次传输所花最短时间

    十个免费的Web压力测试工具
  
[https://coolshell.cn/articles/2589.html/embed#?secret=No65LHIzR5](https://coolshell.cn/articles/2589.html/embed#?secret=No65LHIzR5)
  
[http://www.cnblogs.com/shipengzhi/archive/2012/10/09/2716766.html](http://www.cnblogs.com/shipengzhi/archive/2012/10/09/2716766.html)
  
[https://studygolang.com/articles/3576](https://studygolang.com/articles/3576)
