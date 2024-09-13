---
title: 从 HTTP GET 和 POST 的区别说起
author: "-"
date: 2012-06-03T11:45:35+00:00
url: http-get-post
categories:
  - Web
tags:
  - reprint
  - remix
---
## 从 HTTP GET 和 POST 的区别说起

HTTP 定义了与服务器交互的不同方法，最基本的方法是 GET 和 POST.

面试时得到的回答大多是: POST 是安全的，因为被提交的数据看不到，或者被加密的，其它的还有 GET 的时候中文出现乱码 (在地址栏里) ，数据最大长度限制等等。

说 POST 比 GET 安全肯定是错的，POST 跟 GET 都是明文传输，用[httpfox][2]等插件，或者像[WireShark ][3]等类似工具就能观察到。

POST 和 GET 的差别其实是很大的。语义上，GET 是获取指定URL上的资源，是读操作，重要的一点是不论对某个资源 GET 多少次，它的状态是不会改变的，
在这个意义上，我们说 GET 是安全的 (不是被密码学或者数据保护意义上的安全) 。因为 GET 是安全的，所以 GET 返回的内容可以被浏览器，
Cache 服务器缓存起来 (其中还有很多细节，但不影响这里的讨论) 。

而 POST 的语意是对指定资源"追加/添加"数据，所以是不安全的，每次提交的 POST，参与的代码都会认为这个操作会修改操作对象资源的状态，
于是，浏览器在你按下 F5 的时候会跳出确认框，缓存服务器不会缓存 POST 请求返回内容。

很遗憾到目前为止没有应聘者能够提到这一点。我猜测这背后的原因大概有两个，一是也许大多数人往往 (我也一样) 满足于只要完成任务就好，不管用哪个，
表单提交了，数据处理了，内容显示或者重新定向到另外一个页面，就算完成了一个任务，从任务表里划掉，结束。
而且对大部分项目(OA, CRM, MIS)的大部分情况下，用哪个似乎都可以。

同时，在被商业机构在媒体和书籍上宣传兜售的 WS-* 概念和使用集成开发环境提供的"方便"的代码生成工具后，"了解"到所有 Web 服务调用都是通过 POST，
更潜意识里确定了 POST 和 GET 是一样的，而且 GET 能做的，POST 都能做，POST 简直就是 GET++ 嘛。
自然，能用 POST 就用 POST，不必在乎两者的差别了。

这又让我想起最近学到的一个概念: Radius Of Comprehension，理解的半径:

当学习概念 A 的时候，需要先了解概念 B，而概念 C 又是理解 B 的前提。当 B 和 C 都是新的需要学习的概念时，可以说 A 的理解半径是 2，如图:

A --> B --> C
|--1--|--2--|

在学习 Web 开发时，接触到 GET 和 POS T时，"理解的半径"可能包涵:

```
POST vs. GET
     |---> Conditional GET -> ETag -> Cache
     |         --> Status Code
     ---> HTTP的方法 --> URL
```

往往因为仅仅满足于完成手上被要求的任务，或者懒于问一个为什么，我们就把自己的理解半径设置成零，那么就学不到更深入的东西，
也因此仅仅知道 POST 和 GET 不同，而不再会了解不同在哪里，什么是 Conditional GET 和缓存 header 等概念。

从一个简单的面试问题谈到这，貌似小题大作了，写到哪算哪吧。

看到Fenng [Buzz 了这篇文字][4]，引起一些评论，因此在这再讨论两个概念: [安全的(Safe)和幂等的(Idempotent)][5]。

安全的是指没有明显的对用户有影响的副作用(包括修改该资源的状态)。HTTP方法里的GET和HEAD都是安全的。

幂等的是指一个方法不论多少次操作，结果都是一样。PUT(把内容放到指定URL)，DELETE(删除某个URL代表的资源)，虽然都修改了资源内容，但多次操作，结果是相同的，因此和HEAD，GET一样都是幂等的。

所以根据HTTP协议，GET是安全的，也是幂等的，而POST既不是安全的，也不是幂等的。

