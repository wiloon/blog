---
title: REST是什么？
author: lcf
date: 2012-11-07T06:08:16+00:00
url: /?p=4632
categories:
  - Uncategorized

tags:
  - reprint
---
## REST是什么？
概述
  
REST是英文Representational State Transfer的缩写，中文翻译: 表述性状态转移。

他是由Roy Thomas Fielding博士在他的论文 《Architectural Styles and the Design of Network-based Software Architectures》中提出的一个术语。

REST本身只是为分布式超媒体系统设计的一种架构风格，而不是标准。

基于Web的架构，实际上就是各种规范的集合，这些规范共同组成了Web架构。比如Http协议，比如客户端服务器模式，这些都是规范。每当我们在原有规范的基础上增加新的规范，  就会形成新的架构。而REST正是这样一种架构，他结合了一系列的规范，而形成了一种新的基于Web的架构风格。
  
传统的Web应用大都是B/S架构，它包括了如下一些规范: 

1. 客户－服务器

这种规范的提出，改善了用户接口跨多个平台的可移植性，并且通过简化服务器组件，改善了系统的可伸缩性。最为关键的是通过分离用户接口和数据存储这两个关注点，使得不同用户终端享受相同数据成为了可能。

2. 无状态性

无状态性是在客户－服务器约束的基础上添加的又一层规范。他要求通信必须在本质上是无状态的，即从客户到服务器的每个request都必须包含理解该 request所必须的所有信息。这个规范改善了系统的可见性 (无状态性使得客户端和服务器端不必保存对方的详细信息，服务器只需要处理当前 request，而不必了解所有的request历史) ，可靠性 (无状态性减少了服务器从局部错误中恢复的任务量) ，可伸缩性 (无状态性使得服务器端可以很容易的释放资源，因为服务器端不必在多个request中保存状态) 。同时，这种规范的缺点也是显而易见得，由于不能将状态数据保存在服务器上的共享上下文中，因此增加了在一系列request中发送重复数据的开销,严重的降低了效率。

3.缓存

为了改善无状态性带来的网络的低效性，我们填加了缓存约束。缓存约束允许隐式或显式地标记一个response中的数据，这样就赋予了客户端缓存 response数据的功能，这样就可以为以后的request共用缓存的数据，部分或全部的消除一部分交互，增加了网络的效率。但是用于客户端缓存了信息，也就同时增加了客户端与服务器数据不一致的可能，从而降低了可靠性。

B/S架构的优点是其部署非常方便，但在用户体验方面却不是很理想。为了改善这种情况，
  
我们引入了REST。
  
REST在原有的架构上增加了三个新规范: 统一接口，分层系统和按需代码。

1.统一接口
  
REST 架构风格的核心特征就是强调组件之间有一个统一的接口，这表现在REST世界里，网络上所有的事物都被抽象为资源，而REST就是通过通用的链接器接口对资源进行操作。这样设计的好处是保证系统提供的服务都是解耦的，极大的简化了系统，从而改善了系统的交互性和可重用性。并且REST针对Web的常见情况做了优化，使得REST接口被设计为可以高效的转移大粒度的超媒体数据，这也就导致了REST接口对其它的架构并不是最优的。

2.分层系统
  
分层系统规则的加入提高了各种层次之间的独立性，为整个系统的复杂性设置了边界，通过封装遗留的服务，使新的服务器免受遗留客户端的影响，这也就提高了系统的可伸缩性。

3.按需代码
  
REST允许对客户端功能进行扩展。比如，通过下载并执行applet或脚本形式的代码，来扩展客户端功能。但这在改善系统可扩展性的同时，也降低了可见性。所以它只是REST的一个可选的约束。

REST的设计准则
  
REST架构是针对Web应用而设计的，其目的是为了降低开发的复杂性，提高系统的可伸缩性。REST提出了如下设计准则: 

1. 网络上的所有事物都被抽象为资源 (resource) ；
  
