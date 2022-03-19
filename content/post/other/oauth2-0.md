---
title: OAuth2.0
author: "-"
date: 2012-06-24T06:53:01+00:00
url: /?p=3646
categories:
  - Web

tags:
  - reprint
---
## OAuth2.0

  http://baike.baidu.com/view/6619164.htm


  OAuth 1.0已经在IETF尘埃落定，编号是RFC5894 
  
  
  
    这也标志这OAuth已经正式成为互联网标准协议。
  
  
  
    OAuth 2.0早已经开始讨论和建立的草案。OAuth2.0 很可能是下一代的"用户验证和授权"标准。现在百度开放平台，腾讯开放平台等大部分的开放平台都是使用的OAuth 2.0协议作为支撑。
  
  
  
    OAuth (开放授权) 是一个开放标准，允许用户让第三方应用访问该用户在某一网站上存储的私密的资源 (如照片，视频，联系人列表) ，而无需将用户名和密码提供给第三方应用。
  
  
    OAuth
  
  
    允许用户提供一个令牌，而不是用户名和密码来访问他们存放在特定服务提供者的数据。每一个令牌授权一个特定的网站 (例如，视频编辑网站)在特定的时段 (例如，接下来的2小时内) 内访问特定的资源 (例如仅仅是某一相册中的视频) 。这样，OAuth允许用户授权第三方网站访问他们存储在另外的服务提供者上的信息，而不需要分享他们的访问许可或他们数据的所有内容。
  
  
  
    OAuth是OpenID的一个补充，但是完全不同的服务。
  
  
  
    OAuth 2.0
  
  
  
    是OAuth协议的下一版本，但不向后兼容OAuth 1.0。 OAuth 2.0关注客户端开发者的简易性，同时为Web应用，桌面应用和手机，和起居室设备提供专门的认证流程。规范还在IETF OAuth工作组的开发中，按照Eran Hammer-Lahav的说法，OAuth将于2010年末完成。
  
  
  
    Facebook的新的Graph API只支持OAuth 2.0，Google在2011年3月亦宣布Google API对OAuth 2.0的支援。
  
  
    认证和授权过程
  
  
    在认证和授权的过程中涉及的三方包括: 
  
  
  
    1、服务提供方，用户使用服务提供方来存储受保护的资源，如照片，视频，联系人列表。
  
  
  
    2、用户，存放在服务提供方的受保护的资源的拥有者。
  
  
  
    3、客户端，要访问服务提供方资源的第三方应用，通常是网站，如提供照片打印服务的网站。在认证过程之前，客户端要向服务提供者申请客户端标识。
  
  
  
    使用OAuth进行认证和授权的过程如下所示:
  
  
  
    用户访问客户端的网站，想操作用户存放在服务提供方的资源。
  
  
  
    客户端向服务提供方请求一个临时令牌。
  
  
  
    服务提供方验证客户端的身份后，授予一个临时令牌。
  
  
  
    客户端获得临时令牌后，将用户引导至服务提供方的授权页面请求用户授权。在这个过程中将临时令牌和客户端的回调连接发送给服务提供方。
  
  
  
    用户在服务提供方的网页上输入用户名和密码，然后授权该客户端访问所请求的资源。
  
  
  
    授权成功后，服务提供方引导用户返回客户端的网页。
  
  
  
    客户端根据临时令牌从服务提供方那里获取访问令牌。
  
  
  
    服务提供方根据临时令牌和用户的授权情况授予客户端访问令牌。
  
  
  
    客户端使用获取的访问令牌访问存放在服务提供方上的受保护的资源。
  
  
    简单历史回顾
  
  
    OAuth 1.0在2007年的12月底发布并迅速成为工业标准。
  
  
  
    2008年6月，发布了OAuth 1.0 Revision A，这是个稍作修改的修订版本，主要修正一个安全方面的漏洞。
  
  
  
    2010年四月，OAuth 1.0的终于在IETF发布了，协议编号RFC 5849。
  
  
  
    OAuth 2.0的草案是在今年5月初在IETF发布的。
  
  
  
    OAuth is a security protocol that enables users to grant third-party access to their web resources without sharing their passwords.
  
  
  
    OAuth是个安全相关的协议，作用在于，使用户授权第三方的应用程序访问用户的web资源，并且不需要向第三方应用程序透露自己的密码。
  
  
  
    OAuth 2.0是个全新的协议，并且不对之前的版本做向后兼容，然而，OAuth 2.0保留了与之前版本OAuth相同的整体架构。
  
  
  
    这个草案是围绕着 OAuth2.0的需求和目标，历经了长达一年的讨论，讨论的参与者来自业界的各个知名公司，包括Yahoo!, Facebook, Salesforce, Microsoft, Twitter, Deutsche Telekom, Intuit, Mozilla, and Google。
  
  
  
    OAuth 2.0的新特性: 
  
  
    6种全新的流程: 
  
  
    User-Agent Flow – 客户端运行于用户代理内 (典型如web浏览器) 。
  
  
  
    Web Server Flow – 客户端是web服务器程序的一部分，通过http request接入，这是OAuth 1.0提供的流程的简化版本。
  
  
  
    Device Flow – 适用于客户端在受限设备上执行操作，但是终端用户单独接入另一台电脑或者设备的浏览器
  
  
  
    Username and Password Flow – 这个流程的应用场景是，用户信任客户端处理身份凭据，但是仍然不希望客户端储存他们的用户名和密码，这个流程仅在用户高度信任客户端时才适用。
  
  
  
    Client Credentials Flow – 客户端适用它的身份凭据去获取access token，这个流程支持2-legged OAuth的场景。
  
  
  
    Assertion Flow – 客户端用assertion去换取access token，比如SAML assertion。
  
  
  
    可以通过使用以上的多种流程实现Native应用程序对OAuth的支持 (程序运行于桌面操作系统或移动折本) 
  
  
  
    application support (applications running on a desktop or mobile device) can be implemented using many of the flows above.
  
  
  
    持信人token
  
  
  
OAuth 2.0 提供一种无需加密的认证方式，此方式是基于现存的cookie验证架构，token本身将自己作为secret，通过HTTPS发送，从而替换了通过 HMAC 和token secret加密并发送的方式，这将允许使用cURL发起APIcall和其他简单的脚本工具而不需遵循原先的request方式并进行签名。
  
  
  
    签名简化: 
  
  
  
    对于签名的支持，签名机制大大简化，不需要特殊的解析处理，编码，和对参数进行排序。使用一个secret替代原先的两个secret。
  
  
  
    短期token和长效的身份凭据
  
  
  
    原先的OAuth，会发行一个 有效期非常长的token(典型的是一年有效期或者无有效期限制)，在OAuth 2.0中，server将发行一个短有效期的access token和长生命期的refresh token。这将允许客户端无需用户再次操作而获取一个新的access token，并且也限制了access token的有效期。
  
  
  
    角色分开
  
  
  
    OAuth 2.0将分为两个角色: 
  
  
  
    Authorization server负责获取用户的授权并且发布token。
  
  
  
    Resource负责处理API calls。
  
