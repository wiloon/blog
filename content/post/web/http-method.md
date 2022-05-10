---
author: "-"
date: "" 
title: "http method, get, head, post, options, put, delte, trace, connect"

categories:
  - inbox
tags:
  - reprint
---
## "http method, get, head, post, options, put, delte, trace, connect"

<https://www.cnblogs.com/machao/p/5788425.html>

前言
HTTP Method的历史:

HTTP 0.9 这个版本只有GET方法
HTTP 1.0 这个版本有GET HEAD POST这三个方法
HTTP 1.1 这个版本是当前版本，包含GET HEAD POST OPTIONS PUT DELETE TRACE CONNECT 这8个方法
我们先看看HTTP 1.1 规范的中文翻译

方法定义 (Method Definitions)
HTTP/1.1常用方法的定义如下。虽然方法可以被展开，但新加的方法不能认为能分享与扩展的客户端和服务器同样的语义。

Hst请求头域 (见13.23节) 必须能在所有的HTTP/1.1请求里出现。

9.1 安全和等幂 (Idempotent) 方法
9.1.1 安全方法 (Safe Methods)
实现者应当知道软件是代表用户在互联网上进行交互，并且应该小心地允许用户知道任何它们可能采取的动作(action)，这些动作可能给他们自己或他人带来无法预料的结果。

特别的，GET和HEAD方法仅仅应该获取资源而不是执行动作 (action) 。这些方法应该被考虑是"安全"的。可以让用户代理用其他的方法，如: POST，PUT，DELETE，这样用户代理就能知道这些方法可能会执行不安全的动作。

自然的，保证当服务器由于执行GET请求而不能产生副作用是不可能的；实际上，一些动态的资源会考虑这个特性。用户并没有请求这些副作用，因此不需要对这些副作用负责。

9.1.2等幂方法 (Idempotent Mehtods)
方法可以有等幂的性质因为 (除了出错或终止问题) N>0个相同请求的副作用同单个请求的副作用的效果是一样 (译注: 等幂就是值不变性，相同的请求得到相同的响应结果，不会出现相同的请求出现不同的响应结果) 。方法GET，HEAD，PUT，DELETE都有这种性质。同样，方法OPTIONS和TRACE不应该有副作用，因此具有内在的等幂性。然而，有可能几个请求的序列是不等幂的，即使在那样的序列中所有方法都是等幂的。 (如果整个序列整体的执行的结果总是相同的，并且此结果不会因为序列的整体，部分的再次执行而改变，那么此序列是等幂的。) 例如，一个序列是非等幂的如果它的结果依赖于一个值，此值在以后相同的序列里会改变。

根据定义，一个序列如果没有副作用，那么此序列是等幂的 (假设在资源集上没有并行的操作) 。

### OPTIONS (选项)

OPTIONS方法表明请求想得到请求/响应链上关于此请求里的URI (Request-URI) 指定资源的通信选项信息。此方法允许客户端去判定请求资源的选项和/或需求，或者服务器的能力，而不需要利用一个资源动作 (译注: 使用POST，PUT，DELETE方法) 或一个资源获取 (译注: 用GET方法) 方法。

这种方法的响应是不能缓存的.。

如果OPTIONS请求消息里包括一个实体主体 (当请求消息里出现Content-Length或者Transfer-Encoding头域时) ，那么媒体类型必须通过Content-Type头域指明。虽然此规范没有定义如何使用此实体主体，将来的HTTP扩展可能会利用OPTIONS请求的消息主体去得到服务器得更多信息。一个服务器如果不支持OPTION请求的消息主体，它会遗弃此请求消息主体。

如果请求URI是一个星号 ('') ,，OPTIONS请求将会应用于服务器的所有资源而不是特定资源。因为服务器的通信选项通常依赖于资源，所以""请求只能在"ping"或者"no-op"方法时才有用；它干不了任何事情除了允许客户端测试服务器的能力。例如: 它能被用来测试代理是否遵循HTTP/1.1。

如果请求URI不是一个星号 ('*') ,，OPTIONS请求只能应用于请求URI指定资源的选项。

200响应应该包含任何指明选项性质的头域，这些选项性质由服务器实现并且只适合那个请求的资源 (例如，Allow头域) ，但也可能包一些扩展的在此规范里没有定义的头域。如果有响应主体的话也应该包含一些通信选项的信息。这个响应主体的格式并没有在此规范里定义，但是可能会在以后的HTTP里定义。内容协商可能被用于选择合适的响应格式。如果没有响应主体包含，响应就应该包含一个值为"0"的Content-Length头域。

