---
title: web service
author: "-"
date: 2012-06-17T14:24:04+00:00
url: /?p=3545
categories:
  - Java
  - Web
tags:
  - reprint
---
## web service
http://www.cnblogs.com/hanlsheng/archive/2011/01/20/1940367.html

  第一章           设计一个简单的web service接口

本章主要内容:  你将学会如何设计一个简单的web service接口

1. 穿越网络提供跨平台操作

假设你想为大众或者业务伙伴提供一种这样的服务: 他们向你发送两个字符串，你把两个字符串进行连接，然后返回给他们。当然在现实世界中，你将提供一些更有用更复杂的服务。

此服务有几个必须满足的需求: 首先，用户可以使用不同的语言( 比如Java，C# 等)以及不同的平台( Windows，Linux等)。你提供的服务对于不同的语言和平台必须是可以访问的。第二，用户可以通过网络对你的服务进行访问。而且必须能够穿越防火墙。

给定了以上需求，最佳的解决方案是提供一个所谓的"web service"。比如，你可以在主机( www.ttdev.com)上提供可访问的web service( 通过/SimpleService 访问，见下图)，所以URL全称是: http: www.ttdev.com/SimpleService. 这被称为web service的"endpoint"( 终端，端点)。web service 可以支持一个或者多个操作。在这个例子中，一个操作被命名为"concat": 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg1.jpg" alt="" width="552" height="346" border="0" />

然而，你希望为你的每一个web service 操作提供全球唯一标识，这样别人也可以拥有名称为"concat"的操作。如何实现呢？很简单，你可以在名称"concat"前面声明一个"namespace"( 命名空间，比如http: ttdev.com/ss). namespace( 命名空间)的作用同java 中包的作用非常类似，只是表示形式不用而已，包的表示形式为 com.ttdev.foo。全球唯一标识是由namespace和操作名称组成的。Operation(操作)的名称,比如"concat"被称为local name( 本地名称)。全球唯一标识被称为QName( qualified name)。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg2.jpg" alt="" width="541" height="313" border="0" />

你可能想知道命名空间(如http: ttdev.com/ss)有什么含义。答案是:没有什么特别的含义。即使这个命名空间是一个URL，但不意味着你能通过浏览器进行访问会获得一个可访问页面。对你来说唯一重要的一点是，这个标识是全球唯一的。因为我已经注册了这个域名ttdev.com，所以它一定是全球唯一的。

值得注意的一点是， namespace (命名空间)与endpoint(终端，端点)是完全不同的概念。endpoint是真实的服务提供地点，而namespace仅仅是一个唯一标识符号。我可以轻易的把服务部署在另外的服务器上，这样web service将会有不同的 endpoint，但是 web service的操作唯一标识( 命名空间+本地名称)可以保持不变。

2.RPC 类型的web service

你的concat 操作将包含两个参数。一个名称为"s1"为string 类型。另一个名称为"s2"同样是string类型。返回值同样是一个string类型: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg3.jpg" alt="" width="521" height="165" border="0" />

然而，上图中的string 类型是什么含义呢？是Java的 string类型吗？不是，因为它必须是语言中立的。幸运的是，XML schema spec 定义了一些基本的数据类型，其中包括string类型。每一个数据类型都有一个QName 作为其id。比如: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg4.jpg" alt="" width="545" height="109" border="0" />

所以操作的接口可以如下表示: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg5.jpg" alt="" width="536" height="123" border="0" />

实际上，在web service中,一个方法调用被称为一个"input message"(输入消息),相应的方法参数被称为一个"part"(部分)。返回值被称为一个"output message"(输出消息)其中可能包含多个"part"。所以对于一个web service下图的描述更精确: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg6.jpg" alt="" width="539" height="178" border="0" />

当你调用这个operation(操作或者方法)时，即向web service 发送了一个XML element 作为 input message(输入消息)。如下图: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg7.jpg" alt="" width="539" height="387" border="0" />

当你获得一个返回，output message(输出消息)如下图所示: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg8.jpg" alt="" width="525" height="356" border="0" />

这一类型的web service 被称为"RPC类型"的web service( RPC指的是:"Remote Procedure Call"远程过程调用)。operation(操作)的QName 和part(部分)的名称被用来创建input和output messages( 输入和输出消息)。

3.文档类型的web service( Document style web service)

RP类型不是设计web service接口的唯一方式。比如，input message 只包含一个part(部分)，这个part( 部分)是一个schema中定义的元素。在schema，定义了一个名称为"concatRequest"的元素，它包含两个子元素<s1> 和<s2>:

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg9.jpg" alt="" width="565" height="452" border="0" />

注意: schema被包含在你的web service的接口中: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg10.jpg" alt="" width="533" height="380" border="0" />

就像以上所描述的一样，一part(部分)可以被声明为一个特定的元素(<concatRequest>在schema中定义，自定义)或者被声明为特定类型的任意元素( string由XML schema spec 内部定义)。在这两种情况下，part 都通过QName来指定。

当有人调用这个operation(操作)，他会向你发送一个<concatRequest>元素作为input message，如下: 
 
    <foo:concatRequest xmlns:foo="http:    ttdev.com/ss"><s1>abc</s1> 
    
    
      <s2>123</s2>
    
    
    
      </foo:concatRequest>
  
 
对于output message也类似，可以指定其仅仅包含一个part，这个part是一个<concatResponse> 元素: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg11.jpg" alt="" width="567" height="514" border="0" />

这种类型的web service 被称为"文档类型"的web service。文档类型的特点是，input message(输入消息)仅仅包含一个部分( part)，并且这个部分( part)是在schema中良好定义的。

对于output message( 输出消息)也一样。

如果现在回过头去看看RPC类型的web service 的input service，应该修订为以下形式: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg12.jpg" alt="" width="528" height="231" border="0" />

这是因为<foo:concat>,<s1>和<s2>没有在任何schema中定义，因此必须显示声明<s1>和<s2>的XML元素类型.

现在，让我们对RPC类型和文档类型的web service的input message(输入消息)作一个对比: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg13.jpg" alt="" width="564" height="239" border="0" />

没有太大不同，对吧？最明显的不同是RPC类型的不能通过schema进行验证，而文档类型( Document style)却可以。因此，文档类型的web service 是主要的应用方式在实践中。依据"WS-I"的要求，我们应该只使用文档类型的web services。 注:  WS-I 指的是 web service interoperability organization( web服务互操作组织)。

4.确定文档类型的web service的操作( operation)

访问文档类型的web service的operation(操作)，只需要发送input message的一个part(部分)即可。需要注意的是: 不是发送operation(操作)的名称。这样的话，如果在一个web service中有多个operation( 如下图所示)，如何确定哪一个operation被访问( call)呢？在下面这个例子中，通过检测input message(输入消息)是<concatRequest>还是<someElement>来确定。如果有两个operation都为<someElement>怎么办呢？那就是一个错误，服务将无法工作。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg14.jpg" alt="" width="468" height="324" border="0" />

5.Port 类型

实际上，web service 不会直接包含很多operation。而是把operation进行分组，分为一个或者更多个"port types"( port类型)。port 类型类似于Java中的class，每一个operation类似于Java 中的静态方法。比如，在上面的web service中，你可以拥有一个名称为stringUtil的port type 用以包含对string的操作，同理拥有一个名称为"dateUtil"的port type包好对日期的操作。需要注意的是port type的名称也必须是一个QName。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg15.jpg" alt="" width="549" height="334" border="0" />

6.绑定( Binding)

实际上，你可以使用不同的消息格式对port type进行访问。你已经见过的消息格式是"Simple Object Access Protocol( SOAP)"格式。也就是说，stringUtil的 port type 也可以支持普通文本格式: 

concat(s1='abc', s2='123')

除了消息格式，port type可以使得消息通过 http post请求或者通过邮件进行传输。每一个可用的组合被称为一个绑定( "binding"): 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg16.jpg" alt="" width="474" height="430" border="0" />

哪些绑定你的port type最常用呢？SOAP+HTTP是最常用的组合。在实践中，你应该使用最多。

7.端口( port)

设想有很多人使用你的web service，你决定使得你的web service可以在多台机器上均被访问到。比如看下图，你可以把绑定1( binding 1)部署到计算机c1，c2和c3上；把绑定2( binding2)部署在c3上。在这种情况下你拥有四个port。三个port用于绑定1，一个用于绑定2: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg17.jpg" alt="" width="521" height="422" border="0" />

这里需要注意的是，并不是说通过这三台计算机收到的请求被转发到另一后台计算机上进行处理。而是说，在三台计算上安装了一些软件，这些软件实现了port type。不同的计算机上没有强制要求安装一样的软件。比如，在c1上port1 可能是java实现，而在c2上port2可能是C#实现。非常重要的一点是以上两个port必须支持port type stringUtil指定的operation 和binding1指定的消息格式和传输协议。port4也必须实现相同的operation但是消息格式和传输协议是不同的。

把这种安排告知他人，在你的web service 的接口中包含了这些ports。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg18.jpg" alt="" width="505" height="384" border="0" />

8.目标命名空间( Target namespace)

你已经对operation的名称，port type的名称等使用了相同的namespace(命名空间)在这个web service中。它们是不是必须使用相同的命名空间呢？默认情况下，一个web service使用同一个命名空间。这就是所谓的"target namespace"目标命名空间。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg19.jpg" alt="" width="506" height="388" border="0" />

已经使用了http: ttdev.com/ss作为目标命名空间。这是个好的选择吗？根本上说，如果一个命名空间是全球唯一的那么就是良好的。所以这也是一个好的选择。然而，人们通常习惯于通过URL试着下载一个web页面。当使用http: ttdev.com/ss这个URL去下载页面时是无法工作的。这时他们就怀疑你的web service 是不是有故障啦。为避免这种混淆，你可以使用一个被称为URN(Uniform Resource Name)的作为namespace。

一个命名空间必须是一个URI，URI 是Uniform Resource Identifier的缩写。URI有两种表示形式。一种是URL比如http: www.foo.com/bar。另外一种表示就是URN。URN采用了这种格式: urn:<some-boject-type>:<some-object-id>.比如，International ISBN Agency( 国际isbn代理)向IANA( International Assigned Numbers Association)提交了一份请求，希望能管理名称为"isbn"的对象类型。请求被批准后，International ISBN Agency 就能声明一个URN (urn:isbn:1-23-456789-0)唯一的标识一本书，书的ISBN为1-23-456789-0.International ISBN Agency能够决定对象ID的含义而不用跟IANA协商( 因为请求被批准)。

同样，你可以向IANA提交一个申请用于注册你的internet域名，比如像foo.com。当被批准后，你就可以使用URNs ，比如urn:foo.com:xyz去唯一的标识一个对象xyz。xyz的含义和格式完全由你决定。比如你可以使用urn:foo.com:product:123 表示产品#123，或者urn:foo.com:patent/123标识一个专利代码。

尽管，这样会产生一些工作量。只要你已经注册了一个域名foo.com，其他人不可能在其URN's中使用。

一个XML 命名空间必须是一个URI。你可以使用URL或者URN。在作用上它们没有什么不同。比如，你可以使用urn:ttdev.com:ss代替http:    ttdev.com/ss作为你的目标命名空间，这对你的web service 一点儿影响都没有。

顺便提示下，如果你在URN上查询references，不要尝试去找像 "object type"或者"object id"的术语。官方术语是这样的: 

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg20.jpg" alt="" width="396" height="136" border="0" />

9.WSDL

到现在为止，你已经为你的web service 设计好了接口。

<img src="http://images.cnblogs.com/cnblogs_com/hanlsheng/jpg21.jpg" alt="" width="519" height="387" border="0" />

上图全面描述了你的web service。这个描述语言被称为"wsdl( web services Description Language)".

10.本章总结

web service 有三个特点: 1.语言中立2.平台中立3.可以通过网络访问。

一个web service 包括一个或者多个port。每一个port是一个部署在某一个网络地址上的binding。每一个binding是使用了特定的消息格式和消息传输协议的port type。

一个port type包含一个或者多个operation。一个operation包含一个input message 和一个output message。每一个message有一个或者多个part。每一个part要么是一个web

service 的schema中定义的元素要么就是schema中定义的元素。所有的这些信息都通过WSDL完全描述。

调用RPC类型的web service，要创建一个和operation同名的XML元素以及其子元素( 输入消息的part)。调用文档类型的web service，只需要发送输入消息。因为被用来

调用RPC类型web service的XML 元素没有在schema中定义。为了更好的可交互性，建议使用文档类型的web service。

web service,每一个port、binding、port type和operation都有一个QName用来唯一标识。QName 是由local name 和namespace组成的。xml namespace是一个URI，它是全球唯一的。默认情况下，这些组件的名称被放在web service的目标命名空间中。

有两种类型的URI: URL 和URN. URN的格式为: urn:<NID>:<NSS>.可以使用两种形式中的任何一种作为XML的命名空间。唯一不同的是URL被建议用过对象的地址而URN只是单纯的用于对象标识。