[http://www.yining.org/2010/05/04/http-get-vs-post-and-thoughts/](http://www.yining.org/2010/05/04/http-get-vs-post-and-thoughts/)

[1]: http://twitter.com/yining/status/12993863581
[2]: http://code.google.com/p/httpfox/
[3]: http://www.wireshark.org/
[4]: http://www.google.com/buzz/dbanotes/BuxABaL5oam/%E4%BB%8EHTTP-GET%E5%92%8CPOST%E7%9A%84%E5%8C%BA%E5%88%AB%E8%AF%B4%E8%B5%B7-Yining
[5]: http://tools.ietf.org/html/rfc2616#section-9.1

## reference

- Zhang Yining / CC BY-NC-SA 3.0, http://www.yining.org/2010/05/04/http-get-vs-post-and-thoughts/
- RFC2616
- https://blog.csdn.net/gideal_wang/article/details/4316691

## HTTP POST GET 本质区别详解

[https://www.oschina.net/news/77354/http-get-post-differenthttp://blog.csdn.net/gideal_wang/article/details/4316691](https://www.oschina.net/news/77354/http-get-post-differenthttp://blog.csdn.net/gideal_wang/article/details/4316691)

一般在浏览器中输入网址访问资源都是通过GET方式；在FORM提交中，可以通过Method指定提交方式为GET或者POST，默认为GET提交

Http定义了与服务器交互的不同方法，最基本的方法有4种，分别是GET，POST，PUT，DELETE

URL全称是资源描述符，我们可以这样认 为: 一个URL地址，它用于描述一个网络上的资源，而HTTP中的GET，POST，PUT，DELETE就对应着对这个资源的查 ，改 ，增 ，删 4个操作。到这里，大家应该有个大概的了解了，GET一般用于获取/查询 资源信息，而POST一般用于更新 资源信息(个人认为这是GET和POST的本质区别，也是协议设计者的本意，其它区别都是具体表现形式的差异 )。

根据HTTP规范，GET用于信息获取，而且应该是安全的和幂等的 。

1. 所谓安全的意味着该操作用于获取信息而非修改信息。换句话说，GET请求一般不应产生副作用。就是说，它仅仅是获取资源信息，就像数据库查询一样，不会修改，增加数据，不会影响资源的状态。
   注意: 这里安全的含义仅仅是指是非修改信息。

2. 幂等的意味着对同一URL的多个请求应该返回同样的结果。这里我再解释一下幂等 这个概念:

幂等  (idempotent、idempotence) 是一个数学或计算机学概念，常见于抽象代数中。
幂等有以下几种定义:
对于单目运算，如果一个运算对于在范围内的所有的一个数多次进行该运算所得的结果和进行一次该运算所得的结果是一样的，那么我们就称该运算是幂等的。比如绝对值运算就是一个例子，在实数集中，有abs(a) =abs(abs(a)) 。
对于双目运算，则要求当参与运算的两个值是等值的情况下，如果满足运算结果与参与运算的两个值相等，则称该运算幂等，如求两个数的最大值的函数，有在在实数集中幂等，即max(x,x)  =  x 。

看完上述解释后，应该可以理解GET幂等的含义了。

但在实际应用中，以上2条规定并没有这么严格。引用别人文章的例子: 比如，新闻站点的头版不断更新。虽然第二次请求会返回不同的一批新闻，该操 作仍然被认为是安全的和幂等的，因为它总是返回当前的新闻。从根本上说，如果目标是当用户打开一个链接时，他可以确信从自身的角度来看没有改变资源即可。

根据HTTP规范，POST表示可能修改变服务器上的资源的请求 。继续引用上面的例子: 还是新闻以网站为例，读者对新闻发表自己的评论应该通过POST实现，因为在评论提交后站点的资源已经不同了，或者说资源被修改了。

上面大概说了一下HTTP规范中，GET和POST的一些原理性的问题。但在实际的做的时候，很多人却没有按照HTTP规范去做，导致这个问题的原因有很多，比如说:

1. 很多人贪方便，更新资源时用了GET，因为用POST必须要到FORM (表单) ，这样会麻烦一点。
2. 对资源的增，删，改，查操作，其实都可以通过GET/POST完成，不需要用到PUT和DELETE。
3. 另外一个是，早期的但是Web MVC框架设计者们并没有有意识地将URL当作抽象的资源来看待和设计 。还有一个较为严重的问题是传统的Web MVC框架基本上都只支持GET和POST两种HTTP方法，而不支持PUT和DELETE方法。

简单解释一下MVC: MVC本来是存在于Desktop程序中的，M是指数据模型，V是指用户界面，C则是控制器。使用MVC的目的是将M和V的实现代码分离，从而使同一个程序可以使用不同的表现形式。

以上3点典型地描述了老一套的风格 (没有严格遵守HTTP规范) ，随着架构的发展，现在出现REST(Representational State Transfer)，一套支持HTTP规范的新风格，这里不多说了，可以参考《RESTful Web Services》。

二 表现形式区别

搞清了两者的原理区别，我们再来看一下他们实际应用中的区别:

为了理解两者在传输过程中的不同，我们先看一下HTTP协议的格式:

HTTP请求:

在HTTP请求中，第一行必须是一个请求行 (request line) ，用来说明请求类型、要访问的资源以及使用的HTTP版本。紧接着是一个首部 (header) 小节，用来说明服务器要使用的附加信息。在首部之后是一个空行，再此之后可以添加任意的其他数据[称之为主体 (body) ]。

  GET与POST方法实例:
  GET /books/?sex=man&name=Professional HTTP/1.1
  Host: www.wrox.com
  User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6)
  Gecko/20050225 Firefox/1.0.1
  Connection: Keep-Alive

  POST / HTTP/1.1
  Host: www.wrox.com
  User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6)
  Gecko/20050225 Firefox/1.0.1
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 40
  Connection: Keep-Alive
  (--此处空一行--)
  name=Professional%20Ajax&publisher=Wiley

  有了以上对HTTP请求的了解和示例，我们再来看两种提交方式的区别:

  (1) GET提交，请求的数据会附在URL之后 (就是把数据放置在HTTP协议头中) ，以?分割URL和传输数据，多个参数用&连接；例如: login.action?name=hyddd&password=idontknow&verify=%E4%BD%A0 %E5%A5%BD。如果数据是英文字母/数字，原样发送，如果是空格，转换为+，如果是中文/其他字符，则直接把字符串用BASE64加密，得出如:  %E4%BD%A0%E5%A5%BD，其中％XX中的XX为该符号以16进制表示的ASCII。

  POST提交: 把提交的数据放置在是HTTP包的包体中。上文示例中红色字体标明的就是实际的传输数据

  因此，GET提交的数据会在地址栏中显示出来，而POST提交，地址栏不会改变

  (2)传输数据的大小: 首先声明: HTTP协议没有对传输的数据大小进行限制，HTTP协议规范也没有对URL长度进行限制。

  而在实际开发中存在的限制主要有:

  GET:特定浏览器和服务器对URL长度有限制，例如IE对URL长度的限制是2083字节(2K+35)。对于其他浏览器，如Netscape、FireFox等，理论上没有长度限制，其限制取决于操作系统的支持。

  因此对于GET提交时，传输数据就会受到URL长度的限制。

  POST:由于不是通过URL传值，理论上数据不受限。但实际各个WEB服务器会规定对post提交数据大小进行限制，Apache、IIS6都有各自的配置。

  (3)安全性:

  .POST的安全性要比GET的安全性高。注意: 这里所说的安全性和上面GET提到的"安全"不是同个概念。上面"安全"的含义仅仅是不作数据修改，而这 里安全的含义是真正的Security的含义，比如: 通过GET提交数据，用户名和密码将明文出现在URL上，因为(1)登录页面有可能被浏览器缓存， (2)其他人查看浏览器的历史纪录，那么别人就可以拿到你的账号和密码了，除此之外，使用GET提交数据还可能会造成Cross-site request forgery攻击, post 的安全性也只是相对的, post也是明文传输,用firebug, developer tool等插件就能观察到.

  (4) Http get,post,soap协议都是在http上运行的

