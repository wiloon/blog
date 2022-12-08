---
title: tcp http 调试, 抓包工具, wireshark, Fiddler
author: "-"
date: 2013-12-13T06:14:32+00:00
url: /?p=6037
categories:
  - network
tags:
  - network

---
## tcp http 调试, 抓包工具, wireshark, Fiddler

### wireshark

wireshark的前身是Ethereal，2006年因为其创始人Gerald Combs的跳槽而改名为wireshark。它是一个跨平台的软件，可以在unix系列、linux、mac os、windows等多个平台上面进行网络协议抓包工作。同时他也是一个开源软件，有兴趣的话可以下载源码深入了解。我们可以通过wireshark官网进一步了解相关知识及下载该软件。
  
### fiddler
  
fiddler的定位是网页调试工具，能记录所有客户端和服务器的http和https请求，允许你监视，设置断点，甚至修改输入输出数据。我们还可以为fiddler安装自己所需的插件，从而更好的利用fiddler的强大功能。详细介绍信息可以通过fiddler官网进一步了解，

做Web开发或者Web分析经常需要查看Http通讯的过程，项目实践中，很多Web相关的各种各样稀奇古怪的问题，最后都能通过分析HTTP流量得以解决。我到现在用过的比较好用的两个Http流量分析工具，一个是HTTP Watch，另外一个是Fiddler。

HTTP Watch

HTTP Watch是我最早用过的HTTP流量分析工具。它只能用于IE和Firefox浏览器上。

它有两种使用界面，一种是以插件的形式附加在浏览器上面，供实时分析使用。你可以看到当前窗口中所有的HTTP请求/响应过程。另外它允许把实时分析的结果保存为后缀名为hwl的文件，然后用其自带的Http Watch Studio工具打开，这样既方便了以后对此过程再次进行分析，也方便与其他人共享，易于调试。下面是它的插件界面的截图，非常清新简洁:

image

它的界面非常简单，主要分成三部分: 工具栏，HTTP消息概览，HTTP消息细节窗口。

工具栏主要是方便你快速过滤出你想要分析HTTP消息。

image

你可以按照HTTP流量内容类型去筛选，例如只查看图片相关的HTTP流量。或者根据Url是否包含某特定字符串进行过滤，等等。另外工具栏也提供了"清缓存"和"清Cookie"两个非常常见的操作。

HTTP消息概览栏可以让你快速查看当前窗口中的所有HTTP消息，每个HTTP消息花费的时间，以及服务器返回的状态码，请求的Url等等。默认它还会按照HTTP消息发起的页面进行分组，方便查看。

最底部就是每条HTTP消息的详细信息。最后面的Stream标签页显示的是最原始的HTTP请求/响应流。这里记录的信息是最详细的。

image

为了方便分析常见的需求，它将HTTP消息分成几个部分，也就是你上面看到的Headers、Cookies、QueryString、PostData等等标签页所展示的内容。下面的图展示了此次HTTP通讯涉及的Cookie，每个Cookie的键值，作用的主机域以及路径、过期时间等。

image

HTTP Watch Studio就不做介绍了，基本和插件版本的一致，只不过可以脱离浏览器直接分析以前保存的HTTP通讯过程。

HTTP Watch提供了基础版本以及专业版本，其中基础版本是免费的。事实上基础版本提供的功能已经能够适用于大多数的情况了。

官方站点: <http://www.httpwatch.com>

Fiddler

Fiddler是微软推出的一个免费的HTTP流量分析工具。一开始我以为他只支持IE——毕竟是微软的东西——加之常见的功能HTTP Watch都已经够用了，就没怎么关注。这些天因为要调试Chrome浏览器上的一些问题，而Chrome自带的开发者工具又非常糟糕，搜着搜着又再次找到了Fiddler。

image

Fiddler的界面和HTTP Watch差不多，都是分成三部分，工具栏+HTTP通讯总览+HTTP消息细节。只不过默认情况下它把HTTP消息细节窗口放到了右边。

用了一阵子发现，HTTP Watch能做到的，基本在Fiddler上都可以实现。不过Fiddler的界面显得比HTTP Watch要复杂一些，因为它提供了一些HTTP Watch没有的功能。下面主要介绍的是它和HTTP Watch不一样的地方，一样的功能就略过了。

Fiddler能够监视所有本地进程的HTTP消息，而不仅限于IE、Firefox这些浏览器。这比HTTP Watch适用范围更广。下图显示了google talk和Visual Studio发起的HTTP请求.

image

安装完Fiddler之后你会发现IE还有Firefox中都多了个Fiddler的插件，Fiddler的原理实际上是在本地启动HTTP代理服务器，因为除了Firefox以外，很多应用程序包括其他浏览器都会应用IE上设置的代理。所以Fiddler只需要设置IE和Firefox这两个浏览器的代理服务器即可。这个插件做的事情实际上就是起到动态切换代理服务器的作用。

选中左侧某条特定的HTTP请求，Fiddler会在右侧帮你统计一下当前选中的HTTP消息的一些性能指标，例如发送/接受字节数，发送/接收时间，还有粗略统计世界各地访问该服务器所花费的时间。

image

在右侧窗口中，你可以采用各种视图去解析同一个HTTP请求/响应。例如以纯文本视图，或者图片视图，十六进制视图等等。它还提供了一个压缩测试工具，告诉你如果启用了Gzip或者deflate等压缩之后能够节省多少传输字节。