2. 每个资源对应一个唯一的资源标识符 (resource identifier) ；
  
3.通过通用的连接器接口 (generic connector interface) 对资源进行操作；
  
4. 对资源的各种操作不会改变资源标识符；
  
5. 所有的操作都是无状态的 (stateless) 。

REST中的资源所指的不是数据，而是数据和表现形式的组合，比如"最新访问的10位会员"和"最活跃的10为会员"在数据上可能有重叠或者完全相同，而由于他们的表现形式不同，所以被归为不同的资源，这也就是为什么REST的全名是Representational State Transfer的原因。资源标识符就是URI(Uniform Resource Identifier)，不管是图片，Word还是视频文件，甚至只是一种虚拟的服务，也不管你是xml格式,txt文件格式还是其它文件格式，全部通过 URI对资源进行唯一的标识。

REST是基于Http协议的，任何对资源的操作行为都是通过Http协议来实现。以往的Web开发大多数用的都是Http协议中的GET和 POST方法，对其他方法很少使用，这实际上是因为对Http协议认识片面的理解造成的。Http不仅仅是一个简单的运载数据的协议，而是一个具有丰富内涵的网络软件的协议。他不仅仅能对互联网资源进行唯一定位，而且还能告诉我们如何对该资源进行操作。Http把对一个资源的操作限制在4个方法以内:  GET, POST,PUT和DELETE，这正是对资源CRUD操作的实现。由于资源和URI是一一对应的，执行这些操作的时候URI是没有变化的，这和以往的 Web开发有很大的区别。正由于这一点，极大的简化了Web开发，也使得URI可以被设计成更为直观的反映资源的结构，这种URI的设计被称作 RESTful的URI。这位开发人员引入了一种新的思维方式: 通过URL来设计系统结构。当然了，这种设计方式对一些特定情况也是不适用的，也就是说不是所有的URI都可以RESTful的。

REST 之所以可以提高系统的可伸缩性，就是因为它要求所有的操作都是无状态的。由于没有了上下文(Context)的约束，做分布式和集群的时候就更为简单，也可以让系统更为有效的利用缓冲池(Pool) 。并且由于服务器端不需要记录客户端的一系列访问，也减少了服务器端的性能。

使用REST架构
  
对于开发人员来说，关心的是如何使用REST架构，这里我们来简单谈谈这个问题。REST不仅仅是一种崭新的架构，它带来的更是一种全新的Web开发过程中的思维方式: 通过URL来设计系统结构。在REST中，所有的URL都对应着资源，只要URL的设计是良好的，那么其呈现的系统结构也就是良好的。这点和TDD (Test Driven Development)很相似，他是通过测试用例来设计系统的接口，每一个测试用例都表示一系列用户的需求。开发人员不需要一开始就编写功能，而只需要把需要实现的功能通过测试用例的形式表现出来即可。这个和REST中通过URL设计系统结构的方式类似，我们只需要根据需求设计出合理地URL，这些 URL不一定非要链接到指定的页面或者完成一些行为，只要它们能够直观的表现出系统的用户接口。根据这些URL，我们就可以方便的设计系统结构。从 REST架构的概念上来看，所有能够被抽象成资源的东西都可以被指定为一个URL，而开发人员所需要做的工作就是如何能把用户需求抽象为资源，以及如何抽象的精确。因为对资源抽象的越为精确，对REST的应用来说就越好。这个和传统MVC开发模式中基于Action的思想差别就非常大。设计良好的URL，不但对于开发人员来说可以更明确的认识系统结构，对使用者来说也方便记忆和识别资源，因为URL足够简单和有意义。按照以往的设计模式，很多URL后面都是一堆参数，对于使用者来说也是很不方便的。