1) get: 请求参数是作为一个key/value对的序列 (查询字符串) 附加到URL上的
   查询字符串的长度受到web浏览器和web服务器的限制 (如IE最多支持2048个字符) ，不适合传输大型数据集同时，它很不安全
2) post: 请求参数是在http标题的一个不同部分 (名为entity body) 传输的，这一部分用来传输表单信息，因此必须将Content-type设置为:application/x-www-form-urlencoded。post设计用来支持web窗体上的用户字段，其参数也是作为key/value对传输。
   但是: 它不支持复杂数据类型，因为post没有定义传输数据结构的语义和规则。
3) soap: 是http post的一个专用版本，遵循一种特殊的xml消息格式
   Content-type设置为: text/xml   任何数据都可以xml化

### HTTP响应

1．HTTP响应格式:
 <status line>

 <blank line>
 [<response-body>]

    在响应中唯一真正的区别在于第一行中用状态信息代替了请求信息。状态行 (status line) 通过提供一个状态码来说明所请求的资源情况。
  
  
    HTTP响应实例: 
  
  
    HTTP/1.1 200 OK
Date: Sat, 31 Dec 2005 23:59:59 GMT
Content-Type: text/html;charset=ISO-8859-1
Content-Length: 122
＜html＞
＜head＞
＜title＞Wrox Homepage＜/title＞
＜/head＞
＜body＞
＜!- body goes here -＞
＜/body＞
＜/html＞
2．最常用的状态码有:

    ◆200 (OK): 找到了该资源，并且一切正常。
