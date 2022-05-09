---
title: JMeter
author: "-"
date: 2015-09-21T01:21:31+00:00
url: /?p=8310
categories:
  - Inbox
tags:
  - reprint
---
## JMeter


Aggregate Report 是 JMeter 常用的一个 Listener，中文被翻译为"聚合报告"。今天再次有同行问到这个报告中的各项数据表示什么意思，顺便在这里公布一下，以备大家查阅。

如果大家都是做Web应用的性能测试，例如只有一个登录的请求，那么在Aggregate Report中，会显示一行数据，共有10个字段，含义分别如下。

Label: 每个 JMeter 的 element (例如 HTTP Request) 都有一个 Name 属性，这里显示的就是 Name 属性的值

#Samples: 表示你这次测试中一共发出了多少个请求，如果模拟10个用户，每个用户迭代10次，那么这里显示100

Average: 平均响应时间——默认情况下是单个 Request 的平均响应时间，当使用了 Transaction Controller 时，也可以以Transaction 为单位显示平均响应时间

Median: 中位数，也就是 50％ 用户的响应时间

90% Line: 90％ 用户的响应时间

Note: 关于 50％ 和 90％ 并发用户数的含义，请参考下文

http://www.cnblogs.com/jackei/archive/2006/11/11/557972.html

Min: 最小响应时间

Max: 最大响应时间

Error%: 本次测试中出现错误的请求的数量/请求的总数

Throughput: 吞吐量——默认情况下表示每秒完成的请求数 (Request per Second) ，当使用了 Transaction Controller 时，也可以表示类似 LoadRunner 的 Transaction per Second 数

KB/Sec: 每秒从服务器端接收到的数据量，相当于LoadRunner中的Throughput/Sec


一、基本概念

1．测试计划是使用 JMeter 进行测试的起点，它是其它 JMeter 测试元件的容器。
  
2．线程组: 代表一定数量的并发用户，它可以用来模拟并发用户发送请求。实际的请求内容在Sampler中定义，它被线程组包含。可以在"测试计划->添加->线程组"来建立它，然后在线程组面板里有几个输入栏: 线程数、Ramp-Up Period(in seconds)、循环次数，其中Ramp-Up Period(in seconds)表示在这时间内创建完所有的线程。如有8个线程，Ramp-Up = 200秒，那么线程的启动时间间隔为200/8=25秒，这样的好处是: 一开始不会对服务器有太大的负载。线程组是为模拟并发负载而设计。
  
3. 取样器 (Sampler) : 模拟各种请求。所有实际的测试任务都由取样器承担，存在很多种请求。如: HTTP 、ftp请求等等。
  
4. 监听器: 负责收集测试结果，同时也被告知了结果显示的方式。功能是对取样器的请求结果显示、统计一些数据 (吞吐量、KB/S……) 等。
  
6. 断言: 用于来判断请求响应的结果是否如用户所期望，是否正确。它可以用来隔离问题域，即在确保功能正确的前提下执行压力测试。这个限制对于有效的测试是非常有用的。
  
7. 定时器: 负责定义请求 (线程) 之间的延迟间隔，模拟对服务器的连续请求。
  
5. 逻辑控制器: 允许自定义JMeter发送请求的行为逻辑，它与Sampler结合使用可以模拟复杂的请求序列。
  
8. 配置元件维护Sampler需要的配置信息，并根据实际的需要会修改请求的内容。
  
9. 前置处理器和后置处理器负责在生成请求之前和之后完成工作。前置处理器常常用来修改请求的设置，后置处理器则常常用来处理响应的数据。
  
二、Jmeter报告  (转载) 
  
http://www.cnblogs.com/jackei/archive/2006/11/13/558720.html

1. Aggregate Report 解析

Aggregate Report 是 JMeter 常用的一个 Listener，中文被翻译为"聚合报告"。今天再次有同行问到这个报告中的各项数据表示什么意思，顺便在这里公布一下，以备大家查阅。
  