Max-Forwards请求头域可能会被用于针对请求链中特定的代理。当代理接收到一个OPTIONS请求，且此请求的URI为absoluteURI，并且此请求是可以被转发的，那么代理必须要检测Max-Forwards头域。如果Max-Forwards头域的值为"0"，那么此代理不能转发此消息；而是，代理应该以它自己的通信选项响应。如果Max-Forwards头域是比0大的整数值，那么代理必须递减此值当它转发此请求时。如果没有Max-Forwards头域出现在请求里，那么代理转发此请求时不能包含Max-Forwards头域。

### GET

GET方法意思是获取被请求URI (Request-URI) 指定的信息 (以实体的格式) 。如果请求URI涉及到一个数据生成过程，那么这个生成的数据应该被作为实体在响应中返回，但这并不是过程的资源文本，除非资源文本恰好是过程的输出 (译注: URI指示的资源是动态生成的) 。

如果请求消息包含 If-Modified-Since,，If-Unmodified-Since，If-Match,，If-None-Match,或者 If-Range头域,，GET的语义将变成"条件 (conditionall)  GET"。一个条件GET方法会请求满足条件头域的实体。条件GET方法的目的是为了减少不必要的网络使用，这通过利用缓存的实体的更新，从而不用多次请求或传输客户已经拥有的数据。.

如果请求方法包含一个Range头域，那么GET方法就变成"部分Get"方法。一个部分GET会请求实体的一部分，这在14.35节里描述了。 部分GET方法的目的是为了减少不必要的网络使用，这通过允许获取部分实体，从而不需要传输客户端已经拥有的数据。

GET请求的响应是可缓存的 (cacheable) 如果此响应满足第13节HTTP缓存的要求。

看15.1.3节关于GET请求用于表单时安全考虑。

### HEAD

HEAD方法和GET方法一致，除了服务器不能在响应里返回消息主体。HEAD请求响应里HTTP头域里的元信息应该和GET请求响应里的元信息一致。此方法被用来获取请求实体的元信息而不需要传输实体主体 (entity-body) 。此方法经常被用来测试超文本链接的有效性，可访问性，和最近的改变。.

HEAD请求的响应是可缓存的，因为响应里的信息可能被用于更新以前的那个资源的缓存实体.。如果出现一个新的域值指明了缓存实体和当前源服务器上实体的不同 (可能因为Content-Length，Content-MD5，ETag或Last-Modified值的改变) ，那么缓存 (cache) 必须认为此缓存项是过时的 (stale) 。

### POST

POST 方法被用于请求源服务器接受请求中的实体作为请求资源的一个新的从属物。POST被设计涵盖下面的功能。

-已存在的资源的注释；

-发布消息给一个布告板，新闻组，邮件列表，或者相似的文章组。

-提供一个数据块，如提交一个表单给一个数据处理过程。

-通过追加操作来扩展数据库。

POST方法的实际功能是由服务器决定的，并且经常依赖于请求URI (Request-URI) 。POST提交的实体是请求URI的从属物，就好像一个文件从属于一个目录，一篇新闻文章从属于一个新闻组，或者一条记录从属于一个数据库。

POST方法执行的动作可能不会对请求URI所指的资源起作用。在这种情况下，200 (成功) 或者204 (没有内容) 将是适合的响应状态，这依赖于响应是否包含一个描述结果的实体。

如果资源被源服务器创建，响应应该是201 (Created) 并且包含一个实体，此实体描述了请求的状态并且此实体引用了一个新资源和一个Location头域 (见14.30节) 。

POST方法的响应是可缓存的。除非响应里有Cache-Control或者Expires头域指示其响应不可缓存。然而，303 (见其他) 响应能被利用去指导用户代理 (agent) 去获得可缓存的响应。

POST 请求必须遵循8.2节里指明的消息传输需求。

参见15.1.3节关于安全性的考虑.

### PUT

PUT方法请求服务器去把请求里的实体存储在请求URI (Request-URI) 标识下。如果请求URI (Request-URI) 指定的的资源已经在源服务器上存在，那么此请求里的实体应该被当作是源服务器此URI所指定资源实体的修改版本。如果请求URI (Request-URI) 指定的资源不存在，并且此URI被用户代理 (user agent，译注: 用户代理可认为是客户浏览器) 定义为一个新资源，那么源服务器就应该根据请求里的实体创建一个此URI所标识下的资源。如果一个新的资源被创建了，源服务器必须能向用户代理 (user agent)  发送201 (已创建) 响应。如果已存在的资源被改变了，那么源服务器应该发送200 (Ok) 或者204 (无内容) 响应。如果资源不能根据请求URI创建或者改变，一个合适的错误响应应该给出以反应问题的性质。实体的接收者不能忽略任何它不理解的Content-* (如: Content-Range) 头域，并且必须返回501 (没有被实现) 响应。

