---
author: "-"
date: "2020-05-23T05:42:35Z"
title: "JWT, session"
categories:
  - Security
tags:
  - reprint
---
## "JWT, session"

>github.com/golang-jwt/jwt

背景知识: 

### Authentication和Authorization的区别: 

Authentication: 用户认证，指的是验证用户的身份，例如你希望以小A的身份登录，那么应用程序需要通过用户名和密码确认你真的是小A。

Authorization: 授权，指的是确认你的身份之后提供给你权限，例如用户小A可以修改数据，而用户小B只能阅读数据。

由于http协议是无状态的，每一次请求都无状态。当一个用户通过用户名和密码登录了之后，他的下一个请求不会携带任何状态，应用程序无法知道他的身份，那就必须重新认证。因此我们希望用户登录成功之后的每一次http请求，都能够保存他的登录状态。

目前主流的用户认证方法有基于token和基于session两种方式。

JWT和session ID也会暴露于未经防范的重放攻击

将JWT发布到特定的IP地址并使用浏览器指纹。

Local Storage

无状态 JWT (Stateless JWT) : 包含 Session 数据的 JWT Token。Session 数据将被直接编码进 Token 内。

有状态 JWT (Stateful JWT) : 包含 Session 引用或其 ID 的 JWT Token。Session 数据存储在服务端。

Session token (又称 Session cookie) : 标准的、可被签名的 Session ID，例如各类 Web 框架 (译者注: 包括 Laravel) 内已经使用了很久的 Session 机制。Session 数据同样存储在服务端。

————————————————

原文作者: Wi1dcard

