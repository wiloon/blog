---
title: RPC 远程过程调用 (Remote Procedure Call) 
author: "-"
date: 2011-12-14T10:10:45+00:00
url: rpc
categories:
  - Development
tags:
  - reprint
---
## RPC，Webservice，RMI，JMS

## RPC 远程过程调用 (Remote Procedure Call)

RPC 是远程过程调用 (Remote Procedure Call) 的缩写形式，Birrell 和 Nelson 在 1984 发表于 ACM Transactions on Computer Systems 的论文《Implementing remote procedure calls》对 RPC 做了经典的诠释。RPC 是指计算机 A 上的进程，调用另外一台计算机 B 上的进程，其中 A 上的调用进程被挂起，而 B 上的被调用进程开始执行，当值返回给 A 时，A 进程继续执行。调用方可以通过使用参数将信息传送给被调用方，而后可以通过传回的结果得到信息。而这一过程，对于开发人员来说是透明的。

RPC (Remote Procedure Call Protocol) ——远程过程调用协议，它是一种通过网络从远程计算机程序上请求服务，而不需要了解底层网络技术的协议。RPC协议假定某些传输协议的存在，如TCP或UDP，为通信程序之间携带信息数据。在OSI网络通信模型中，RPC跨越了传输层和应用层。RPC使得开发包括网络分布式多程序在内的应用程序更加容易。
  
RPC采用客户机/服务器模式。请求程序就是一个客户机，而服务提供程序就是一个服务器。首先，客户机调用进程发送一个有进程参数的调用信息到服务进程，然后等待应答信息。在服务器端，进程保持睡眠状态直到调用信息的到达为止。当一个调用信息到达，服务器获得进程参数，计算结果，发送答复信息，然后等待下一个调用信息，最后，客户端调用进程接收答复信息，获得进程结果，然后调用执行继续进行。
  
有多种 RPC模式和执行。最初由 Sun 公司提出。IETF ONC 宪章重新修订了 Sun 版本，使得 ONC RPC 协议成为 IETF 标准协议。现在使用最普遍的模式和执行是开放式软件基础的分布式计算环境 (DCE) 。

http://blog.csdn.net/mindfloating/article/details/39473807

http://blog.csdn.net/mindfloating/article/details/39474123

https://waylau.com/remote-procedure-calls/