如果请求穿过一个缓存 (cache) ，并且此请求URI (Request-URI) 指示了一个或多个当前缓存的实体，那么这些实体应该被看作是旧的。PUT方法的响应不应该被缓存。

POST方法和PUT方法请求最根本的区别是请求URI (Request-URI) 的含义不同。POST请求里的URI指示一个能处理请求实体的资源 (译注: 此资源可能是一段程序，如jsp里的servlet)  。此资源可能是一个数据接收过程，一个网关 (gateway，译注: 网关和代理服务器的区别是: 网关可以进行协议转换，而代理服务器不能，只是起代理的作用，比如缓存服务器其实就是一个代理服务器) ，或者一个单独接收注释的实体。而PUT方法请求里有一个实体一一用户代理知道URI意指什么，并且服务器不能把此请求应用于其他URI指定的资源。如果服务器期望请求被应用于一个不同的URI，那么它必须发送301 (永久移动了) 响应；用户代理可以自己决定是否重定向请求。

一个独立的资源可能会被许多不同的URI指定。如: 一篇文章可能会有一个URI指定当前版本，此URI区别于其文章其他特殊版本的URI。这种情况下，一个通用URI的PUT请求可能会导致其资源的其他URI被源服务器定义。

HTTP/1.1没有定义PUT方法对源服务器的状态影响。

PUT请求必须遵循8.2节中的消息传输要求。

除非特别指出，PUT方法请求里的实体头域应该被用于资源的创建或修改。

### DELETE (删除)

DELETE方法请求源服务器删除请求URI指定的资源。此方法可能会在源服务器上被人为的干涉 (或其他方法) 。客户端不能保证此操作能被执行，即使源服务器返回成功状态码。然而，服务器不应该指明成功除非它打算删除资源或把此资源移到一个不可访问的位置。

如果响应里包含描述成功的实体，响应应该是200 (Ok) ；如果DELETE动作没有通过，应该以202 (已接受) 响应；如果DELETE方法请求已经通过了，但响应不包含实体，那么应该以204 (无内容) 响应。

如果请求穿过缓存，并且请求URI (Request-URI) 指定一个或多个缓存当前实体，那么这些缓存项应该被认为是旧的。DELETE方法的响应是不能被缓存的。

### TRACE

TRACE方法被用于激发一个远程的，应用层的请求消息回路 (译注: TRACE方法让客户端测试到服务器的网络通路，回路的意思如发送一个请返回一个响应，这就是一个请求响应回路，) 。最后的接收者或者是接收请求里Max-Forwards头域值为0源服务器或者是代理服务器或者是网关。TRACE请求不能包含一个实体。

TRACE方法允许客户端知道请求链的另一端接收什么，并且利用那些数据去测试或诊断。Via头域值 (见14.45) 有特殊的用途，因为它可以作为请求链的跟踪信息。利用Max-Forwards头域允许客户端限制请求链的长度去测试一串代理服务器是否在无限回路里转发消息。

如果请求是有效的，响应应该在响应实体主体里包含整个请求消息，并且响应应该包含一个Content-Type头域值为"message/http"的头域。TRACE方法的响应不能不缓存。

### CONNECT  (连接)

HTTP1.1协议规范保留了CONNECT方法，此方法是为了能用于能动态切换到隧道的代理服务器 (proxy，译注: 可以为代理，也可以是代理服务器) 。

上边的内容对HTTP Method 说的已经很详细了，但幂等这个概念可能不太容易理解。下边我们就着重介绍下:

在 HTTP 协议中，CONNECT 方法可以开启一个客户端与所请求资源之间的双向沟通的通道。它可以用来创建隧道 (tunnel) 。

例如，CONNECT 可以用来访问采用了 SSL (en-US) (HTTPS)  协议的站点。客户端要求代理服务器将 TCP 连接作为通往目的主机隧道。之后该服务器会代替客户端与目的主机建立连接。连接建立好之后，代理服务器会面向客户端发送或接收 TCP 消息流。

### 幂等性

幂等的数学定义为

f(f(x)) = f(x)

在HTTP/1.1规范中幂等性的定义是:

Methods can also have the property of "idempotence" in that (aside from error or expiration issues) the side-effects of N > 0 identical requests is the same as for a single request.