既然REST这么好用，那么是不是所有的Web应用都能采取此种架构呢？答案是否定的。我们知道，直到现在为止，MVC(Model-View- Controller) 模式依然是Web开发最普遍的模式，绝大多数的公司和开发人员都采取此种架构来开发Web应用，并且其思维方式也停留于此。MVC模式由数据，视图和控制器构成，通过事件(Event)触发Controller来改变Model和View。加上Webwork,Struts等开源框架的加入，MVC开发模式已经相当成熟，其思想根本就是基于Action来驱动。从开发人员角度上来说，贸然接受一个新的架构会带来风险，其中的不确定因素太多。并且REST新的思维方式是把所有用户需求抽象为资源，这在实际开发中是比较难做到的，因为并不是所有的用户需求都能被抽象为资源，这样也就是说不是整个系统的结构都能通过REST的来表现。所以在开发中，我们需要根据以上2点来在REST和MVC中做出选择。我们认为比较好的办法是混用REST和MVC，因为这适合绝大多数的Web应用开发，开发人员只需要对比较容易能够抽象为资源的用户需求采取REST的开发模式，而对其它需求采取MVC开发即可。这里需要提到的就是ROR(Ruby on Rails)框架，这是一个基于Ruby语言的越来越流行的Web开发框架，它极大的提高了Web开发的速度。更为重要的是，ROR(从1.2版本起)框架是第一个引入REST做为核心思想的Web开发框架，它提供了对REST最好的支持，也是当今最成功的应用REST的Web开发框架。实际上，ROR的 REST实现就是REST和MVC混用，开发人员采用ROR框架，可以更快更好的构建Web应用。

对开发人员来说，REST不仅仅在Web开发上贡献了自己的力量，同时也让我们学到了如何把软件工程原则系统地应用于对一个真实软件的设计和评估上。

[基于REST架构的Web Service设计][1]

SOAP的Web Service解决方案虽然较为成熟，且安全性较好，但是使用门槛较高，在大并发情况下会有性能问题，在互联网上使用不太普及，因此并不太适合Web 2.0网站服务使用，目前大量的Web 2.0网站使用另外一种解决方案——REST。

**REST的架构设计**

REST (Representational State Transfer) 是一种轻量级的Web Service架构风格，其实现和操作明显比SOAP和XML-RPC更为简洁，可以完全通过HTTP协议实现，还可以利用缓存Cache来提高响应速度，性能、效率和易用性上都优于SOAP协议。

REST架构遵循了CRUD原则，CRUD原则对于资源只需要四种行为: Create (创建) 、Read (读取) 、Update (更新) 和Delete (删除) 就可以完成对其操作和处理。这四个操作是一种原子操作，即一种无法再分的操作，通过它们可以构造复杂的操作过程，正如数学上四则运算是数字的最基本的运算一样。

REST架构让人们真正理解我们的网络协议HTTP本来面貌，对资源的操作包括获取、创建、修改和删除资源的操作正好对应HTTP协议提供的GET、POST、PUT和DELETE方法，因此REST把HTTP对一个URL资源的操作限制在GET、POST、PUT和DELETE这四个之内。这种针对网络应用的设计和开发方式，可以降低开发的复杂性，提高系统的可伸缩性。

**REST的设计准则**

REST架构是针对Web应用而设计的，其目的是为了降低开发的复杂性，提高系统的可伸缩性。REST提出了如下设计准则: 

网络上的所有事物都被抽象为资源 (resource) ；

每个资源对应一个唯一的资源标识符 (resource identifier) ；

通过通用的连接器接口 (generic connector interface) 对资源进行操作；

对资源的各种操作不会改变资源标识符；

所有的操作都是无状态的 (stateless) 。

**使用REST架构**

对于开发人员来说，关心的是如何使用REST架构，这里我们来简单谈谈这个问题。REST不仅仅是一种崭新的架构，它带来的更是一种全新的Web开发过程中的思维方式: 通过URL来设计系统结构。REST是一套简单的设计原则、一种架构风格 (或模式) ，不是一种具体的标准或架构。REST有很多成功的使用案例，著名的Delicious和Flickr都提供基于REST风格的API使用，客户端调用也极其方便，下面是我用ASP写的一个很简单的REST举例，从中可以看出REST是多么的简单易用。

