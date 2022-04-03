---
title: REST Web Service带给我们什么
author: lcf
date: 2012-11-07T06:06:59+00:00
url: /?p=4630
categories:
  - Uncategorized

tags:
  - reprint
---
## REST Web Service带给我们什么
Web Service的协议最近几年一直在发生转变。Web Servcie的最大优势是能在一个操作系统不同的各个系统之间架起沟通的桥梁，早期的 Web Service一般都是以SOAP协议传输。仔细学习和研究过SOAP协议的同学知道，SOAP协议是一个很完备的自解释协议，对Service、Interface、Method和Parameter的描述都非常详细，甚至还制定了一个WSDL的XSD来，在VS中，只要导入Web Service的WSDL，VS就可以自动生成存根代理代码，你只需调用它便可以调用这些SOAP的Web Service了。

SOAP 的Web Service看起来是很完美的解决方案，但是往往看起来完美的东西，用起来并不完美。 SOAP就是如此，随着Web Service 应用在企业级软件的运用，SOAP的缺陷迅速开始暴露出来。

首先，SOAP协议是在是太复杂，很少有人能完全看懂根据SOAP协议生成的数据 (其实这本来设计，就是给机器看的，哪能照顾你大爷，呵呵哦！) 。我本人是很厌烦看SOAP的数据，一看头就大，特别是SOAP头和尾。

其次，太复杂还不是SOAP协议最大的缺陷。大不了我用下解释SOAP的工具，现在VS也提供此类工具用来查看SOAP类型的数据。但是恰恰是这个缺陷造就了SOAP另一个很致命的缺陷。由于SOAP为了是每个调用的参数和返回值都可以独立解释，为此，需要在每次调用中加入大量的XML复杂信息，来解释这些数据。例如为了解释一个XML的节点是STRING，于是<datatype="string">被按在了一个XML节点上，其实这是没有必要的。因为，往往程序员在消费这个service的时候，已经知道了返回的数据类型，比如你在调用GetAge的时候，返回的XML肯定是int型。所以，一般一个SOAP的调用，一个来回少则数K，多则数M的，甚至数G的数据，而在这些数据中，真正有效的数据很少，根据统计，有效数据仅占全部数据的5%，甚至更少。对于海量数据的企业应用来说，大量的用户对海量数据的存储，如果用SOAP来进行数据传输，那简直就是灾难！！！

另外，调式SOAP的WEB SERVICE也是很费时费力的，SOAP数据的难阅读性，直接增加了调式的难度。

所以，在REST之前，很多的企业应用还是用DCOM，甚至是自定义XML来进行数据传输。

那有没有很好协议的Web Service呢！？。。。现在。。。有了，REST的Web Service就是。

REST的Web Service彻底摒弃了SOAP协议。它的数据格式简单，一般都直接采用对象XML序列化的数据作为返回结果。这样就极大的降低了数据传输量，提高了效率。而且这种XML数据可以直接用IE打开，很容易阅读理解。

随着WCF和VS 2008的发布，MS首次加入了对架构REST Web Service的支持，虽然还很不完全，但是有总比没有好！现在，你只需: 

1，添加Data Contract

2，添加Interface并附给URL

3，设置CLASS

4，附加到IIS或者CONSOLE程序

你就可以创建一个REST Web Service。然后通过IE，在地址栏输入Interface的URL，就想访问网页一样调用你的Web Service，返回的数据就通过IE直接显示，这够直观了吧！？

现在，很多大型公司的Public Web Service也都已经REST化，比如GOOGLE所有的Web Service都是REST的，MS也已经采用REST来优化他的public WebService。很多"云计算"的提供商，如AMASON，他的"云服务" (呵呵，暂且如此叫吧) ，也是REST的。国内很多知名公司在看到REST的巨大优势后也纷纷开始采用REST的Web Service来提高他们的效率，如上海深睿科技的销售管理软件易卖通采用REST WebService，极大的提高了系统的速度和效率，使得传统的供销村管理软件架构在网络和"云"内成为可能。

总之，REST带给我们的是，一种更好、更简单、更有效率的Web Service，同时，可能将来成为"云计算"的基础通讯协议。


