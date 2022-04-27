---
title: 爬虫Labin,Nutch,Neritrix介绍和对比
author: "-"
date: 2015-01-05T06:22:18+00:00
url: /?p=7174
categories:
  - Uncategorized
tags:
  - Crawler

---
## 爬虫Labin,Nutch,Neritrix介绍和对比
http://www.open-open.com/bbs/view/1325332257061

Larbin
  
开发语言: C++
  
http://larbin.sourceforge.net/index-eng.html
  
larbin是个基于C++的web爬虫工具,拥有易于操作的界面,不过只能跑在LINUX下,在一台普通PC下larbin每天可以爬5百万个页面(当然啦,需要拥有良好的网络)

简介

Larbin是一种开源的网络爬虫/网络蜘蛛,由法国的年轻人 Sébastien Ailleret独立开发。larbin目的是能够跟踪页面的url进行扩展的抓取,最后为搜索引擎提供广泛的数据来源。
  
Larbin只是一个爬虫,也就是说larbin只抓取网页,至于如何parse的事情则由用户自己完成。另外,如何存储到数据库以及建立索引的事情 larbin也不提供。
  
Latbin最初的设计也是依据设计简单但是高度可配置性的原则,因此我们可以看到,一个简单的larbin的爬虫可以每天获取５００万的网页,非常高效。

功能
  
1. larbin 获取单个、确定网站的所有联结,甚至可以镜像一个网站。
  
2. larbin建立 url 列表群,例如针对所有的网页进行 url retrive后,进行xml的联结的获取。或者是 mp3 。
  
3. larbin 定制后可以作为搜索引擎的信息的来源 (例如可以将抓取下来的网页每2000一组存放在一系列的目录结构里面) 。

问题
  
Labin的主要问题是,: 

仅提供保存网页保存功能,没有进行进一步的网页解析；

不支持分布式系统；

功能相对简单,提供的配置项也不够多；

不支持网页自动重访,更新功能；

从2003年底以后,Labin已经放弃更新,目前处于荒芜长草的状态

\***\***\****

Nutch
  
开发语言: Java
  
http://lucene.apache.org/nutch/


简介: 

Apache的子项目之一,属于Lucene项目下的子项目。

Nutch是一个基于Lucene,类似Google的完整网络搜索引擎解决方案,基于Hadoop的分布式处理模型保证了系统的性能,类似Eclipse的插件机制保证了系统的可客户化,而且很容易集成到自己的应用之中。
  
总体上Nutch可以分为2个部分: 抓取部分和搜索部分。抓取程序抓取页面并把抓取回来的数据做成反向索引,搜索程序则对反向索引搜索回答用户的请求。抓取程序和搜索程序的接口是索引,两者都使用索引中的字段。抓取程序和搜索程序可以分别位于不同的机器上。下面详细介绍一下抓取部分。

抓取部分: 
  
抓取程序是被Nutch的抓取工具驱动的。这是一组工具,用来建立和维护几个不同的数据结构:  web database, a set of segments, and the index。下面逐个解释这三个不同的数据结构: 
  
1. The web database, 或者WebDB。这是一个特殊存储数据结构,用来映像被抓取网站数据的结构和属性的集合。WebDB 用来存储从抓取开始 (包括重新抓取) 的所有网站结构数据和属性。WebDB 只是被 抓取程序使用,搜索程序并不使用它。WebDB 存储2种实体: 页面 和 链接。页面 表示 网络上的一个网页,这个网页的Url作为标示被索引,同时建立一个对网页内容的MD5 哈希签名。跟网页相关的其它内容也被存储,包括: 页面中的链接数量 (外链接) ,页面抓取信息 (在页面被重复抓取的情况下) ,还有表示页面级别的分数 score 。链接 表示从一个网页的链接到其它网页的链接。因此 WebDB 可以说是一个网络图,节点是页面,链接是边。
  
2. Segment 。这是网页的集合,并且它被索引。Segment的Fetchlist 是抓取程序使用的url列表,它是从 WebDB中生成的。Fetcher 的输出数据是从 fetchlist 中抓取的网页。Fetcher的输出数据先被反向索引,然后索引后的结果被存储在segment 中。 Segment的生命周期是有限制的,当下一轮抓取开始后它就没有用了。默认的 重新抓取间隔是30天。因此删除超过这个时间期限的segment是可以的。而且也可以节省不少磁盘空间。Segment 的命名是日期加时间,因此很直观的可以看出他们的存活周期。
  