[https://github.com/www1350/javaweb/issues/56](https://github.com/www1350/javaweb/issues/56)

RPC (Remote Procedure Call Protocol)

RPC使用C/S方式，采用http协议,发送请求到服务器，等待服务器返回结果。这个请求包括一个参数集和一个文本集，通常形成"classname.methodname"形式。优点是跨语言跨平台，C端、S端有更大的独立性，缺点是不支持对象，无法在编译器检查错误，只能在运行期检查。

你应该知道的rpc原理
  
一些开源的RPC框架 thrift，Finagle，dubbo，grpc，json-rpc等。
  
深入理解rpc
  
你的题目是RPC框架，首先了解什么叫RPC，为什么要RPC，RPC是指远程过程调用，也就是说两台服务器A，B，一个应用部署在A服务器上，想要调用B服务器上应用提供的函数/方法，由于不在一个内存空间，不能直接调用，需要通过网络来表达调用的语义和传达调用的数据。

比如说，一个方法可能是这样定义的:
  
Employee getEmployeeByName(String fullName)
  
那么:

首先，要解决通讯的问题，主要是通过在客户端和服务器之间建立TCP连接，远程过程调用的所有交换的数据都在这个连接里传输。连接可以是按需连接，调用结束后就断掉，也可以是长连接，多个远程过程调用共享同一个连接。
  
第二，要解决寻址的问题，也就是说，A服务器上的应用怎么告诉底层的RPC框架，如何连接到B服务器 (如主机或IP地址) 以及特定的端口，方法的名称名称是什么，这样才能完成调用。比如基于Web服务协议栈的RPC，就要提供一个endpoint URI，或者是从UDDI服务上查找。如果是RMI调用的话，还需要一个RMI Registry来注册服务的地址。
  
第三，当A服务器上的应用发起远程过程调用时，方法的参数需要通过底层的网络协议如TCP传递到B服务器，由于网络协议是基于二进制的，内存中的参数的值要序列化成二进制的形式，也就是序列化 (Serialize) 或编组 (marshal) ，通过寻址和传输将序列化的二进制发送给B服务器。
  
第四，B服务器收到请求后，需要对参数进行反序列化 (序列化的逆操作) ，恢复为内存中的表达方式，然后找到对应的方法 (寻址的一部分) 进行本地调用，然后得到返回值。
  
第五，返回值还要发送回服务器A上的应用，也要经过序列化的方式发送，服务器A接到后，再反序列化，恢复为内存中的表达方式，交给A服务器上的应用
  
image
  
 (图片来源: [https://www.cs.rutgers.edu/~pxk/417/notes/03-rpc.html](https://www.cs.rutgers.edu/~pxk/417/notes/03-rpc.html))

为什么RPC呢？就是无法在一个进程内，甚至一个计算机内通过本地调用的方式完成的需求，比如比如不同的系统间的通讯，甚至不同的组织间的通讯。由于计算能力需要横向扩展，需要在多台机器组成的集群上部署应用，

RPC的协议有很多，比如最早的CORBA，Java RMI，Web Service的RPC风格，Hessian，Thrift，甚至Rest API。

### 关于Netty

而Netty框架不局限于RPC，更多的是作为一种网络协议的实现框架，比如HTTP，由于RPC需要高效的网络通信，就可能选择以Netty作为基础。除了网络通信，RPC还需要有比较高效的序列化框架，以及一种寻址方式。如果是带会话 (状态) 的RPC调用，还需要有会话和状态保持的功能。

大体上来说，Netty就是提供一种事件驱动的，责任链式 (也可以说是流水线) 的网络协议实现方式。网络协议包含很多层次，很多部分组成，如传输层协议，编码解码，压缩解压，身份认证，加密解密，请求的处理逻辑，怎么能够更好的复用，扩展，业界通用的方法就是责任链，

一个请求应答网络交互通常包含两条链，一条链 (Upstream) 是从传输层，经过一系列步骤，如身份认证，解密，日志，流控，最后到达业务层，一条链 (DownStream) 是业务层返回后，又经过一系列步骤，如加密等，又回到传输层。
  
这样每一层都有一个处理接口，都可以进行不同的操作，比如身份认证，加解密，日志，流控，将不同的处理实现像拼积木那样插接起来就可以实现一个网络协议了 (快速开发) 。每一层都有自己的实现，上层不需要关注面向网络的操作 (可维护) 。Netty已经提供了很多实现。

当然Netty还有许多好处，比如对非阻塞IO (NIO) 的支持，比如在链上传递时最大程度的减少buffer的copy (高性能) 。

作者: 用心阁
  
链接: [http://www.zhihu.com/question/25536695/answer/36197244](http://www.zhihu.com/question/25536695/answer/36197244)
  
来源: 知乎

### Web Service

Web Service提供的服务是基于web容器的，底层使用http协议，类似一个远程的服务提供者，比如天气预报服务，对各地客户端提供天气预报，是一种请求应答的机制，是跨系统跨平台的。就是通过一个servlet，提供服务出去。

首先客户端从服务器的到WebService的WSDL，同时在客户端声称一个代理类(Proxy Class) 这个代理类负责与WebService

服务器进行Request 和Response 当一个数据 (XML格式的) 被封装成SOAP格式的数据流发送到服务器端的时候，就会生成一个进程对象并且把接收到这个Request的SOAP包进行解析，然后对事物进行处理，处理结束以后再对这个计算结果进行SOAP

包装，然后把这个包作为一个Response发送给客户端的代理类(Proxy Class)，同样地，这个代理类也对这个SOAP包进行解析处理，继而进行后续操作。这就是WebService的一个运行过程。

Web Service大体上分为5个层次:

Http传输信道
  
XML的数据格式
  
SOAP封装格式
  
WSDL的描述方式
  
UDDI UDDI是一种目录服务，企业可以使用它对Webservices进行注册和搜索
  
JAX-WS
  
CXF
  
jersey
  
Apache Axis2
  
SOA

SOA分为广义的SOA和狭义的SOA，广义的SOA是指一种新的企业应用架构和企业IT基础架构，它可以使企业实现跨应用，跨部门，跨企业甚至跨 行业之间的离散系统实现互连。 (注意: 这里所指的服务并不单单是Web Service,它可以是以Web Service实现 ，也可以以业务方式实现，甚至是书面口头承诺实现) 。而狭义的SOA是指一种软件架构，它可以根据需求通过网络对松散耦合的粗粒度应用组件进行分布式部 署、组合和使用。服务层是SOA的基础，可以直接被应用调用，从而有效控制系统中与软件代理交互的人为依赖性。
  
目前Web Service越来越流行，并成为实现SOA的一种手段。Web Service使应用功能通过标准化接口 (WSDL) 提供，使用标准化语言 (XML) 进行描述，并可基于标准化传输方式 (HTTP和JMS) 、采用标准化 协议 (SOAP) 进行调用，并使用XML SCHEMA方式对数据进行描述。你也可以不采用Web服务来创建SOA应用，但是这种标准的重要性日益增加、应用日趋普遍。

ESB企业服务总线

ESB是企业服务总线 (Enterprise Service Bus) 的缩写，是中间件技术与Web Service等技术结合的产物，也是SOA系统中的核心基础设施。ESB就是一个服务的中介，形成服务使用者->ESB服务Proxy->服务提供者的生物链，中介的作用在不同应用中各有不同:

解耦中介 : 客户对实际服务提供者的身份、物理位置、传输协议和接口定义都是不知道也不关心的，交互集成代码提取到了业务逻辑之外，由ESB平台进行中央的宣告式定义。ESB平台实现协议转换 (WebService，Http，JMS...)，消息转换 (转换、充实、过滤)，消息路由 (同步/异步、发布/订阅、基于内容路由、分支与聚合...)。
  
服务中介 : ESB平台作为中介提供服务交互中的基础服务。ESB平台实现SLA (可靠性保证，负载均衡，流量控制，缓存，事务控制，加密传输)，服务管理监控 (异常处理，服务调用及消息数据记录，系统及服务的状态监控，ESB配置管理)，统一安全管理 (这个有点理想主义)。
  
服务编排 : 多个服务进行编排形成新的服务。ESB支持一个直观的形式定义新组合服务的流程(工作流、BPEL 或 代码级编排)。
  
从上面可以看到ESB的基本功能仍然是数据传输，消息协议转化，路由三大核心功能。有这三大核心功能也可以看到在进行异构系统的整合时候往往根据需要ESB提供这些功能。没有ESB时候也可以实现SOA，比如借助SCA和BPEL来实现SOA，当时却很难实现消息协议转化和动态路由。

ESB在发展过程中有从原有的消息中间件转化为ESB产品的，这类消息中间件和数据总线产品在原有的EAI企业应用集成中应用比较多。而SOA根据强调了基于服务的集成，以Web Service服务为基本的管理单元。一个服务的定位是关于如何把业务逻辑表现成为一组相互独立的，自描述的且能互操作的实体。

对于SOA关注的是服务全生命周期，通过服务实现业务价值。而ESB关注的是服务中介和服务的集成，是SOA的基础设施。SOA有两个核心组件，一个是ESB，一个是BPEL，而ESB是基础设施，BPEL是业务流程驱动下服务的集成和整合。离开了SOA，ESB将失去它所连接的服务，而仅仅是一个总线，同时也将变得毫无价值。Bobby做了一个比喻: 路是没有任何价值的，除非你利用它把一个东西从一个地方移到另外一个地方。而离开SOA，ESB就像一个没人使用的道路。

做SOA的事情不要先上来建立一个大而全的ESB，相反是关注你的业务问题，找到用SOA的方法来解决业务上的需求，在解决这个问题的过程当中，你会看到一系列的业务服务。这些业务服务是会产生业务价值的。它可以灵活地组装，动态地解决你变化的业务需求。这是它的价值，只有这样才能使你的业务敏捷起来，随需应变起来。而在服务的组装过程中，你再去考虑利用ESB来把他们连接起来。
  
image
  
ESB 需要某种形式的服务路由目录 (service routing directory) 来路由服务请求。然而，SOA 可能还有单独的业务服务目录 (business service directory) ，其最基本的形式可能是设计时服务目录，用于在组织的整个开发活动中实现服务的重用。Web 服务远景在业务服务目录和服务路由目录的角色中都放置了一个 UDDI 目录，因而使得可以动态发现和调用服务。这样的目录可以视为 ESB 的一部分；然而，在这样的解决方案变得普遍之前，业务服务目录可能与 ESB 是分离的。

[http://www.cnblogs.com/zengxlf/p/3193529.html](http://www.cnblogs.com/zengxlf/p/3193529.html)

几者的区别与联系

### RPC与RMI

1. RPC 跨语言，而 RMI只支持Java。
2. RMI 调用远程对象方法，允许方法返回 Java 对象以及基本数据类型，而RPC 不支持对象的概念，传送到 RPC 服务的消息由外部数据表示 (External Data Representation, XDR) 语言表示，这种语言抽象了字节序类和数据类型结构之间的差异。只有由 XDR 定义的数据类型才能被传递， 可以说 RMI 是面向对象方式的 Java RPC 。
3. 在方法调用上，RMI中，远程接口使每个远程方法都具有方法签名。如果一个方法在服务器上执行，但是没有相匹配的签名被添加到这个远程接口上，那么这个新方法就不能被RMI客户方所调用。
4. 在RPC中，当一个请求到达RPC服务器时，这个请求就包含了一个参数集和一个文本值，通常形成"classname.methodname"的形式。这就向RPC服务器表明，被请求的方法在为 "classname"的类中，名叫"methodname"。然后RPC服务器就去搜索与之相匹配的类和方法，并把它作为那种方法参数类型的输入。这里的参数类型是与RPC请求中的类型是匹配的。一旦匹配成功，这个方法就被调用了，其结果被编码后返回客户方。

### JMS和RMI

采用JMS 服务，对象是在物理上被异步从网络的某个JVM 上直接移动到另一个JVM 上 (是消息通知机制)

而RMI 对象是绑定在本地JVM 中，只有函数参数和返回值是通过网络传送的 (是请求应答机制) 。

RMI一般都是同步的，也就是说，当client调用Server的一个方法的时候，需要等到对方的返回，才能继续执行client端，这个过程调用本地方法感觉上是一样的，这也是RMI的一个特点。

JMS 一般只是一个点发出一个Message到Message Server,发出之后一般不会关心谁用了这个message。

所以，一般RMI的应用是紧耦合，JMS的应用相对来说是松散耦合应用。

3. Webservice与RMI

RMI是在tcp协议上传递可序列化的java对象，只能用在java虚拟机上，绑定语言，客户端和服务端都必须是java

webservice没有这个限制，webservice是在http协议上传递xml文本文件，与语言和平台无关

4. Webservice与JMS

Webservice专注于远程服务调用，jms专注于信息交换。

大多数情况下Webservice是两系统间的直接交互 (Consumer <--> Producer) ，而大多数情况下jms是三方系统交互 (Consumer <- Broker -> Producer) 。当然，JMS也可以实现request-response模式的通信，只要Consumer或Producer其中一方兼任broker即可。

JMS可以做到异步调用完全隔离了客户端和服务提供者，能够抵御流量洪峰； WebService服务通常为同步调用，需要有复杂的对象转换，相比SOAP，现在JSON，rest都是很好的http架构方案； (举一个例子，电子商务的分布式系统中，有支付系统和业务系统，支付系统负责用户付款，在用户在银行付款后需要通知各个业务系统，那么这个时候，既可以用同步也可以用异步，使用异步的好处就能抵御网站暂时的流量高峰，或者能应对慢消费者。)

JMS是java平台上的消息规范。一般jms消息不是一个xml，而是一个java对象，很明显，jms没考虑异构系统，说白了，JMS就没考虑非java的东西。但是好在现在大多数的jms provider (就是JMS的各种实现产品) 都解决了异构问题。相比WebService的跨平台各有千秋吧。

[http://www.tuicool.com/articles/2qAzqq](http://www.tuicool.com/articles/2qAzqq)

什么是RESTful？

REST这个词，是Roy Thomas Fielding在他2000年的博士论文中提出的。有兴趣可以看看这里论文，谁是Fielding?点击前面名字了解。

那RESTful到底是什么呢？简单的讲，它是: 一种架构设计风格，提供了设计原则和约束条件，而不是架构。而满足这些约束条件和原则的应用程序或设计就是 RESTful架构或服务。

推荐阅读:  张善友博客——REST 入门介绍

infoq——深入浅出REST

第二个问题: 到底 REST 和 SOAP、RPC 有何区别？

这个问题比较大，要知道他们有什么区别首先需要明白，他们分别是什么？

REST上面已经简单的说明了它是什么。
  
SOAP(简单对象访问协议)是什么？SOAP是一种数据交换协议规范，是一种轻量的、简单的、基于XML的协议的规范。它有什么优点？简单总结为:  易用，灵活，跨语言，跨平台。
  
易用: 是因为它的消息是基于xml并封装成了符合http协议，因此,它符合任何路由器、 防火墙或代理服务器的要求。
  
灵活: 表现在极具拓展性，SOAP 无需中断已有的应用程序, SOAP 客户端、 服务器和协议自身都能发展。而且SOAP 能极好地支持中间介质和层次化的体系结构。
  
跨语言: soap可以使用任何语言来完成，只要发送正确的soap请求即可。
  
跨平台: 基于soap的服务可以在任何平台无需修改即可正常使用。
  
RPC(远程调用框架) 是一种允许分布式应用程序调用网络上不同计算机的可用服务的机制。涉猎不多，一下省略256个字。有熟悉的朋友可以在评论补充，然后我会修改到该内容中去
  
从上面我们可以看出，REST 和 SOAP、RPC 有何区别呢？没什么太大区别，他们的本质都是提供可支持分布式的基础服务，最大的区别在于他们各自的的特点所带来的不同应用场景。

REST可以看着是http协议的一种直接应用，默认基于json作为传输格式，使用简单，学习成本低效率高，但是安全性较低，而SOAP可以看着是一个重量级的协议，基于xml，SOAP在安全方面是通过使用XML-Security和XML-Signature两个规范组成了WS-Security来实现安全控制的，当前已经得到了各个厂商的支持，.net ，php ，java 都已经对其有了很好的支持 。这是REST薄弱的地方。

## RPC (Remote Procedure Call), RMI, Web Services, JMS

1. RPC: RPC本身没有规范,但基本的工作机制是一样的，即: serialization/deserialization + stub + skeleton, 宽泛的讲，只要能实现远程调用，都是RPC，如: rmi, .net-remoting, ws/soap/rest, hessian, xmlrpc, thrift, potocolbuffer

### RMI, Remote Method Invocation

RMI 是一种PRC. java的RMI就是java平台上的RPC技术方案。  
RMI是远程方法调用 (Remote Method Invocation) 的简称，其是一种计算机之间利用远程对象互相调用实现双方通讯的一种通讯机制，它能够让一个Java虚拟机上的对象调用另一个Java虚拟机上对象的方法。Java RMI在JDK1.1中实现的，其它可以被看作是RPC的Java版本。但是传统RPC并不能很好地应用于分布式对象系统。而Java RMI 则支持存储于不同地址空间的程序级对象之间彼此进行通信，实现远程对象之间的无缝远程调用。

RMI相对于其它比较复杂的RPC要简单的多 (比如 Thrift、Grpc、Protoff等) ，本文仅仅简单阐述了其组成、实现原理图、代码示例。如果想深入学习和了解，可以自行解读源码或参照其它解读文档。
  
局限性
  
相比于其它RPC(Thrift、Grpc等)，RMI存在许多的缺点:

RMI只能实现JAVA系统之间的调用，而WebService可以实现跨语言实现系统之间的调用。

RMI使用了JAVA默认的序列化方式，对于性能要求比较高的系统，可能需要其他的序列化方案来解决。

RMI服务在运行时难免会存在故障，例如，如果RMI服务无法连接了，就会导致客户端无法响应的现象。

RMI服务是基于远程接口提供的服务，一旦远程接口名称或者参数发生变化，客户端程序必须作出相应改变才能保证系统的稳定。

RMI 采用stubs 和 skeletons 来进行远程对象(remote object)的通讯。stub 充当远程对象的客户端代理，有着和远程对象相同的远程接口，远程对象的调用实际是通过调用该对象的客户端代理对象stub来完成的，通过该机制RMI就好比它是本地工作，采用tcp/ip协议，客户端直接调用服务端上的一些方法。优点是强类型，编译期可检查错误，缺点是只能基于JAVA语言，客户机与服务器紧耦合。

RMI TCP connection  
to feed a remote JMX client (in your case Java VisualVM) with data from JVM.
[https://stackoverflow.com/questions/40793580/what-is-rmi-tcp-connection](https://stackoverflow.com/questions/40793580/what-is-rmi-tcp-connection)

### JMS (Java Messaging Service)

JMS是Java的消息服务，JMS的客户端之间可以通过JMS服务进行异步的消息传输。JMS支持两种消息模型: Point-to-Point (P2P) 和Publish/Subscribe (Pub/Sub) ，即点对点和发布订阅模型。

3. JMS 是 java 平台上的消息规范。一般jms消息不是一个xml，而是一个java对象，很明显，jms没考虑异构系统，说白了，JMS就没考虑非java的东西。但是好在现在大多数的jms provider (就是JMS的各种实现产品) 都解决了异构问题。
4. soap 专注于远程服务调用，jms专注于信息交换。
5. 大多数情况下soap是两系统间的直接交互 (Consumer <-> Producer) ，而大多数情况下jms是三方系统交互 (Consumer <- Broker -> Producer) 。当然，JMS也可以实现request-response模式的通信，只要Consumer或Producer其中一方兼任broker即可。
6. 多数情况下，ws是同步的，jms是异步。虽然，ws也可以是异步的，而jms也可以是同步的。

## JAX-RPC

通过使用JAX-RPC (Java API for XML-based RPC)，已有的Java类或Java应用都能够被重新包装，并以Web Services的形式发布。JAX-RPC提供了将RPC参数(in/out)编码和解码的API，使开发人员可以方便地使用SOAP消息来完成RPC调用。同样，对于那些使用EJB(Enterprise JavaBeans)的商业应用而言，同样可以使用JAX-RPC来包装成Web服务，而这个Web Service的WSDL界面是与原先的EJB的方法是对应一致的。JAX-RPC为用户包装了Web服务的部署和实现，对Web服务的开发人员而言，SOAP/WSDL变得透明，这有利于加速Web服务的开发周期。

JAX-RPC (基于可扩展标记语言XML的远程过程调用的Java应用程序接口)是Java Web服务开发包(WSDP)的应用程序接口(API)，WSDP能使Java开发者在Web服务或其他的Web应用程序中包括远程过程调用(RPC)。JAX-RPC致力于要使应用程序或Web服务调用其他应用程序或Web服务变得更加容易。

JAX-RPC为基于SOAP(简单对象访问协议)的应用程序的开发提供了一个编程模型。JAX-RPC编程模型通过抽象SOAP协议层的运行机制与提供Java和Web服务描述语言(WSDL)间的映射服务来简化开发。

---

版权声明: 本文为CSDN博主「皮斯特劳沃」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: [https://blog.csdn.net/pistolove/article/details/64122191](https://blog.csdn.net/pistolove/article/details/64122191)