从定义上看，HTTP方法的幂等性是指一次和多次请求某一个资源应该具有同样的副作用。幂等性属于语义范畴，正如编译器只能帮助检查语法错误一样，HTTP规范也没有办法通过消息格式等语法手段来定义它，这可能是它不太受到重视的原因之一。但实际上，幂等性是分布式系统设计中十分重要的概念，而HTTP的分布式本质也决定了它在HTTP中具有重要地位。

为什么需要幂等性呢？我们先从一个例子说起，假设有一个从账户取钱的远程API (可以是HTTP的，也可以不是) ，我们暂时用类函数的方式记为:

bool withdraw(account_id, amount)
withdraw的语义是从account_id对应的账户中扣除amount数额的钱；如果扣除成功则返回true，账户余额减少amount；如果扣除失败则返回false，账户余额不变。值得注意的是: 和本地环境相比，我们不能轻易假设分布式环境的可靠性。一种典型的情况是withdraw请求已经被服务器端正确处理，但服务器端的返回结果由于网络等原因被掉丢了，导致客户端无法得知处理结果。如果是在网页上，一些不恰当的设计可能会使用户认为上一次操作失败了，然后刷新页面，这就导致了withdraw被调用两次，账户也被多扣了一次钱。

这个问题的解决方案一是采用分布式事务，通过引入支持分布式事务的中间件来保证withdraw功能的事务性。分布式事务的优点是对于调用者很简单，复杂性都交给了中间件来管理。缺点则是一方面架构太重量级，容易被绑在特定的中间件上，不利于异构系统的集成；另一方面分布式事务虽然能保证事务的ACID性质，而但却无法提供性能和可用性的保证。

另一种更轻量级的解决方案是幂等设计。我们可以通过一些技巧把withdraw变成幂等的，比如:

int create_ticket()
bool idempotent_withdraw(ticket_id, account_id, amount)
create_ticket的语义是获取一个服务器端生成的唯一的处理号ticket_id，它将用于标识后续的操作。idempotent_withdraw和withdraw的区别在于关联了一个ticket_id，一个ticket_id表示的操作至多只会被处理一次，每次调用都将返回第一次调用时的处理结果。这样，idempotent_withdraw就符合幂等性了，客户端就可以放心地多次调用。

基于幂等性的解决方案中一个完整的取钱流程被分解成了两个步骤: 1.调用create_ticket()获取ticket_id；2.调用idempotent_withdraw(ticket_id, account_id, amount)。虽然create_ticket不是幂等的，但在这种设计下，它对系统状态的影响可以忽略，加上idempotent_withdraw是幂等的，所以任何一步由于网络等原因失败或超时，客户端都可以重试，直到获得结果。如图2所示:

和分布式事务相比，幂等设计的优势在于它的轻量级，容易适应异构环境，以及性能和可用性方面。在某些性能要求比较高的应用，幂等设计往往是唯一的选择。

HTTP的幂等性
Todd.log - a place to keep my thoughts on programming
理解HTTP幂等性

基于HTTP协议的Web API是时下最为流行的一种分布式服务提供方式。无论是在大型互联网应用还是企业级架构中，我们都见到了越来越多的SOA或RESTful的Web API。为什么Web API如此流行呢？我认为很大程度上应归功于简单有效的HTTP协议。HTTP协议是一种分布式的面向资源的网络应用层协议，无论是服务器端提供Web服务，还是客户端消费Web服务都非常简单。再加上浏览器、Javascript、AJAX、JSON以及HTML5等技术和工具的发展，互联网应用架构设计表现出了从传统的PHP、JSP、ASP.NET等服务器端动态网页向Web API + RIA (富互联网应用) 过渡的趋势。Web API专注于提供业务服务，RIA专注于用户界面和交互设计，从此两个领域的分工更加明晰。在这种趋势下，Web API设计将成为服务器端程序员的必修课。然而，正如简单的Java语言并不意味着高质量的Java程序，简单的HTTP协议也不意味着高质量的Web API。要想设计出高质量的Web API，还需要深入理解分布式系统及HTTP协议的特性。

幂等性定义

本文所要探讨的正是HTTP协议涉及到的一种重要性质: 幂等性(Idempotence)。在HTTP/1.1规范中幂等性的定义是:

