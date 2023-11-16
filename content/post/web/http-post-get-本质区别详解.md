---
title: HTTP POST GET 本质区别详解
author: "-"
date: 2012-06-03T13:11:53+00:00
url: /?p=3399
categories:
  - Java
  - Web
tags:
  - reprint
---
## HTTP POST GET 本质区别详解

[https://www.oschina.net/news/77354/http-get-post-differenthttp://blog.csdn.net/gideal_wang/article/details/4316691](https://www.oschina.net/news/77354/http-get-post-differenthttp://blog.csdn.net/gideal_wang/article/details/4316691)

一 原理区别

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
  
1.很多人贪方便，更新资源时用了GET，因为用POST必须要到FORM (表单) ，这样会麻烦一点。
  
    2.对资源的增，删，改，查操作，其实都可以通过GET/POST完成，不需要用到PUT和DELETE。
  
    3.另外一个是，早期的但是Web MVC框架设计者们并没有有意识地将URL当作抽象的资源来看待和设计 。还有一个较为严重的问题是传统的Web MVC框架基本上都只支持GET和POST两种HTTP方法，而不支持PUT和DELETE方法。
  
* 简单解释一下MVC: MVC本来是存在于Desktop程序中的，M是指数据模型，V是指用户界面，C则是控制器。使用MVC的目的是将M和V的实现代码分离，从而使同一个程序可以使用不同的表现形式。
  
    以上3点典型地描述了老一套的风格 (没有严格遵守HTTP规范) ，随着架构的发展，现在出现REST(Representational State Transfer)，一套支持HTTP规范的新风格，这里不多说了，可以参考《RESTful Web Services》。
  
    二 表现形式区别
  
    搞清了两者的原理区别，我们再来看一下他们实际应用中的区别:
  
    为了理解两者在传输过程中的不同，我们先看一下HTTP协议的格式:
  
    HTTP请求:
  
    <request line>
  
    <blank line>
  
    <request-body>]
  
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