如果大家都是做Web应用的性能测试，例如只有一个登录的请求，那么在Aggregate Report中，会显示一行数据，共有10个字段，含义分别如下。
  
Label: 每个 JMeter 的 element (例如 HTTP Request) 都有一个 Name 属性，这里显示的就是 Name 属性的值
  
#Samples: 表示你这次测试中一共发出了多少个请求，如果模拟10个用户，每个用户迭代10次，那么这里显示100
  
Average: 平均响应时间——默认情况下是单个 Request 的平均响应时间，当使用了 Transaction Controller 时，也可以以Transaction 为单位显示平均响应时间
  
Median: 中位数，也就是 50％ 用户的响应时间
  
90% Line: 90％ 用户的响应时间
  
Note: 关于 50％ 和 90％ 并发用户数的含义，请参考下文
  
http://www.cnblogs.com/jackei/archive/2006/11/11/557972.html
  
Min: 最小响应时间
  
Max: 最大响应时间
  
Error%: 本次测试中出现错误的请求的数量/请求的总数
  
Throughput: 吞吐量——默认情况下表示每秒完成的请求数 (Request per Second) ，当使用了 Transaction Controller 时，也可以表示类似 LoadRunner 的 Transaction per Second 数
  
KB/Sec: 每秒从服务器端接收到的数据量，相当于LoadRunner中的Throughput/Sec

基本知识: 

1. 吞吐量: 是指在没有帧丢失的情况下，设备能够接受的最大速率。
  
2. 存储的最小单位是字节Byte，对于存储单位，有以下几个单位，GB、MB和KB，那么这三者之间的换算关系是: 1GB＝1024MB，1MB＝1024KB，1KB＝1024Bytes。
  
Bit : "位"，称为bit，也就是比特，有的时候也称为位。一个字节为8位二进制表示。
  
Byte: "字节"，一个字节就是8比特。
  
3. Mbps (million bits per second 兆位/秒) 代表每秒传输1，000，000比特。该缩写用来描述数据传输速度。例如: 4Mbps=每秒钟传输4M比特。
  
数据传输速率的单位，字母b (bit) 是比特和字母 B  (Byte) 是字节。
  
4. 吞吐量与带宽的区分: 吞吐量和带宽是很容易搞混的一个词，两者的单位都是Mbps.先让我们来看两者对应的英语，吞吐量:throughput ; 带宽: Max net bitrate 。当我们讨论通信链路的带宽时，一般是指链路上每秒所能传送的比特数。我们可以说以太网的带宽是10Mbps。但是，我们需要区分链路上的可用带宽 (带宽) 与实际链路中每秒所能传送的比特数 (吞吐量) 。我们倾向于用"吞吐量"一次来表示一个系统的测试性能。这样，因为实现受各种低效率因素的影响，所以由一段带宽为10Mbps的链路连接的一对节点可能只达到2Mbps的吞吐量。这样就意味着，一个主机上的应用能够以2Mbps的速度向另外的一个主机发送数据。
  
5. 方差和标准差都是用来描述一组数据的波动性的 (集中还是分散) ，标准差的平方就是方差。方差越大，数据的波动越大。
  
三．利用BadBoy生成测试计划 (测试脚本) 
  
badBoy可以非常容易的生成web的测试脚本。类似与LoadRunner的使用，输入站点的URL，点击Record开始录制。File –> Export to Jmeter ，导出为Jmeter认识的测试脚本。
  
四．一个简单的测试示例思路 (目前自己思路，不断改进) 

a． 需要的"测试脚本"，对应web的应用使用badboy生成测试脚本。直接导入Jmeter，进行配置。

b．如图

TestPlan : 是整个Jmeter测试执行的容器。
  
ThreadGroup : 模拟请求，定义线程数、Ramp-Up Period、循环次数。
  
Step1 : 循环控制器 ，控制Sample的执行次数。
  
Sample取样器 : 决定进行那种类型的测试，如http、ftp等。
  
