---
title: location.reload() 和 location.replace()
author: "-"
date: 2013-07-12T07:15:14+00:00
url: /?p=5645
categories:
  - Uncategorized

tags:
  - reprint
---
## location.reload() 和 location.replace()

首先介绍两个方法的语法:

 语法:  location.reload([bForceGet])                                                                                                                           参数:  _bForceGet_, 可选参数, 默认为 false,从客户端缓存里取当前页。                                                                  true, 则以 GET 方式,从服务端取最新的页面, 相当于客户端点击 F5("刷新")

replace 方法,该方法通过指定URL替换当前缓存在历史里 (客户端) 的项目,因此当使用replace方法之后,你不能通过"前进"和"后退"来访问已经被替换的URL。
 语法:  location.replace(URL)                                                                                                      参数:  URL

在实际应用的时候,重新刷新页面的时候,我们通常使用:  location.reload() 或者是 history.go(0) 来做。因为这种做法就像是客户端点F5刷新页面,所以页面的method="post"的时候,会出现"网页过期"的提示。那是因为Session的安全保护机制。可以想到:  当调用 location.reload() 方法的时候, aspx页面此时在服务端内存里已经存在, 因此必定是 IsPostback 的。如果有这种应用:  我们需要重新加载该页面,也就是说我们期望页面能够在服务端重新被创建, 我们期望是 Not IsPostback 的。这里,location.replace() 就可以完成此任务。被replace的页面每次都在服务端重新生成。你可以这么写:  location.replace(location.href)

><http://blog.csdn.net/fangxinggood/article/details/604916>
