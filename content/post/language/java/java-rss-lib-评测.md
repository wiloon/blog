---
title: java rss lib 评测
author: "-"
date: 2015-02-09T14:02:31+00:00
url: /?p=7335
categories:
  - Inbox
tags:
  - reprint
---
## java rss lib 评测
http://blog.csdn.net/zhaozexin/article/details/282333

前两天上新浪,看到新浪 RSS 频道开通,不容易啊,等了这么久。

我的目标是做一个简单的portlet,每次读取新浪的RSS站点显示最新的新闻条目。

花了一个下午,去sourceforge和google 上搜索 opensource 的 java rss lib,还真有不少 (顺便提一下,sourceforget的搜索真的很烂) 。简单过滤以后,觉得以下三个类库比较有搞头。Rome 、rssutils和rsslib4j。具体的评测如下: 

一. Rome
  
Rome 是 java.net 上的一个开源项目,现在的版本是0.5。为什么叫Rome呢,按它的介绍上的说法,有个"条条大路通罗马"的意思,有些RSS的意味。Rome可能是 sun 公司从自己某个子项目中抽离出来的,package和类的命名就象j2sdk一样感觉规范。功能上支持RSS的所有版本及 Atom 0.3(Atom是和RSS类似的一种内容聚合的方式)。Rome 本身是提供API和功能实现,其下独立出一个 rome-fetcher 项目,专门用来读取RSS内容。正和我意啊。
  
参照 fetcher 上的范例,解析 RSS 相当简单,代码片断如下: 

FeedFetcher fetcher = new HttpURLFeedFetcher();
  
SyndFeed feed = fetcher.retrieveFeed(feedUrl);
  
System.out.println(feedUrl + " has a title: " + new String(feed.getTitle().getBytes("iso8859-1"), "utf-8") + " and contains " + feed.getEntries().size() + " entries.");
  
for (Iterator iter = feed.getEntries().iterator(); iter.hasNext(); ) {
  
SyndEntry entry = (SyndEntry) iter.next();
  
System.out.println("" + entry.getTitle() + "[" + entry.getPublishedDate() + "]");
  
}

为什么用 new String(feed.getTitle().getBytes("iso8859-1"), "utf-8") 进行转码,是因为Rome来解析 新浪新闻 RSS的时候试图从 URLConnection 的 header 中得到编码信息,否则总是用 iso8859-1。而新浪的RSS response header 中不包含编码信息,所以要做一番转码。另外还有就是 entry.getPubDate() 也将返回null,因为Rome 用多种pattern 去试图解析时间信息,新浪的时间格式还是符合RFC822的,但是Rome 使用SimpleDateFormat 来解析时间,它忘记了一点,就是 SimpleDateFormat的解析是关联于 Locale 的,所以由于我本地locale是China,SimpleDateFormat的parse方法解析不出英文的时间字符。以上代码前加 Locale.setDefault(Locale.Englisth) 可以搞定,但总觉得不爽。

如果也不想转码的话,Rome 还提供了一个 XmlReader 的类,通过分析 header 和 xml 内容推断 encoding,修改 HttpURLFeedFetcher 的源码 :

// 改变 InputStreamReader , 换用 XmlReader
  
//InputStreamReader reader = new InputStreamReader(is, ResponseHandler.getCharacterEncoding(connection));
  
XmlReader reader = new XmlReader(connection);
  
SyndFeedInput input = new SyndFeedInput();
  
SyndFeed feed = input.build(reader);

那么中文不用转码也能正确显示了,不过修改源码后我再解析 百度新闻 RSS 的时候,底层的JDOM却会抱错说xml 格式不正确。也许Rome的开发者也遇到过这样的问题,所以才没有使用 XmlReader。

二. rssutils
  
它是一个工具包,sun 的 develope站点上有文章 RSS Utilities: A Tutorial 专门介绍用taglib 显示RSS内容,附带的可以下载这个工具包,但我从网上搜索不到它的出处,自然也无法看到它的源码。但从反编译的代码来看,也是sun公司内部高手所做,设计精巧,代码简练。实现一个handler,用sax的方式解析xml内容,handler内部用反射和javabean的机制构造RSS元素对象并赋值。代码片断如下: 

RssParser parser = new RssParserImpl();
  
Rss rss = parser.parse(new URL(url));
  
System.out.println(rss.getChannel().getTitle());
  
for (Iterator iter = rss.getChannel().getItems().iterator(); iter.hasNext();) {
  
Item item = (Item)iter.next();
  
System.out.println("" + item.getTitle() + " " + item.getPubDate());
  
}

如上所示,代码也是相当简单,没有转码的需求,时间也正确显示 (因为根本没做分析,当字符串直接返回) 。但是该工具包并非真正对外公布,代码中有些不严谨的地方,如System.out的输出,很不爽。而且如果 RSS 的 xml内容如果缺少部分不常用元素 ,它也会printStackTrace一大串,服了它了。另外还有一个大问题,就是当我用它解析 百度新闻 的时候,直接就报错: org.xml.sax.SAXParseException: 字符转换错误: "Unconvertible UTF-8 character beginning with 0xb0"。网上查了查,可能是 java 修改过的 UTF-8 和标准 UTF-8 些微不兼容导致。详情参看 Java 平台中的增补字符 一文。

三. rsslib4j
  
rsslib4j 是 sourceforget 上的项目,主页是 http://sourceforge.net/projects/rsslib4j,现在最新的版本是0.2,才0.2,可是开发状态却已经是稳定产品化了。同样支持所有RSS版本。
  
rsslib4j 解析 RSS 的方式和 rssutils 一样,我看了看源码,设计比较简单,代码可读性一般,大量使用if。代码片断如下: 

RSSHandler hand = new RSSHandler();
  
RSSParser.parseXmlFile(new URL(url), hand, false);
  
RSSChannel ch = hand.getRSSChannel();
  
System.out.println(ch.toString());
  
LinkedList lst = hand.getRSSChannel().getItems();
  
for (int i = 0; i < lst.size(); i++) {
  
RSSItem itm = (RSSItem) lst.get(i);
  
System.out.println(itm.toString());
  
}

看起来也是相当清晰易懂,执行结果也和rssutils一样,不过用它来解析 百度新闻 却不会出现 rssutils 的utf-8编码错误,真是奇怪,两者都是调JAXP的 SAXParser 。不过它的代码也有bug,不能解析出 channel 的一些信息,查看源码,有点简单逻辑错误,修正后解决。想写封email给项目开发者可惜英文不行,通过cvs去commit一下也嫌麻烦,作罢。

总结

Rome:
  
优 - 1) 可扩展性好,有前途。2) 功能强大,除了用来解析RSS,还可以聚合和构造RSS。
  
劣 - 1) 兼容性待加强,2) 绑定jdom。为什么不喜欢 jdom呢,因为它api 老变,还很绝,搞得不兼容。

rssutils:
  
优 - 1) 代码设计精妙,值得学习。2) 附带 taglib 实现,直接可在 jsp 中应用。
  
劣 - 1) 没有源码。 2) 兼容性有待加强。 3) 功能较弱,只能用来解析RSS,没有聚合和构造RSS功能。

rsslib4j:
  
优 - 1) 简单有效,体积小。2) 兼容性不错。
  
劣 - 1) 有小bug。2) 功能较弱,只能用来解析RSS,没有聚合和构造RSS功能。

编辑选择:  rsslib4j
  
我只用来读读新浪新闻,rsslib4j 够用就好,不过要自己修改和编译源码。