转自链接: [https://learnku.com/articles/22616](https://learnku.com/articles/22616 "https://learnku.com/articles/22616")

版权声明: 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请保留以上作者信息和原文链接。

[https://juejin.im/post/5a437441f265da43294e54c3](https://juejin.im/post/5a437441f265da43294e54c3 "https://juejin.im/post/5a437441f265da43294e54c3")

聊一聊JWT与session

### 前言

认证和授权，其实吧简单来说就是:认证就是让服务器知道你是谁，授权就是服务器让你知道你什么能干，什么不能干，认证授权俩种方式: Session-Cookie与JWT，下面我们就针对这两种方案就行阐述。

### Session

##### 工作原理

当 client通过用户名密码请求server并通过身份认证后，server就会生成身份认证相关的 session 数据，并且保存在内存或者内存数据库。并将对应的 sesssion_id返回给client，client会把保存session_id (可以加密签名下防止篡改) 在cookie。此后client的所有请求都会附带该session_id (毕竟默认会把cookie传给server) ，以确定server是否存在对应的session数据以及检验登录状态以及拥有什么权限，如果通过校验就该干嘛干嘛，否则重新登录。

前端退出的话就清cookie。后端强制前端重新认证的话就清或者修改session。

![](https://user-gold-cdn.xitu.io/2017/12/27/160984b7052cf619?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

##### 优势
相比JWT，最大的优势就在于可以主动清除session了
session保存在服务器端，相对较为安全
结合cookie使用，较为灵活，兼容性较好
##### 弊端
cookie + session在跨域场景表现并不好
如果是分布式部署，需要做多机共享session机制，实现方法可将session存储到数据库中或者redis中
基于 cookie 的机制很容易被 CSRF
查询session信息可能会有数据库查询操作

##### session、cookie、sessionStorage、localstorage的区别

> session: 主要存放在服务器端，相对安全

> cookie: 可设置有效时间，默认是关闭浏览器后失效，主要存放在客户端，并且不是很安全，可存储大小约为4kb

> sessionStorage: 仅在当前会话下有效，关闭页面或浏览器后被清除

> localstorage: 除非被清除，否则永久保存

### JWT

JSON Web Token (JWT) 是一种开放标准 (RFC 7519) ，它定义了一种紧凑且独立的方式，可以将各方之间的信息作为JSON对象进行安全传输。该信息可以验证和信任，因为是经过数字签名的。

JWT基本上由.分隔的三部分组成，分别是头部，有效载荷和签名。 一个简单的JWT的例子，如下所示: 

     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ.ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs
    复制代码

如果你细致得去看的话会发现其实这是一个分为 3 段的字符串，段与段之间用 点号 隔开，在 JWT 的概念中，每一段的名称分别为: 

    Header.Payload.Signature
    复制代码

在字符串中每一段都是被 base64url 编码后的 JSON，其中 Payload 段可能被加密。

##### Header
JWT 的 Header 通常包含两个字段，分别是: typ(type) 和 alg(algorithm)。

* typ: token的类型，这里固定为 JWT
* alg: 使用的 hash 算法，例如: HMAC SHA256 或者 RSA

一个简单的例子: 

        {
          "alg": "HS256",
          "typ": "JWT"
        }
    复制代码

我们对他进行编码后是: 

        >>> base64.b64encode(json.dumps({"alg":"HS256","typ":"JWT"}))
        'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9'
    复制代码

##### Payload

JWT 中的 Payload 其实就是真实存储我们需要传递的信息的部分，例如正常我们会存储些用户 ID、用户名之类的。此外，还包含一些例如发布人、过期日期等的元数据。

但是，这部分和 Header 部分不一样的地方在于这个地方可以加密，而不是简单得直接进行 BASE64 编码。但是这里我为了解释方便就直接使用 BASE64 编码，需要注意的是，这里的 BASE64 编码稍微有点不一样，切确得说应该是 Base64UrlEncoder，和 Base64 编码的区别在于会忽略最后的 padding (=号) ，然后 '-' 会被替换成'_'。

举个例子，例如我们的 Payload 是: 

     {"user_id":"zhangsan"}
    复制代码

那么直接 Base64 的话应该是: 

        >>> base64.urlsafe_b64encode('{"user_id":"zhangsan"}')
        'eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ=='
    复制代码

然后去掉 = 号，最后应该是: 

      'eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ'
    复制代码

##### Signature

Signature 部分其实就是对我们前面的 Header 和 Payload 部分进行签名，保证 Token 在传输的过程中没有被篡改或者损坏，签名的算法也很简单，但是，为了加密，所以除了 Header 和 Payload 之外，还多了一个密钥字段，完整算法为: 

        Signature = HMACSHA256(
            base64UrlEncode(header) + "." +
            base64UrlEncode(payload),
            secret)
    复制代码

还是以前面的例子为例，

        base64UrlEncode(header)  =》 eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9
        base64UrlEncode(payload) =》 eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ
    复制代码

secret 就设为: "secret", 那最后出来的签名应该是: 

        >>> import hmac
        >>> import hashlib
        >>> import base64
        >>> dig = hmac.new('secret',     >>> msg="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ", 
                   digestmod=
        >>> base64.b64encode(dig.digest())
        'ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs='
    复制代码

将上面三个部分组装起来就组成了我们的 JWT token了，所以我们的

        {'user_id': 'zhangsan'}
    复制代码

的 token 就是: 

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ.ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs
    复制代码

##### 工作原理

1\.首先，前端通过Web表单将自己的用户名和密码发送到后端的接口。这一过程一般是一个HTTP POST请求。建议的方式是通过SSL加密的传输 (https协议) ，从而避免敏感信息被嗅探。

2\.后端核对用户名和密码成功后，将用户的id等其他信息作为JWT Payload (负载) ，将其与头部分别进行Base64编码拼接后签名，形成一个JWT。形成的JWT就是一个形同lll.zzz.xxx的字符串。

3\.后端将JWT字符串作为登录成功的返回结果返回给前端。前端可以将返回的结果保存在localStorage或sessionStorage上，退出登录时前端删除保存的JWT即可。

4\.前端在每次请求时将JWT放入HTTP Header中的Authorization位。(解决XSS和XSRF问题)

5\.后端检查是否存在，如存在验证JWT的有效性。例如，检查签名是否正确；检查Token是否过期；检查Token的接收方是否是自己 (可选) 。

6\.验证通过后后端使用JWT中包含的用户信息进行其他逻辑操作，返回相应结果。

![](https://user-gold-cdn.xitu.io/2017/12/27/1609867a8c834efe?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### JWTs vs. Sessions

##### 可扩展性
随着应用程序的扩大和用户数量的增加，你必将开始水平或垂直扩展。session数据通过文件或数据库存储在服务器的内存中。在水平扩展方案中，你必须开始复制服务器数据，你必须创建一个独立的中央session存储系统，以便所有应用程序服务器都可以访问。否则，由于session存储的缺陷，你将无法扩展应用程序。解决这个挑战的另一种方法是使用 sticky session。你还可以将session存储在磁盘上，使你的应用程序在云环境中轻松扩展。这类解决方法在现代大型应用中并没有真正发挥作用。建立和维护这种分布式系统涉及到深层次的技术知识，并随之产生更高的财务成本。在这种情况下，使用JWT是无缝的;由于基于token的身份验证是无状态的，所以不需要在session中存储用户信息。我们的应用程序可以轻松扩展，因为我们可以使用token从不同的服务器访问资源，而不用担心用户是否真的登录到某台服务器上。你也可以节省成本，因为你不需要专门的服务器来存储session。为什么？因为没有session！

注意: 如果你正在构建一个小型应用程序，这个程序完全不需要在多台服务器上扩展，并且不需要RESTful API的，那么session机制是很棒的。 如果你使用专用服务器运行像Redis那样的工具来存储session，那么session也可能会为你完美地运作！

##### 安全性

JWT签名旨在防止在客户端被篡改，但也可以对其进行加密，以确保token携带的claim 非常安全。JWT主要是直接存储在web存储 (本地/session存储) 或cookies中。 JavaScript可以访问同一个域上的Web存储。这意味着你的JWT可能容易受到XSS (跨站脚本) 攻击。恶意JavaScript嵌入在页面上，以读取和破坏Web存储的内容。事实上，很多人主张，由于XSS攻击，一些非常敏感的数据不应该存放在Web存储中。一个非常典型的例子是确保你的JWT不将过于敏感/可信的数据进行编码，例如用户的社会安全号码。

最初，我提到JWT可以存储在cookie中。事实上，JWT在许多情况下被存储为cookie，并且cookies很容易受到CSRF (跨站请求伪造) 攻击。预防CSRF攻击的许多方法之一是确保你的cookie只能由你的域访问。作为开发人员，不管是否使用JWT，确保必要的CSRF保护措施到位以避免这些攻击。

现在，JWT和session ID也会暴露于未经防范的重放攻击。建立适合系统的重放防范技术，完全取决于开发者。解决这个问题的一个方法是确保JWT具有短期过期时间。虽然这种技术并不能完全解决问题。然而，解决这个挑战的其他替代方案是将JWT发布到特定的IP地址并使用浏览器指纹。

注意: 使用HTTPS / SSL确保你的Cookie和JWT在客户端和服务器传输期间默认加密。这有助于避免中间人攻击！

##### RESTful API服务

现代应用程序的常见模式是从RESTful API查询使用JSON数据。目前大多数应用程序都有RESTful API供其他开发人员或应用程序使用。由API提供的数据具有几个明显的优点，其中之一就是这些数据可以被多个应用程序使用。在这种情况下，传统的使用session和Cookie的方法在用户认证方面效果不佳，因为它们将状态引入到应用程序中。

RESTful API的原则之一是它应该是无状态的，这意味着当发出请求时，总会返回带有参数的响应，不会产生附加影响。用户的认证状态引入这种附加影响，这破坏了这一原则。保持API无状态，不产生附加影响，意味着维护和调试变得更加容易。

另一个挑战是，由一个服务器提供API，而实际应用程序从另一个服务器调用它的模式是很常见的。为了实现这一点，我们需要启用跨域资源共享 (CORS) 。Cookie只能用于其发起的域，相对于应用程序，对不同域的API来说，帮助不大。在这种情况下使用JWT进行身份验证可以确保RESTful API是无状态的，你也不用担心API或应用程序由谁提供服务。

##### 性能

对此的批判性分析是非常必要的。当从客户端向服务器发出请求时，如果大量数据在JWT内进行编码，则每个HTTP请求都会产生大量的开销。然而，在会话中，只有少量的开销，因为SESSION ID实际上非常小。看下面这个例子: 

JWT有5个claim: 

    {
    
      "sub": "1234567890",
    
      "name": "Prosper Otemuyiwa",
    
      "admin": true,
    
      "role": "manager",
    
      "company": "Auth0"
    
    }
    复制代码

编码时，JWT的大小将是SESSION ID (标识符) 的几倍，从而在每个HTTP请求中，JWT比SESSION ID增加更多的开销。而对于session，每个请求在服务器上需要查找和反序列化session。

JWT通过将数据保留在客户端的方式以空间换时间。你应用程序的数据模型是一个重要的影响因素，因为通过防止对服务器数据库不间断的调用和查询来减少延迟。需要注意的是不要在JWT中存储太多的claim，以避免发生巨大的，过度膨胀的请求。

值得一提的是，token可能需要访问后端的数据库。特别是刷新token的情况。他们可能需要访问授权服务器上的数据库以进行黑名单处理。获取有关刷新token和何时使用它们的更多信息。另外，请查看本文，了解有关黑名单的更多信息([auth0.com/blog/blackl…](https://auth0.com/blog/blacklist-json-web-token-api-keys/))。

##### 下游服务

现代web应用程序的另一种常见模式是，它们通常依赖于下游服务。例如，在原始请求被解析之前，对主应用服务器的调用可能会向下游服务器发出请求。这里的问题是，cookie不能很方便地流到下游服务器，也不能告诉这些服务器关于用户的身份验证状态。由于每个服务器都有自己的cookie方案，所以阻力很大，并且连接它们也是困难的。JSON Web Token再次轻而易举地做到了！

##### 实效性

此外，无状态JWT的实效性相比session太差，只有等到过期才可销毁，而session则可手动销毁。

例如有个这种场景，如果JWT中存储有权限相关信息，比如当前角色为 admin，但是由于JWT所有者滥用自身权利，高级管理员将权利滥用者的角色降为 user。但是由于 JWT 无法实时刷新，必需要等到 JWT 过期，强制重新登录时，高级管理员的设置才能生效。

或者是用户发现账号被异地登录，然后修改密码，此时token还未过期，异地的账号一样可以进行操作包括修改密码。

但这种场景也不是没有办法解决，解决办法就是将JWT生成的token存入到redis或者数据库中，当用户登出或作出其他想要让token失效的举动，可通过删除token在数据库或者redis里面的对应关系来解决这个问题。

### node中使用JWT

我这个项目中使用的是JWT，使用方法如下: 

首先安装JWT库: 

    npm install jsonwebtoken
    复制代码

然后创建签名数据，生成token: 

    let jwt = require('jsonwebtoken');
    
    var token = jwt.sign({ name: '张三' }, 'shhhhh');
    console.log(token);
    复制代码

运行程序可以看到打印出来的内容类似这样: 

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoi5byg5LiJIiwiaWF0IjoxNDYyODgxNDM3fQ.uVWC2h0_r1F4FZ3qDLkGN5KoFYbyZrFpRJMONZrJJog
    复制代码

之后，对token字符串，可以这样解码: 

    let decoded=jwt.decode(token);
    console.log(decoded);
    复制代码

将打印出: 

    { name: '张三', iat: 1462881437 }
    复制代码

其中iat是时间戳，即签名时的时间 (注意: 单位是秒) 。

不过，一般我们不会使用decode方法，因为它只是简单的对claims部分的做base64解码。

我们需要的是验证claims的内容是否被篡改。

此时我们需要使用verify方法: 

    let decoded = jwt.verify(token, 'shhhhh');
    console.log(decoded);
    复制代码

虽然打印出的内容和decode方法是一样的。但是是经过校验的。

我们可以改变校验用的密钥，比如改为shzzzz，使之和加密时的密钥不一致。那么解码就会出现报错: 

    JsonWebTokenError: invalid signature
    复制代码

我们也可以偷偷修改token的claims或者header部分，会得到这样的报错: 

    JsonWebTokenError: invalid token
    复制代码

最后，根据自己的需求，决定是否需要将生成的token存入数据库或者redis，但建议不要存储用户密码等敏感信息。

### token刷新
https://zhuanlan.zhihu.com/p/52300092
https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/#silent_refresh
https://usthe.com/2018/04/%E7%AD%BE%E5%8F%91%E7%9A%84%E7%94%A8%E6%88%B7%E8%AE%A4%E8%AF%81token%E8%B6%85%E6%97%B6%E5%88%B7%E6%96%B0%E7%AD%96%E7%95%A5/
https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/


所以... JWT 适合做什么？
在本文之初，我就提到 JWT 虽然不适合作为 Session 机制，但在其它方面的确有它的用武之地。该主张依旧成立，JWT 特别有效的使用例子通常是作为一次性的授权令牌。

引用 JSON Web Token specification: 

JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties. [...] enabling the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC) and/or encrypted.

在此上下文中，「Claim」可能是一条「命令」，一次性的认证，或是基本上能够用以下句子描述的任何情况: 

你好，服务器 B，服务器 A 告诉我我可以 <...Claim...>，这是我的证据: < ... 密钥... >。

举个例子，你有个文件服务，用户必须认证后才能下载文件，但文件本身存储在一台完全分离且无状态的「下载服务器」内。在这种情况下，你可能想要「应用服务器 (服务器 A) 」颁发一次性的「下载 Tokens」，用户能够使用它去「下载服务器 (服务器 B) 」获取需要的文件。

以这种方式使用 JWT，具备几个明确的特性: 

Tokens 生命期较短。它们只需在几分钟内可用，让客户端能够开始下载。
Tokens 仅单次使用。应用服务器应当在每次下载时颁发新的 Token。所以任何 Token 只用于一次请求就会被抛弃，不存在任何持久化的状态。
应用服务器依旧使用 Sessions。仅仅下载服务器使用 Tokens 来授权每次下载，因为它不需要任何持久化状态。
正如以上你所看到的，结合 Sessions 和 JWT Tokens 有理有据。它们分别拥有各自的目的，有时候你需要两者一起使用。只是不要把 JWT 用作 持久的、长期的 数据就好。

---

https://learnku.com/articles/22616