image

Fiddler会记录下每次HTTP通讯的过程，然后允许你在不将请求发送给服务器的情况下返回之前记录的响应结果。

Fiddler还允许你对HTTP请求下断点，然后你可以根据情况来决定每个请求所返回的响应。

如果你想测试一些特殊的HTTP请求或者修改当前请求一些报头的时候，你不需要自己再写一个小程序去实现这样的功能，因为在Fiddler提供了直接编写HTTP请求的功能。你可以模拟浏览器去发送HTTP消息。

Fiddler支持插件机制，如果你觉得它提供的功能还不够用，那么你可以安装各种插件以增强它的功能或者编写自己的插件。官网上提供了几个不错的插件供免费下载。一个可以用于对HTML和Javascript代码进行语法着色，还有一个可以监视Web应用程序的安全隐患。

官方站点: <http://www.fiddler2.com>

总结

总的来说，HTTP Watch的使用相比Fiddler更简洁、容易上手。但是只适用于IE和Firefox。Fiddler功能更为强大，适用范围更广，而且还是免费的。具体用哪个就得看实际需求了。

1.为什么是Fiddler?
  
抓包工具有很多，小到最常用的web调试工具firebug，达到通用的强大的抓包工具wireshark.为什么使用fiddler?原因如下:

a.Firebug虽然可以抓包，但是对于分析http请求的详细信息，不够强大。模拟http请求的功能也不够，且firebug常常是需要"无刷新修改"，如果刷新了页面，所有的修改都不会保存。

b.Wireshark是通用的抓包工具，但是比较庞大，对于只需要抓取http请求的应用来说，似乎有些大材小用。

c.Httpwatch也是比较常用的http抓包工具，但是只支持IE和firefox浏览器 (其他浏览器可能会有相应的插件) ，对于想要调试chrome浏览器的http请求，似乎稍显无力，而Fiddler2 是一个使用本地 127.0.0.1:8888 的 HTTP 代理，任何能够设置 HTTP 代理为 127.0.0.1:8888 的浏览器和应用程序都可以使用 Fiddler。

2.什么是Fiddler?
  
Fiddler是位于客户端和服务器端的HTTP代理，也是目前最常用的http抓包工具之一 。 它能够记录客户端和服务器之间的所有 HTTP请求，可以针对特定的HTTP请求，分析请求数据、设置断点、调试web应用、修改请求的数据，甚至可以修改服务器返回的数据，功能非常强大，是web调试的利器。

既然是代理，也就是说: 客户端的所有请求都要先经过Fiddler，然后转发到相应的服务器，反之，服务器端的所有响应，也都会先经过Fiddler然后发送到客户端，基于这个原因，Fiddler支持所有可以设置http代理为127.0.0.1:8888的浏览器和应用程序。使用了Fiddler之后，web客户端和服务器的请求如下所示:

Fiddler 作为系统代理，当启用 Fiddler 时，IE 的PROXY 设定会变成 127.0.0.1:8888，因此如果你的浏览器在开启fiddler之后没有设置相应的代理，则fiddler是无法捕获到HTTP请求的。如下是启动Fiddler之后，IE浏览器的代理设置:

以Firefox为例，默认情况下，firefox是没有启用代理的 (如果你安装了proxy等代理工具或插件，是另外一种情况) ，在firefox中配置http代理的步骤如下:

工具->选项->高级->网络->设置  。并配置相应的代理如下:

就可以使用Fiddler抓取Firefox的HTTP请求了。

3.Fiddler使用界面简介
  
Fiddler主界面的布局如下:

主界面中主要包括四个常用的块:

1.Fiddler的菜单栏，上图绿色部分。包括捕获http请求，停止捕获请求，保存http请求，载入本地session、设置捕获规则等功能。

2.Fiddler的工具栏,上图红色部分。包括Fiddler针对当前view的操作 (暂停，清除session,decode模式、清除缓存等) 。

3.web Session面板，上图黄色区域，主要是Fiddler抓取到的每条http请求 (每一条称为一个session) ,主要包含了请求的url，协议，状态码，body等信息，详细的字段含义如下图所示:

4.详情和数据统计面板。针对每条http请求的具体统计 (例如发送/接受字节数，发送/接收时间，还有粗略统计世界各地访问该服务器所花费的时间) 和数据包分析。如inspector面板下，提供headers、textview、hexview,Raw等多种方式查看单条http请求的请求报文的信息:

而composer面板下，则可以模拟向相应的服务器发送数据的过程 (不错，这就是灌水机器人的基本原理,也可以是部分http flood的一种方式) 。

也可以粘贴一次请求的raw http headers,达到模拟请求的目的:

Filter标签则可以设置Fiddler的过滤规则，来达到过滤http请求的目的。最简单如: 过滤内网http请求而只抓取internet的http请求，或则过滤相应域名的http请求。Fiddler的过滤器非常强大，可以过滤特定http状态码的请求，可以过滤特定请求类型的http请求 (如css请求，image请求，js请求等) ，可以过滤请求报文大于或则小于指定大小 (byte) 的请求:

请多的过滤器规则需要一步一步去挖掘。

<http://www.cnblogs.com/TankXiao/archive/2012/02/06/2337728.html>

<http://blog.csdn.net/lisztlee/article/details/8221135>

<http://blog.csdn.net/ohmygirl/article/details/17846199>