监听器 : 图形结果、聚合报告。
  
定时器 : Random类型，定义线程请求的延迟。

c．聚合报告的解释

Label : 各个模拟测试的名称
  
#Samples : 各个测试的样本总数
  
Average : 每个请求的平均响应时间
  
Median : 中值，即50%请求的平均响应时间
  
90%Line : 90%请求的响应时间
  
Min : 最小响应时间 ，Max : 最大的响应时间
  
Error% : 错误响应的概率。即无法响应的概率。
  
ThroughPut : 吞吐量 - 默认情况下表示每秒完成的请求数 (Request per Second) 。
  
KB/Sec : 每秒从服务器端接收到的数据量。
  
五．Jmeter常见问题  (转载)  http://www.51testing.com/?uid-128005-action-viewspace-itemid-84094
  
说明: 这些问答是从网上转载的，自己修改了其中的一些内容，如果大家兴趣，可以将大家在使用Jmeter的时候碰到的问题写下来，我们一起补充到这个问答里面，共同努力完善jmeter的资料。
  
1. JMeter的工作原理是什么？
  
向服务器提交请求；从服务器取回请求返回的结果。

2. JMeter的作用？
  
JMeter可以用于测试静态或者动态资源的性能 (文件、Servlets、Perl脚本、java对象、数据库和查询、ftp服务器或者其他的资源) 。JMeter用于模拟在服务器、网络或者其他对象上附加高负载以测试他们提供服务的受压能力，或者分析他们提供的服务在不同负载条件下的总性能情况。你可以用JMeter提供的图形化界面分析性能指标或者在高负载情况下测试服务器/脚本/对象的行为。

3. 怎样能看到jmeter提供的脚本范例？
  
在\JMeter\jakarta-jmeter-2.0.3\xdocs\demos目录下。

4. 怎样设置并发用户数？
  
选中可视化界面中左边树的Test Plan节点，单击右键，选择Add-> Thread Group,其中Number of Threads参数用来设置发送请求的用户数目。

5. JMeter的运行指示？
  
Jmeter在运行时，右上角有个单选框大小的小框框，运行是该框框为绿色，运行完毕后，该框框为白色。

6. User Parameters的作用是什么？
  
提高脚本可用性

7. 在result里会出现彩色字体的http response code，说明什么呢？
  
Http response code是http返回值，彩色字体较引人注目，可以使用户迅速关注。象绿色的302就说明在这一步骤中，返回值取自本机的catch，而不是server。

8. 怎样计算Ramp-up period时间？
  
Ramp-up period是指每个请求发生的总时间间隔，单位是秒。如果Number of Threads设置为5，而Ramp-up period是10，那么每个请求之间的间隔就是10/5，也就是2秒。Ramp-up period设置为0，就是同时并发请求。

9. Get和Post的区别？
  
他们是http协议的2种不同实现方式。Get是指server从Request URL取得所需参数。从result中的request中可以看到，get可以看到参数，但是post是主动向server发送参数，所以一般看不到这些参数的。

10. 哪些原因可能导致error的产生？
  
a. Http错误，包括不响应，结果找不到，数据错误等等；
  
b. JMeter本身原因产生的错误。

11. 为什么Aggregate Report结果中的Total值不是真正的总和？
  
JMeter给结果中total的定义是并不完全指总和，为了方便使用，它的值表现了所在列的代表值，比如min值，它的total就是所在列的最小值。下图就是total在各列所表示的意思。

12. JMeter的Thread Number是提供多个不同用户并发的功能么？
  
不是，Thread Number仅仅是指并发数，如果需要实现多个不同用户并发，我们应该采用其它方法，比如通过在jmeter外建立csv文件的方法来实现。

13. 同时并发请求时，若需要模拟不同的用户同时向不同的server并发请求，怎样实现呢？
  
方法很灵活，我们可以将不同的server在thread里面预先写好。或者预先将固定的变量值写入csv文件，这样还可以方便修改。然后将文件添加到User Parameters。