客户端代码: 


  
Private Function httpGet(url, method, data)
 Dim xmlhttp
 Set xmlhttp = Server.CreateObject("MSXML2.ServerXMLHTTP")
 xmlhttp.open method, url + "?" + data, False
 xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
 xmlhttp.setRequestHeader "Content-Length", Len(data)
 xmlhttp.send (Null)
 If (xmlhttp.Status = 200) Then httpGet = xmlhttp.responseText
 Set xmlhttp = Nothing
 End Function
  
  
    Private Function httpPost(url, method, data)
 Dim xmlhttp
 Set xmlhttp = Server.CreateObject("MSXML2.ServerXMLHTTP")
 xmlhttp.open method, url, False
 xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
 xmlhttp.setRequestHeader "Content-Length", Len(data)
 xmlhttp.send (data)
 If (xmlhttp.Status = 200) Then httpPost = xmlhttp.responseText
 Set xmlhttp = Nothing
 End Function
  
  
    Private Function httpPut(url, method, data)
 Dim xmlhttp
 Set xmlhttp = Server.CreateObject("MSXML2.ServerXMLHTTP")
 xmlhttp.open method, url, False
 xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
 xmlhttp.setRequestHeader "Content-Length", Len(data)
 xmlhttp.send (data)
 If xmlhttp.Status >= 400 And xmlhttp.Status <= 599 Then
 response.write " Error Occurred : " & xmlhttp.Status & " - " & xmlhttp.statusText
 Else
 response.write xmlhttp.responseText
 End If
 If (xmlhttp.Status = 200) Then httpPut = xmlhttp.responseText
 Set xmlhttp = Nothing
 End Function
  
  
    Private Function httpDelete(url, method, data)
 Dim xmlhttp
 Set xmlhttp = Server.CreateObject("MSXML2.ServerXMLHTTP")
 xmlhttp.open method, url + "?" + data, False
 xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
 xmlhttp.setRequestHeader "Content-Length", Len(data)
 xmlhttp.send (Null)
 If xmlhttp.Status >= 400 And xmlhttp.Status <= 599 Then
 response.write " Error Occurred : " & xmlhttp.Status & " - " & xmlhttp.statusText
 Else
 response.write xmlhttp.responseText
 End If
 If (xmlhttp.Status = 200) Then httpDelete = xmlhttp.responseText
 Set xmlhttp = Nothing
 End Function
  
  
    response.write httpPost("http://localhost/rest/service.asp", "POST", "do=POST")
 response.write httpGet("http://localhost/rest/service.asp", "GET", "do=GET")
 response.write httpPut("http://localhost/rest/service.asp", "PUT", "do=PUT")
 response.write httpDelete("http://localhost/rest/service.asp", "DELETE", "do=DELETE")
  

服务端代码: 


  Response.Write Request.ServerVariables("REQUEST_METHOD")
 If (Request.ServerVariables("REQUEST_METHOD")="GET") Then
 Response.Write "DO GET" + Request("do")
 ElseIf (Request.ServerVariables("REQUEST_METHOD")="POST") Then
 Response.Write "DO POST" + Request("do")
 ElseIf (Request.ServerVariables("REQUEST_METHOD")="PUT") Then
 Response.Write "DO PUT" + Request("do")
 ElseIf (Request.ServerVariables("REQUEST_METHOD")="DELETE") Then
 Response.Write "DO DELETE" + Request("do")
 End if

需要注意的是，IIS服务器默认是不支持ASP文件的PUT和DELETE操作，默认会返回"403 - Forbidden"错误，因此需要修改IIS的设置，修改方法是: 管理根据－IIS信息服务器－网站－属性－主目录－应用程序配置－配置－映射，选择ASP － 编辑 － 修改为全部动作。

关于更多关于REST方面的知识，建议阅读《RESTful Web Services》这本书。

 [1]: http://blog.csdn.net/lu7kang/article/details/5528295