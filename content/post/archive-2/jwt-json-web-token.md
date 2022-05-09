---
title: JWT, JSON Web Token
author: "-"
date: 2018-07-30T12:02:39+00:00
url: /?p=12462
categories:
  - Inbox
tags:
  - reprint
---
## JWT, JSON Web Token
### 会话
会话跟踪技术是一种在客户端与服务器间保持 HTTP 状态的解决方案,我们所熟知的有 Cookie + Session、URL 重写、Token 等。

### jwt
JWT 的全称是 Json Web Token,是一种基于 JSON 的、用于在网络上声明某种主张的令牌 (token) 规范。

JWT 由三部分组成: head、payload、signature,各部分通过 ‘ . ’ 连接
xxxx . yyyy . zzzz

#### HEAD
头部是一个 JSON 对象,包含了一些元数据, 存储描述数据类型 (JWT) 和签名算法 (HSA256、RSA256) ,通过 Base64UrlEncode 编码后生成 head 。
```json
{
  "typ" : "JWT",
  "alg" : "HS256"
}
```

type: 必需。token 类型,JWT表示是 JSON Web Token.  
alg: 必需。token 所使用的签名算法,可用的值在这里有规定。  

#### PAYLOAD
负载存放一些传输的有效声明,可以使用官方提供的声明,也可以自定义声明。同样通过 Base64UrlEncode 编码后生成 payload。
 
声明可以分为三种类型: 

Registered claims:

官方预定义的、非强制性的但是推荐使用的、有助于交互的声明(注意使用这些声明只能是三个字符)。


----

JSON Web Token (JWT)是一种基于 token 的认证方案。

JSON Web Token 的结构

一个 JWT token 看起来是这样的:

>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEzODY4OTkxMzEsImlzcyI6ImppcmE6MTU0ODk1OTUiLCJxc2giOiI4MDYzZmY0Y2ExZTQxZGY3YmM5MGM4YWI2ZDBmNjIwN2Q0OTFjZjZkYWQ3YzY2ZWE3OTdiNDYxNGI3MTkyMmU5IiwiaWF0IjoxMzg2ODk4OTUxfQ.uKqU9dTB6gKwG6jQCuXYAiMNdfNRw98Hw_IWuA5MaMo

可以简化为下面这样的结构:

    base64url_encode(Header) + '.' + base64url_encode(Claims) + '.' + base64url_encode(Signature)

Claims (Payload)

Claims 部分包含了一些跟这个 token 有关的重要信息。 JWT 标准规定了一些字段,下面节选一些字段:

- iss: The issuer of the token,token 签发人
- sub: The subject of the token,token 主题
- aud: audience 受众
- exp: Expiration Time。 token 过期时间,Unix 时间戳格式
- nbf: Not Before 生效时间
- iat: Issued At。 token 创建时间, Unix 时间戳格式, 签发时间
- jti: JWT ID。编号, 针对当前 token 的唯一标识

#### 其它 claim name, IANA JSON Web Token Registry中定义的关键字。
    https://www.iana.org/assignments/jwt/jwt.xhtml

#### Public claims: 
保留给 JWT 的使用者自定义。但是需要注意避免使用IANA JSON Web Token Registry中定义的关键字。

#### Private claims:
保留给 JWT 的使用者自定义,用来传送传输双方约定好的消息。

#### SIGNATURE
数据签名是 JWT 的核心部分,构成较为复杂,且无法被反编码。

signature 可以选择对称加密算法或者非对称加密算法,常用的就是 HS256、RS256。
对称加密:  加密方和解密方利用同一个秘钥对数据进行加密和解密。
非对称加密:  加密方用私钥加密,并把公钥告诉解密方用于解密。

---


https://www.jianshu.com/p/15572dfa4ccd

http://blog.leapoahead.com/2015/09/06/understanding-jwt/

JWT (其实还有SAML) 最适合的应用场景就是"开票",或者"签字"。

在有纸化办公时代,多部门、多组织之间的协同工作往往会需要拿着A部门领导的"签字"或者"盖章"去B部门"使用"或者"访问"对应的资源,其实这种"领导签字/盖章"就是JWT,都是一种由具有一定权力的实体"签发"并"授权"的"票据"。一般的,这种票据具有可验证性 (领导签名/盖章可以被验证,且难于模仿) ,不可篡改性 (涂改过的文件不被接受,除非在涂改处再次签字确认) ；并且这种票据一般都是"一次性"使用的,在访问到对应的资源后,该票据一般会被资源持有方收回留底,用于后续的审计、追溯等用途。

举两个例子: 

员工李雷需要请假一天,于是填写请假申请单,李雷在获得其主管部门领导签字后,将请假单交给HR部门韩梅梅,韩梅梅确认领导签字无误后,将请假单收回,并在公司考勤表中做相应记录。
  
员工李雷和韩梅梅因工外出需要使用公司汽车一天,于是填写用车申请单,签字后李雷将申请单交给车队司机老王,乘坐老王驾驶的车辆外出办事,同时老王将用车申请单收回并存档。
  
在以上的两个例子中,"请假申请单"和"用车申请单"就是JWT中的payload,领导签字就是base64后的数字签名,领导是issuer,"HR部门的韩梅梅"和"司机老王"即为JWT的audience,audience需要验证领导签名是否合法,验证合法后根据payload中请求的资源给予相应的权限,同时将JWT收回。

### aud
https://stackoverflow.com/questions/28418360/jwt-json-web-token-audience-aud-versus-client-id-whats-the-difference

As it turns out, my suspicions were right. The audience aud claim in a JWT is meant to refer to the Resource Servers that should accept the token.

As this post simply puts it:

The audience of a token is the intended recipient of the token.

The audience value is a string -- typically, the base address of the resource being accessed, such as https://contoso.com.

The client_id in OAuth refers to the client application that will be requesting resources from the Resource Server.

The Client app (e.g. your iOS app) will request a JWT from your Authentication Server. In doing so, it passes it's client_id and client_secret along with any user credentials that may be required. The Authorization Server validates the client using the client_id and client_secret and returns a JWT.

The JWT will contain an aud claim that specifies which Resource Servers the JWT is valid for. If the aud contains www.myfunwebapp.com, but the client app tries to use the JWT on www.supersecretwebapp.com, then access will be denied because that Resource Server will see that the JWT was not meant for it.


---

http://blog.leapoahead.com/2015/09/06/understanding-jwt/  

JWT(auth0): RS256非对称加密算法实现Token的签发、验证
原文链接:  https://xie.infoq.cn/article/e55bb7e46be860902e39f9280?utm_source=rss&utm_medium=article

>https://github.com/dgrijalva/jwt-go
