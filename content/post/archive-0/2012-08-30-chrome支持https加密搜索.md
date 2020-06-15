---
title: chrome支持HTTPS加密搜索
author: wiloon
type: post
date: 2012-08-30T04:33:52+00:00
url: /?p=3971
categories:
  - Uncategorized

---
http://www.williamlong.info/archives/2186.html



https://www.google.com.hk/search?hl=zh-CN&q=%s



Google的官方博客曾经在上周发布消息称，Google会在下周部署HTTPS（超文本加密传输协议）加密技术的搜索方式，以确保搜索过程的安全性，Google没有食言，现在，HTTPS的Google搜索已经可以使用了。

Google在官方博客介绍说，普通的HTTP浏览是不安全的，用户和服务器之间的通讯会被第三方监听和干扰，对于Google来说，你在Google搜索的词语会被第三方截获，如果第三方不希望你在Google搜索这个词语，还可以通过技术手段阻止用户的搜索行为。

这也就是Google发布的beta版本的SSL加密搜索的原因，在HTTPS的Google搜索中，用户搜索的信息将无法被第三方获取，也不会出现数据泄漏的问题。目前HTTPS的Google搜索覆盖了Google网页搜索的部分产品，目前还不支持图片搜索和地图搜索，而其他搜素（资讯、博客、视频、动态等）都支持。

对于中国用户来说，HTTPS的加密搜索一劳永逸地解决了中国用户对于Google搜索的稳定性问题，我们知道，从某一天开始，一些常用的中文单字在Google中被屏蔽，搜索包含“吴”、“温”、“贾”、“李”、“习”、“贺”、“周”、“胡”等字的词语，会出现“连接被重置”，这导致一些很常用的词语，例如“学习”、“胡萝卜”、“温度计”等无法在Google搜索，而现在，使用HTTPS的Google，我们可以搜索你想搜索的任何词语，再也不会出现“连接被重置”了。

我早在2006年的时候就建议Google能支持HTTPS搜索，没想到要等这么多年才如愿所偿，HTTPS虽然较为耗费系统资源，但对于中国用户来说意义实在太大了。

为了你的用户隐私、安全和稳定性，现在就把你的Google搜索地址更换为 https://www.google.com 吧。

对于中国用户来说，如果你访问 https://www.google.com 自动跳转Google.com.hk，请点一下页面底部的Google.com in English，然后再访问https的Google即可使用。

Google Chrome浏览器默认在地址栏输入关键字即可搜索，默认是HTTP方式，我们可以设置地址栏默认Google HTTPS搜索的方法，右击地址栏-修改搜索引擎，点“添加”，加上信息: “https://www.google.com.hk/search?hl=zh-CN&q=%s”，如图所示，将其设置为默认即可，这样，我们在Google Chrome浏览器中就能默认使用Google HTTPS进行搜索了。