◆304 (NOT MODIFIED): 该资源在上次请求之后没有任何修改。这通常用于浏览器的缓存机制。
◆401 (UNAUTHORIZED): 客户端无权访问该资源。这通常会使得浏览器要求用户输入用户名和密码，以登录到服务器。
◆403 (FORBIDDEN): 客户端未能获得授权。这通常是在401之后输入了不正确的用户名或密码。
◆404 (NOT FOUND): 在指定的位置不存在所申请的资源。

    四 完整示例: 
  
  
    例子: 
HTTP GET

    发送
  
  
    GET /DEMOWebServices2.8/Service.asmx/CancelOrder?UserID=string&PWD=string&OrderConfirmation=string HTTP/1.1
Host: api.efxnow.com

    回复
  
  
    HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
 <objPlaceOrderResponse xmlns="https://api.efxnow.com/webservices2.3">
 <Success>boolean</Success>
 <ErrorDescription>string</ErrorDescription>
 <ErrorNumber>int</ErrorNumber>
 <CustomerOrderReference>long</CustomerOrderReference>
 <OrderConfirmation>string</OrderConfirmation>
 <CustomerDealRef>string</CustomerDealRef>
 </objPlaceOrderResponse>

HTTP POST

发送

POST /DEMOWebServices2.8/Service.asmx/CancelOrder HTTP/1.1
Host: api.efxnow.com
Content-Type: application/x-www-form-urlencoded
Content-Length: length

    UserID=string&PWD=string&OrderConfirmation=string
  
  
    回复
  
  
    HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8
Content-Length: length

    <?xml version="1.0" encoding="utf-8"?>
 <objPlaceOrderResponse xmlns="https://api.efxnow.com/webservices2.3">
 <Success>boolean</Success>
 <ErrorDescription>string</ErrorDescription>
 <ErrorNumber>int</ErrorNumber>
 <CustomerOrderReference>long</CustomerOrderReference>
 <OrderConfirmation>string</OrderConfirmation>
 <CustomerDealRef>string</CustomerDealRef>
 </objPlaceOrderResponse>

    SOAP 1.2
  
  
    发送
  
  
    POST /DEMOWebServices2.8/Service.asmx HTTP/1.1
Host: api.efxnow.com
Content-Type: application/soap+xml; charset=utf-8
Content-Length: length

    <?xml version="1.0" encoding="utf-8"?>
 <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
 <soap12:Body>
 <CancelOrder xmlns="https://api.efxnow.com/webservices2.3">
 <UserID>string</UserID>
 <PWD>string</PWD>
 <OrderConfirmation>string</OrderConfirmation>
 </CancelOrder>
 </soap12:Body>
 </soap12:Envelope>

    回复
  
  
    HTTP/1.1 200 OK