3. The index。索引库是反向索引所有系统中被抓取的页面,它并不直接从页面反向索引产生,而是合并很多小的segment的索引产生的。Nutch 使用 Lucene 来建立索引,因此所有Lucene相关的工具 API 都用来建立索引库。需要说明的是Lucene的segment 的概念和Nutch的segment概念是完全不同的,不要混淆。简单来说 Lucene 的 segment 是 Lucene 索引库的一部分,而Nutch 的Segment是WebDB中被抓取和索引的一部分。
  
抓取过程详解: 

抓取是一个循环的过程: 抓取工具从WebDB中生成了一个 fetchlist 集合；抽取工具根据fetchlist从网络上下载网页内容；工具程序根据抽取工具发现的新链接更新WebDB；然后再生成新的fetchlist；周而复始。这个抓取循环在nutch中经常指:  generate/fetch/update 循环。
  
一般来说同一域名下的 url 链接会被合成到同一个 fetchlist。这样做的考虑是: 当同时使用多个工具抓取的时候,不会产生重复抓取的现象。Nutch 遵循 Robots Exclusion Protocol, 可以用robots.txt 定义保护私有网页数据不被抓去。
  
上面这个抓取工具的组合是Nutch的最外层的,也可以直接使用更底层的工具,自己组合这些底层工具的执行顺序达到同样的结果。这是Nutch吸引人的地方。下面把上述过程分别详述一下,括号内就是底层工具的名字: 
  
1. 创建一个新的WebDB (admin db -create)。
  
2. 把开始抓取的跟Url 放入WebDb (inject)。
  
3. 从WebDb的新 segment 中生成 fetchlist (generate)。
  
4. 根据 fetchlist 列表抓取网页的内容 (fetch)。
  
5. 根据抓取回来的网页链接url更新 WebDB (updatedb)。
  
6. 重复上面3-5个步骤直到到达指定的抓取层数。
  
7. 用计算出来的网页url权重 scores 更新 segments (updatesegs)。
  
8. 对抓取回来的网页建立索引(index)。
  
9. 在索引中消除重复的内容和重复的url (dedup)。
  
10. 合并多个索引到一个大索引,为搜索提供索引库(merge)。


\***\***\***\***\*****

Heritrix
  
开发语言: Java
  
http://crawler.archive.org/
  
Heritrix是一个开源,可扩展的web爬虫项目。Heritrix设计成严格按照robots.txt文件的排除指示和META robots标签。
  
简介

Heritrix与Nutch对比

和 Nutch。二者均为Java开源框架,Heritrix 是 SourceForge上的开源产品,Nutch为Apache的一个子项目,它们都称作网络爬虫/蜘蛛 ( Web Crawler) ,它们实现的原理基本一致: 深度遍历网站的资源,将这些资源抓取到本地,使用的方法都是分析网站每一个有效的URI,并提交Http请求,从而获得相应结果,生成本地文件及相应的日志信息等。

Heritrix 是个 "archival crawler" - 用来获取完整的、精确的、站点内容的深度复制。包括获取图像以及其他非文本内容。抓取并存储相关的内容。对内容来者不拒,不对页面进行内容上的修改。重新爬行对相同的URL不针对先前的进行替换。爬虫通过Web用户界面启动、监控、调整,允许弹性的定义要获取的URL。


Nutch和Heritrix的差异: 

Nutch 只获取并保存可索引的内容。Heritrix则是照单全收。力求保存页面原貌

Nutch 可以修剪内容,或者对内容格式进行转换。

Nutch 保存内容为数据库优化格式便于以后索引；刷新替换旧的内容。而Heritrix 是添加(追加)新的内容。

Nutch 从命令行运行、控制。Heritrix 有 Web 控制管理界面。

Nutch 的定制能力不够强,不过现在已经有了一定改进。Heritrix 可控制的参数更多。

Heritrix提供的功能没有nutch多,有点整站下载的味道。既没有索引又没有解析,甚至对于重复爬取URL都处理不是很好。

Heritrix的功能强大 但是配置起来却有点麻烦。

\***\***\***\***\***\***\***


三者的比较
  
一、从功能方面来说,Heritrix与Larbin的功能类似。都是一个纯粹的网络爬虫,提供网站的镜像下载。而Nutch是一个网络搜索引擎框架,爬取网页只是其功能的一部分。

二、从分布式处理来说,Nutch支持分布式处理,而另外两个好像尚且还没有支持。

三、从爬取的网页存储方式来说,Heritrix和 Larbin都是将爬取下来的内容保存为原始类型的内容。而Nutch是将内容保存到其特定格式的segment中去。