14. User Parameter中的DUMMY是什么意思？
  
当其具体内容是${__CSVRead(${__property(user.dir)}${FILENAME},next())}时用来模拟读文件的下一行。

15. 当测试对象在多server间跳转时，应该怎样处理？
  
程序运行时，有些http和隐函数会携带另外的server IP,我们可以从他们的返回值中获取。

16. 为何测试对象是http和https混杂出现？
  
Https是加密协议，为了安全，一般不推荐使用http，但是有些地方，使用https过于复杂或者较难实现，会采用http协议。

17. Http和https的默认端口是什么？
  
Apache server (Http)的默认端口是80；
  
SSL (Https)的默认端口是443。

18. 为何在run时，有些页面失败，但是最后不影响结果？
  
原因较多，值得提及的一种是因为主流页面与它不存在依赖关系，所以即使这样的页面出错，也不会影响运行得到正常结果，但是这样会影响到测试的结果以及分析结果。

19. 为什么脚本刚开始运行就有错误，其后来的脚本还可运行？
  
在Thread Group中有相关设置，如果选择了continue，即使前面的脚本出现错误，整个thread仍会运行直到结束。选择Stop Thread会结束当前thread；选择Stop Test则会结束全部的thread。推荐选项是Stop Thread。

20. 在Regular expression_r Extractor会看到Template的值是$1$,这个值是什么意思呢？
  
$1$是指取第一个 () 里面的值。如果Regular expression_r的数值有多个，用这种方法可以避免不必要的麻烦。

21. Regular expression_r中的(.*)是什么意思？
  
那是一个正则表达式 (regular expression_r) 。'.'等同于sql语言中的'?',表示可有可无。'\*'表示0个或多个。'()'表示需要取值。(.\*)表达任意长度的字符串。

22. 在读取Regular expression_r时要注意什么？
  
一定要保证所取数值的绝对唯一性。

23. 怎样才能判断什么样的情况需要添加Regular expression_r Extractor？
  
检查Http Request中的Send Parameters,如果有某个参数是其前一个page中所没有给出的，就要到原文件中查找，并添加Regular expression_r Extractor到其前一page的http request中。

24. 在自动获取的脚本中有时会出现空的http request，是什么意思呢？
  
是因为在获取脚本时有些错误，是脚本工具原因。在run时这种错误不参与运行的。

25. 在运行结果中为何有rate为N/A的情况出现？
  
可能因为JMeter自身问题造成，再次运行可以得到正确结果。

26. 常用http错误代码有哪些？
  
400无法解析此请求。
  
403禁止访问: 访问被拒绝。
  
404找不到文件或目录。
  
405用于访问该页的HTTP动作未被许可。
  
410文件已删除。
  
500服务器内部错误。
  
501标题值指定的配置没有执行。
  
502 Web服务器作为网关或代理服务器时收到无效的响应。

27. Http request中的Send Parameters是指什么？
  
是指code中写定的值和自定义变量中得到的值，就是在运行页面时需要的参数。

28. Parameters在页面中是不断传递的么？
  
是的。参数再产生后会在页面中一直传递到所需页面。所以我们可以在动态参数产生时捕获它，也可以在所需页面的上一页面捕获。(但是这样可能有错误，最好在产生页面获取)

29. 在使用JMeter测试时，是完全模拟用户操作么？造成的结果也和用户操作完全相同么？
  
是的。JMeter完全模拟用户操作，所以操作记录会全部写入DB.在运行失败时，可能会产生错误数据，这就取决于脚本检查是否严谨，否则错误数据也会进入DB，给程序运行带来很多麻烦。
  
六．Jmeter测试心得 (转载)  http://www.javaeye.com/topic/211216

企业应用开发过程中，性能测试是很重要的一个环节，在这个环节中Apache的JMeter以它开源、100%纯Java、操作方便等优点发挥着很大的作用。
  
经过一段时间的使用，多少有些心得和技巧，拿出来共享，希望能有些帮助。