Content-Type: application/soap+xml; charset=utf-8
Content-Length: length

    <?xml version="1.0" encoding="utf-8"?>
 <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
 <soap12:Body>
 <CancelOrderResponse xmlns="https://api.efxnow.com/webservices2.3">
 <CancelOrderResult>
 <Success>boolean</Success>
 <ErrorDescription>string</ErrorDescription>
 <ErrorNumber>int</ErrorNumber>
 <CustomerOrderReference>long</CustomerOrderReference>
 <OrderConfirmation>string</OrderConfirmation>
 <CustomerDealRef>string</CustomerDealRef>
 </CancelOrderResult>
 </CancelOrderResponse>
 </soap12:Body>
 </soap12:Envelope>

      两种最常用的 HTTP 方法是: GET 和 POST。
  
  
    
      什么是 HTTP？
    
    
    
      超文本传输协议 (HTTP) 的设计目的是保证客户机与服务器之间的通信。
    
    
    
      HTTP 的工作方式是客户机与服务器之间的请求-应答协议。
    
    
    
      web 浏览器可能是客户端，而计算机上的网络应用程序也可能作为服务器端。
    
    
    
      举例: 客户端 (浏览器) 向服务器提交 HTTP 请求；服务器向客户端返回响应。响应包含关于请求的状态信息以及可能被请求的内容。
  
  
    
      两种 HTTP 请求方法: GET 和 POST
    
    
    
      在客户机和服务器之间进行请求-响应时，两种最常被用到的方法是: GET 和 POST。
    
    
    
      
        GET - 从指定的资源请求数据。
      
      
        POST - 向指定的资源提交要被处理的数据
      
    
  
  
    
      GET 方法
    
    
    
      请注意，查询字符串 (名称/值对) 是在 GET 请求的 URL 中发送的: 
    
    
    /test/demo_form.asp?name1=value1&name2=value2
    
    
      有关 GET 请求的其他一些注释: 
    
    
    
      
        GET 请求可被缓存
      
      
        GET 请求保留在浏览器历史记录中
      
      
        GET 请求可被收藏为书签
      
      
        GET 请求不应在处理敏感数据时使用
      
      
        GET 请求有长度限制
      
      
        GET 请求只应当用于取回数据
      
    
  
  
    
      POST 方法
    
    
    
      请注意，查询字符串 (名称/值对) 是在 POST 请求的 HTTP 消息主体中发送的: 
    
    
    POST /test/demo_form.asp HTTP/1.1
Host: w3schools.com
name1=value1&name2=value2

      有关 POST 请求的其他一些注释: 
    
    
    
      
        POST 请求不会被缓存
      
      
        POST 请求不会保留在浏览器历史记录中
      
      
        POST 不能被收藏为书签
      
      
        POST 请求对数据长度没有要求
      
    
  
  
    
      比较 GET 与 POST
    
    
    
      下面的表格比较了两种 HTTP 方法: GET 和 POST。
    
    
    
      
        <th>
        </th>
        
        <th>
          GET
        </th>
        
        <th>
          POST
        </th>
      
      
      
        
          后退按钮/刷新
        
        
        
          无害
        
        
        
          数据会被重新提交 (浏览器应该告知用户数据会被重新提交) 。
        
      
      
      
        
          书签
        
        
        
          可收藏为书签
        
        
        
          不可收藏为书签
        
      
      
      
        
          缓存
        
        
        
          能被缓存
        
        
        
          不能缓存
        
      
      
      
        
          编码类型
        
        
        
          application/x-www-form-urlencoded
        
        
        
          application/x-www-form-urlencoded 或 multipart/form-data。为二进制数据使用多重编码。
        
      
      
      
        
          历史
        
        
        
          参数保留在浏览器历史中。
        
        
        
          参数不会保存在浏览器历史中。
        
      
      
      
        
          对数据长度的限制
        
        
        
          是的。当发送数据时，GET 方法向 URL 添加数据；URL 的长度是受限制的 (URL 的最大长度是 2048 个字符) 。
        
        
        
          无限制。
        
      
      
      
        
          对数据类型的限制
        
        
        
          只允许 ASCII 字符。
        
        
        
          没有限制。也允许二进制数据。
        
      
      
      
        
          安全性
        
        
        
          与 POST 相比，GET 的安全性较差，因为所发送的数据是 URL 的一部分。 
          
          
            在发送密码或其他敏感信息时绝不要使用 GET ！ 
            
            
              POST 比 GET 更安全，因为参数不会被保存在浏览器历史或 web 服务器日志中。
             
            
            
              
                可见性
              
              
              
                数据在 URL 中对所有人都是可见的。
              
              
              
                数据不会显示在 URL 中。
              
               
            
            
              
                其他 HTTP 请求方法
              
              
              
                下面的表格列出了其他一些 HTTP 请求方法: 
              
              
              
                
                  <th>
                    方法
                  </th>
                  
                  <th>
                    描述
                  </th>
                
                
                
                  
                    HEAD
                  
                  
                  
                    与 GET 相同，但只返回 HTTP 报头，不返回文档主体。
                  
                
                
                
                  
                    PUT
                  
                  
                  
                    上传指定的 URI 表示。
                  
                
                
                
                  
                    DELETE
                  
                  
                  
                    删除指定资源。
                  
                
                
                
                  
                    OPTIONS
                  
                  
                  
                    返回服务器支持的 HTTP 方法。
                  
                
                
                
                  
                    CONNECT
                  
                  
                  
                    把请求连接转换到透明的 TCP/IP 通道。
                  
                
              
              
              
                
              
              
              
                http://www.w3school.com.cn/tags/html_ref_httpmethods.asp