四,对于爬取下来的内容的处理来说,Heritrix和 Larbin都是将爬取下来的内容不经处理直接保存为原始内容。而Nutch对文本进行了包括链接分析、正文提取、建立索引 (Lucene索引) 等处理。

五,从爬取的效率来说,Larbin效率较高,因为其是使用c++实现的并且功能单一。


crawler
  
开发

语言
  
功能

单一
  
支持分布式

爬取
  
效率
  
镜像

保存
  
Nutch
  
Java
  
×
  
√
  
低
  
×
  
Larbin
  
C++
  
√
  
×
  
高
  
√
  
Heritrix
  
Java
  
√
  
×
  
中
  
√

--------------------


其它一些开源爬虫汇总: 
  
WebSPHINX
  
WebSPHINX是一个Java类包和Web爬虫的交互式开发环境。Web爬虫(也叫作机器人或蜘蛛)是可以自动浏览与处理Web页面的程序。WebSPHINX由两部分组成: 爬虫工作平台和WebSPHINX类包。
  
http://www.cs.cmu.edu/~rcm/websphinx/

WebLech
  
WebLech是一个功能强大的Web站点下载与镜像工具。它支持按功能需求来下载web站点并能够尽可能模仿标准Web浏览器的行为。WebLech有一个功能控制台并采用多线程操作。
  
http://weblech.sourceforge.net/
  
Arale
  
Arale主要为个人使用而设计,而没有像其它爬虫一样是关注于页面索引。Arale能够下载整个web站点或来自web站点的某些资源。Arale还能够把动态页面映射成静态页面。
  
http://web.tiscali.it/_flat/arale.jsp.html

J-Spider
  
J-Spider:是一个完全可配置和定制的Web Spider引擎.你可以利用它来检查网站的错误(内在的服务器错误等),网站内外部链接检查,分析网站的结构(可创建一个网站地图),下载整个Web站点,你还可以写一个JSpider插件来扩展你所需要的功能。
  
http://j-spider.sourceforge.net/

spindle
  
spindle 是一个构建在Lucene工具包之上的Web索引/搜索工具.它包括一个用于创建索引的HTTP spider和一个用于搜索这些索引的搜索类。spindle项目提供了一组JSP标签库使得那些基于JSP的站点不需要开发任何Java类就能够增加搜索功能。
  
http://www.bitmechanic.com/projects/spindle/

Arachnid
  
Arachnid: 是一个基于Java的web spider框架.它包含一个简单的HTML剖析器能够分析包含HTML内容的输入流.通过实现Arachnid的子类就能够开发一个简单的Web spiders并能够在Web站上的每个页面被解析之后增加几行代码调用。 Arachnid的下载包中包含两个spider应用程序例子用于演示如何使用该框架。
  
http://arachnid.sourceforge.net/

LARM
  
LARM能够为Jakarta Lucene搜索引擎框架的用户提供一个纯Java的搜索解决方案。它包含能够为文件,数据库表格建立索引的方法和为Web站点建索引的爬虫。
  
http://larm.sourceforge.net/

JoBo
  
JoBo 是一个用于下载整个Web站点的简单工具。它本质是一个Web Spider。与其它下载工具相比较它的主要优势是能够自动填充form(如: 自动登录)和使用cookies来处理session。JoBo还有灵活的下载规则(如: 通过网页的URL,大小,MIME类型等)来限制下载。
  
http://www.matuschek.net/software/jobo/index.html

snoics-reptile
  
snoics -reptile是用纯Java开发的,用来进行网站镜像抓取的工具,可以使用配制文件中提供的URL入口,把这个网站所有的能用浏览器通过GET的方式获取到的资源全部抓取到本地,包括网页和各种类型的文件,如: 图片、flash、mp3、zip、rar、exe等文件。可以将整个网站完整地下传至硬盘内,并能保持原有的网站结构精确不变。只需要把抓取下来的网站放到web服务器(如: Apache)中,就可以实现完整的网站镜像。
  
http://www.blogjava.net/snoics

Web-Harvest
  
Web-Harvest是一个Java开源Web数据抽取工具。它能够收集指定的Web页面并从这些页面中提取有用的数据。Web-Harvest主要是运用了像XSLT,XQuery,正则表达式等这些技术来实现对text/xml的操作。
  
http://web-harvest.sourceforge.net

spiderpy
  
spiderpy是一个基于Python编码的一个开源web爬虫工具,允许用户收集文件和搜索网站,并有一个可配置的界面。
  
http://pyspider.sourceforge.net/

The Spider Web Network Xoops Mod Team
  
pider Web Network Xoops Mod是一个Xoops下的模块,完全由PHP语言实现。
  
http://www.tswn.com/