1. 制作测试脚本: 
  
手工制作测试脚本，需要你知道请求的url和携带的参数等等，太花费时间，
  
所以可以用badboy工具录制脚本。这个工具虽然不是开源的，但是却可以用来免费的录制成.jmx的脚本，使用起来很方便。
  
官方网站是: http://www.badboy.com.au/

2. 出现乱码了？
  
在用JMeter发行HTTPRequest时，在请求参数中有中文时，发现存储到DB中后，相应的字段是乱码，
  
明明在参数后面的Encode选项中打了V。后来发现badboy录制脚本的时候并没有记录编码方式，所以修改脚本，
  
在Content encoding中设置正确的编码方式就不会出现乱码了。

3. JMeter的妙用-准备测试数据: 
  
要求性能测试开始前，先准备5W条数据。当然可以通过直接修改DB，但是如果这5W条数据涉及到很多表的关联，
  
甚至还要通过存储过程的处理怎么办，直接修改DB很容易出现错误的数据，要是在客户的机器上弄错，可就闯祸了。
  
这时候想到了JMeter，它本来是用来模拟大量用户并发请求的，现在用它来批量的生成数据吧。
  
如果要求每条数据都不同，就要修改脚本，使用JMeter的函数来动态产生数据，比较常用的是CSVRead函数，
  
记不住名的话Ctrl+F可以呼唤出函数助手。使用这个函数的时候需要注意几点，首先是csv文件的编码格式，
  
使用ansi没有问题，使用unicode时会使读取的第一行数据出现错误；
  
${__CSVRead(data.txt,0)}-读取本行的第一列值
  
${__CSVRead(data.txt,1)}${__CSVRead(data.txt,next)}-读取本行的第二列值，并把行标移动到下一行
  
试验证明JMeter应该做好了同步，在多线程环境下上面的调用方法没有问题；
  
最后，修改JMeter的线程数会加快数据生成的速度，原理是当并发线程在20左右的时候会达到最大的吞吐量 (request/分) ，
  
所以应该设定线程数20左右。

4. JMeter中debug方法: 
  
JMeter提供了log函数输出log，但是有时候并不好用，比如我想输出某个函数的返回值看是不是正确的，
  
${__log(${__CSVRead(data.txt,1)})}这样的写法是错误的，JMeter会抛出异常，该怎么办呢？
  
答案是巧用监听器 (Listener) 来输出想看到的数据，结果显示为树的那个监听器，
  
它可以让你查看每个sampler的请求数据和响应数据，在请求数据中就有你想看到的信息。

5. 常用的功能: 
  
?使用HTTP Cookie Manager或URL重写实现同一线程内的多个请求共享Session。
  
?把Login的请求放到只执行一次的控制器中，那么即使循环多次，Login也只请求一次。
  
?如果想让多个线程在同一时刻同时请求，那么用Synchronizing Timer来做集合点。
  
?为了节省系统资源，使用非窗口模式运行JMeter (jmeter -n -t test.jmx) 
  
?如果模拟并发用户过多，比如200线程，那么可以分散到多台机器上运行Jmeter (比如4台电脑，每台50线程) 
  
更多功能请参照使用手册
  
中文手册 (未完成) http://wiki.javascud.org/pages/viewpage.action?pageId=5566

6. 在winnt系统上，使用perfmon来帮助Jmeter采集服务器的系统资源数据，可以配置log输出这些数据作为性能瓶颈分析时使用。
  
七．置信区间 http://java.chinaitlab.com/tools/355421.html
  
对数据进行更科学的分析，确定测试结果。类似于Jmeter聚合报告的90% Line给出的参考，而不能仅仅参考均值。
  
记: 熟悉Jmeter使用之后，自己更应该关注的是"测试实践"，以及通过怎么样的方法改进性能。

http://whttp://blog.csdn.net/ultrani/article/details/8309932

www.51testing.com/html/28/116228-238479.html