## GET与POST区别

HTTP 定义了与服务器交互的不同方法，最基本的方法是 GET 和 POST.

使用 Get 的时候，参数会显示在地址栏上

使用 Post 的时候, 因为可以在 request body 里传数据, 所以 post 请求一般不在 url 里传参数, 但是理论上 url 里是可以放参数的, 服务端也能正常收到.

HTTP-GET和HTTP-POST是使用HTTP的标准协议动词，用于编码和传送变量名/变量值对参数，并且使用相关的请求语义。
每个HTTP-GET和HTTP-POST都由一系列HTTP请求头组成，这些请求头定义了客户端从服务器请求了什么，而响应则是由一系列HTTP应答头和应答数据组成，
如果请求成功则返回应答。
HTTP-GET以使用MIME类型application/x-www-form-urlencoded的urlencoded文本的格式传递参数。
Urlencoding是一种字符编码，保证被传送的参数由遵循规范的文本组成，例如一个空格的编码是"%20"。附加参数还能被认为是一个查询字符串。
与HTTP-GET类似，HTTP-POST参数也是被URL编码的。然而，变量名/变量值不作为URL的一部分被传送，而是放在实际的HTTP请求消息内部被传送。

get 是从服务器上获取数据，post 是向服务器传送数据, 比如上传文件只能用 Post


在客户端，Get 方式在通过URL提交数据，数据在URL中可以看到；数据的按照variable=value的形式，添加到action所指向的URL后面，
并且两者使用"?"连接，而各个变量之间使用"&"连接；POST方式，数据放置在HTML HEADER内提交。



Get限制Form表单的数据集的值必须为ASCII字符；而Post支持整个ISO10646字符集。默认是用ISO-8859-1编码


Get是Form的默认方法。


get方法没有请求实体，含有数据的url都在请求头里面.



注: 所谓安全的意味着该操作用于获取信息而非修改信息。幂等的意味着对同一 URL 的多个请求应该返回同样的结果。完整的定义并不像看起来那样严格。
换句话说，GET 请求一般不应产生副作用。从根本上讲，其目标是当用户打开一个链接时，她可以确信从自身的角度来看没有改变资源。
比如，新闻站点的头版不断更新。虽然第二次请求会返回不同的一批新闻，该操作仍然被认为是安全的和幂等的，因为它总是返回当前的新闻。
反之亦然。POST 请求就不那么轻松了。POST 表示可能改变服务器上的资源的请求。
仍然以新闻站点为例，读者对文章的注解应该通过 POST 请求实现，因为在注解提交之后站点已经不同了 (比方说文章下面出现一条注解) 。

RFC2616 http://www.ietf.org/rfc/rfc2616.txt