Methods can also have the property of "idempotence" in that (aside from error or expiration issues) the side-effects of N > 0 identical requests is the same as for a single request.
从定义上看，HTTP方法的幂等性是指一次和多次请求某一个资源应该具有同样的副作用。幂等性属于语义范畴，正如编译器只能帮助检查语法错误一样，HTTP规范也没有办法通过消息格式等语法手段来定义它，这可能是它不太受到重视的原因之一。但实际上，幂等性是分布式系统设计中十分重要的概念，而HTTP的分布式本质也决定了它在HTTP中具有重要地位。

HTTP的幂等性

HTTP协议本身是一种面向资源的应用层协议，但对HTTP协议的使用实际上存在着两种不同的方式: 一种是RESTful的，它把HTTP当成应用层协议，比较忠实地遵守了HTTP协议的各种规定；另一种是SOA的，它并没有完全把HTTP当成应用层协议，而是把HTTP协议作为了传输层协议，然后在HTTP之上建立了自己的应用层协议。本文所讨论的HTTP幂等性主要针对RESTful风格的，不过正如上一节所看到的那样，幂等性并不属于特定的协议，它是分布式系统的一种特性；所以，不论是SOA还是RESTful的Web API设计都应该考虑幂等性。下面将介绍HTTP GET、DELETE、PUT、POST四种主要方法的语义和幂等性。

HTTP GET方法用于获取资源，不应有副作用，所以是幂等的。比如: GET <http://www.bank.com/account/123456，不会改变资源的状态，不论调用一次还是N次都没有副作用。请注意，这里强调的是一次和N次具有相同的副作用，而不是每次GET的结果相同。GET> <http://www.news.com/latest-news这个HTTP>请求可能会每次得到不同的结果，但它本身并没有产生任何副作用，因而是满足幂等性的。

HTTP DELETE方法用于删除资源，有副作用，但它应该满足幂等性。比如: DELETE <http://www.forum.com/article/4231，调用一次和N次对系统产生的副作用是相同的，即删掉id为4231>的帖子；因此，调用者可以多次调用或刷新页面而不必担心引起错误。

比较容易混淆的是HTTP POST和PUT。POST和PUT的区别容易被简单地误认为"POST表示创建资源，PUT表示更新资源"；而实际上，二者均可用于创建资源，更为本质的差别是在幂等性方面。在HTTP规范中对POST和PUT是这样定义的:

The POST method is used to request that the origin server accept the entity enclosed in the request as a new subordinate of the resource identified by the Request-URI in the Request-Line ...... If a resource has been created on the origin server, the response SHOULD be 201 (Created) and contain an entity which describes the status of the request and refers to the new resource, and a Location header.

The PUT method requests that the enclosed entity be stored under the supplied Request-URI. If the Request-URI refers to an already existing resource, the enclosed entity SHOULD be considered as a modified version of the one residing on the origin server. If the Request-URI does not point to an existing resource, and that URI is capable of being defined as a new resource by the requesting user agent, the origin server can create the resource with that URI.

POST所对应的URI并非创建的资源本身，而是资源的接收者。比如: POST <http://www.forum.com/articles的语义是在http://www.forum.com/articles下创建一篇帖子，HTTP响应中应包含帖子的创建状态以及帖子的URI。两次相同的POST请求会在服务器端创建两份资源，它们具有不同的URI；所以，POST方法不具备幂等性。而PUT所对应的URI>是要创建或更新的资源本身。比如: PUT <http://www.forum/articles/4231的语义是创建或更新ID为4231的帖子。对同一URI进行多次PUT的副作用和一次PUT是相同的；因此，PUT>方法具有幂等性。

在介绍了几种操作的语义和幂等性之后，我们来看看如何通过Web API的形式实现前面所提到的取款功能。很简单，用POST /tickets来实现create_ticket；用PUT /accounts/account_id/ticket_id&amount=xxx来实现idempotent_withdraw。值得注意的是严格来讲amount参数不应该作为URI的一部分，真正的URI应该是/accounts/account_id/ticket_id，而amount应该放在请求的body中。这种模式可以应用于很多场合，比如: 论坛网站中防止意外的重复发帖。

上面简单介绍了幂等性的概念，用幂等设计取代分布式事务的方法，以及HTTP主要方法的语义和幂等性特征。其实，如果要追根溯源，幂等性是数学中的一个概念，表达的是N次变换与1次变换的结果相同，有兴趣的读者可以从Wikipedia上进一步了解。

参考资料
<https://www.quora.com/What-is-the-history-of-HTTP-verbs-PUT-GET-POST-and-DELETE>
<http://www.cnblogs.com/weidagang2046/archive/2011/06/04/idempotence.html>
<http://www.360doc.com/content/15/1124/19/29350465_515532644.shtml>
<https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html>  
<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods/CONNECT>  
